#!/usr/bin/env python3
"""Step 9, arm b -- REJECTION PROBE for the ordering guard in src/step9_b_13_register_0124.py.

WHY THIS EXISTS. decisions/0123 SS3, the Human Lead's ruling: A PRECONDITION THAT CANNOT FAIL ON
THE VECTOR IT POLICES IS NOT A CHECK. The ordering guard's whole claim is that it can tell a
STALE producer from a current one -- and on the tree it was written against, the producer is
current, so it passes. A guard shown only passing has not been shown to discriminate.

So it is driven to failure here, on the condition that ACTUALLY FIRED:

  1. HISTORICAL REPRODUCTION. decisions/0125 moved the corrected emission; the register
     generator re-ran and src/step9_b_6_stamp_superseded.py did not. The committed .md
     therefore carried a mark set computed against the PREVIOUS corrected emission. That exact
     file is recovered from git -- the revision of artifacts/step9-headline-b.md immediately
     before the one that re-stamped it -- and the guard is pointed at it while the corrected
     side stands as it does today. It must REJECT, and it must name the cells.

  2. CONSTRUCTED, BOTH DIRECTIONS. A stale producer can be short a mark or carry a spare one,
     and only the first is what 0125 produced. So the second is constructed: one mark is
     stripped from a marked cell and one is added to an unmarked CI cell of the same table.
     The guard must name both, in the right direction.

  3. THE CURRENT TREE. It must PASS, and its coverage is printed, because a guard that examined
     zero cells passes trivially and a clean result and an empty result are the same value.

READ-ONLY, AND VERIFIED SO RATHER THAN ASSERTED. Every case runs through
step9_b_13_register_0124.rerun_stamper_read_only(), which copies its inputs into a scratch
directory before the stamper touches anything. The sha256 of all three committed surfaces is
taken before and after and compared; nothing under artifacts/ or processed/ is written by this
script or by anything it calls.

GIT IS READ WITH `--format=%H` AND NOTHING ELSE. Commit messages before 2026-08-24 carry
cross-arm content (decisions/0125 SS5d), so no message body is fetched here; only hashes, dates,
and the contents of this arm's own path.

Run:  python3 src/step9_b_17_ordering_repro.py     (exit 0 = the guard discriminated)
"""

import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import step9_b_13_register_0124 as G                                            # noqa: E402
import step9_b_6_stamp_superseded as M                                          # noqa: E402

MD_REL = "artifacts/step9-headline-b.md"
MARK = M.MD_ROW_MARK_0124


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


def git(*args):
    return subprocess.check_output(["git", "-C", ROOT] + list(args)).decode()


def run_guard(overrides=None):
    """(passed, message_or_coverage). A SystemExit from the guard is a rejection."""
    try:
        return True, G.assert_producer_not_stale(overrides)
    except SystemExit as e:
        return False, str(e)


def rows_under(md_path):
    """How many register rows step9_b_13 derives when the marked .md is `md_path`.

    Derivation only -- src/step7_register.py is not opened and nothing is written. The module
    global is restored in a finally block.
    """
    saved = M.COMMITTED_MD
    try:
        M.COMMITTED_MD = md_path
        return len(G.derive_rows()["rows"])
    finally:
        M.COMMITTED_MD = saved


def previous_revision_of_the_md(tmp):
    """The committed .md as it stood before the most recent re-stamp, or None.

    Identified structurally, not by a typed hash: the revision immediately preceding the newest
    one that touched this path. The hash and date it resolves to are PRINTED, so the reader can
    check which state was reconstructed rather than take the label for it.
    """
    revs = [ln.split() for ln in
            git("log", "--format=%H %ad", "--date=short", "--", MD_REL).strip().split("\n") if ln]
    if len(revs) < 2:
        return None, None, None
    h, date = revs[1]
    path = os.path.join(tmp, "pre_restamp.md")
    with open(path, "wb") as fh:
        fh.write(subprocess.check_output(["git", "-C", ROOT, "show", "%s:%s" % (h, MD_REL)]))
    return path, h[:9], date


def constructed_both_directions(tmp):
    """Current .md with one mark stripped and one added, in the stamper's own cell format."""
    lines = open(M.COMMITTED_MD).read().split("\n")
    stripped = added = None
    for i, ln in enumerate(lines):
        if stripped is None and ln.startswith("|") and MARK in ln:
            lines[i] = ln.replace(MARK, "", 1)
            stripped = i + 1
            continue
        if added is None and stripped is not None and ln.startswith("| W108_s2_finale") \
                and MARK not in ln:
            cells = ln.split("|")
            k = next((j for j, c in enumerate(cells) if "%" in c or "." in c), None)
            if k is None:
                continue
            cells[k] = cells[k].rstrip() + MARK + " "
            lines[i] = "|".join(cells)
            added = i + 1
    if stripped is None or added is None:
        return None, None, None
    path = os.path.join(tmp, "constructed.md")
    open(path, "w").write("\n".join(lines))
    return path, stripped, added


def main():
    surfaces = [M.COMMITTED_MD, M.COMMITTED_HEADLINE, M.COMMITTED_WORKING]
    before = {p: sha(p) for p in surfaces}
    tmp = tempfile.mkdtemp(prefix="step9b-ordering-repro-")
    results = []
    record = {
        "run": "Step 9, arm b -- rejection probe for the ordering guard",
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc)
                                   .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "probe": "src/step9_b_17_ordering_repro.py",
        "probe_sha256_12": sha(os.path.abspath(__file__)),
        "guard": "src/step9_b_13_register_0124.py::assert_producer_not_stale",
        "producer": "src/step9_b_6_stamp_superseded.py",
        "rule": G.PRODUCER_STALENESS_RULE,
        "adopts": "nothing",
        "api_calls": 0,
        "writes_to_artifacts_or_processed": 0,
        "cases": {},
    }

    print("1. HISTORICAL REPRODUCTION -- the condition that fired at decisions/0125")
    hist, h, date = previous_revision_of_the_md(tmp)
    if hist is None:
        print("   the previous revision of %s is not recoverable from this checkout." % MD_REL)
        print("   CONSTRUCTED EQUIVALENT USED INSTEAD -- stated, not silently substituted.")
        results.append(None)
    else:
        cur = open(M.COMMITTED_MD).read()
        old = open(hist).read()
        print("   committed .md at %s (%s), %d marks; HEAD's file has %d."
              % (h, date, old.count(MARK), cur.count(MARK)))
        print("   corrected emission: as it stands NOW, i.e. after 0125's re-emission.")
        if old.count(MARK) == cur.count(MARK) and old == cur:
            # STATED, NOT SILENTLY PASSED. `revs[1]` is the revision before the newest one that
            # touched this path; a later commit that edits the .md WITHOUT re-stamping moves
            # that pointer off the pre-0125 state, and this case then has nothing stale to
            # reject. It fails loudly below either way -- this says WHY, so the failure is not
            # read as the guard having stopped working.
            print("   *** THE HISTORICAL CONDITION IS NO LONGER AT THIS REVISION: it is "
                  "byte-identical to HEAD's file, so there is no stale mark set here to "
                  "reject. Point this case at the pre-0125 revision, or use case 2. ***")
        ok, msg = run_guard({"COMMITTED_MD": hist})
        print("   guard: %s" % ("*** DID NOT FIRE ***" if ok else "REJECTED as intended"))
        if not ok:
            for ln in msg.split("\n"):
                if ln.strip():
                    print("     %s" % ln.strip()[:160])
        results.append(not ok)

        # WHAT THE STALENESS COST, MEASURED. The guard's job is to make this visible; without
        # it the two runs below are indistinguishable, because the missing rows are missing
        # from the very output that would have reported them.
        stale = rows_under(hist)
        live = rows_under(M.COMMITTED_MD)
        print("   register rows derived from the STALE mark set: %d; from the current one: %d"
              % (stale, live))
        print("   -> SHORT BY %d, and both runs print a clean count. %s"
              % (live - stale, "This is the shortfall." if live > stale else
                 "*** NO SHORTFALL REPRODUCED ***"))
        results.append(live > stale)
        record["cases"]["1_historical"] = {
            "reconstructed": True,
            "revision_of_the_md": h, "revision_date": date,
            "marks_in_that_revision": old.count(MARK), "marks_at_head": cur.count(MARK),
            "corrected_side": "as it stands now, i.e. after 0125's re-emission",
            "guard_rejected": not ok,
            "register_rows_under_the_stale_mark_set": stale,
            "register_rows_under_the_current_mark_set": live,
            "rows_lost_silently": live - stale,
        }

    print("\n2. CONSTRUCTED, BOTH DIRECTIONS -- one mark stripped, one spare mark added")
    con, s_line, a_line = constructed_both_directions(tmp)
    if con is None:
        sys.exit("probe setup failed: no marked and no unmarked adopted-arm row was found")
    print("   mark stripped from raw line %d; spare mark added at raw line %d" % (s_line, a_line))
    ok, msg = run_guard({"COMMITTED_MD": con})
    both = (not ok) and "AND THE FILE ON DISK DOES NOT" in msg and "NO LONGER MARKS" in msg
    print("   guard: %s" % ("REJECTED, naming both directions" if both else
                            ("*** DID NOT FIRE ***" if ok else "rejected, but not both directions")))
    if not ok:
        for ln in msg.split("\n"):
            if ln.strip():
                print("     %s" % ln.strip()[:160])
    results.append(both)
    record["cases"]["2_constructed_both_directions"] = {
        "mark_stripped_at_raw_line": s_line, "spare_mark_added_at_raw_line": a_line,
        "guard_rejected_naming_both_directions": both,
    }

    print("\n3. THE CURRENT TREE -- must PASS, and the pass must not be vacuous")
    ok, cov = run_guard()
    print("   guard: %s" % ("PASS" if ok else "*** HARD STOP: %s ***" % str(cov)[:300]))
    if ok:
        for k in sorted(cov):
            print("     %-46s %d" % (k, cov[k]))
        ok = ok and cov["md_table_cells_compared_on_disk"] > 0 \
            and cov["json_string_leaves_compared"] > 0
    results.append(ok)
    record["cases"]["3_current_tree"] = {"guard_passed": bool(ok),
                                         "coverage": cov if isinstance(cov, dict) else None}

    after = {p: sha(p) for p in surfaces}
    print("\nsurfaces untouched: %s"
          % ("byte-identical, all %d" % len(surfaces) if before == after
             else "*** MISMATCH *** %s %s" % (before, after)))
    checked = [r for r in results if r is not None]
    print("%d of %d cases behaved as specified." % (sum(checked), len(checked)))
    record["surfaces_byte_identical_before_and_after"] = (before == after)
    record["cases_as_specified"] = "%d of %d" % (sum(checked), len(checked))
    # 0109: the CODE lives in src/ and is committed; the RUN RECORD lives in logs/. A control's
    # exit status is not this arm's measurement to publish in artifacts/ (0096 ruling 1).
    out = os.path.join(ROOT, "logs", "step9_b_ordering_guard_repro.json")
    with open(out, "w") as fh:
        json.dump(record, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("run record: logs/step9_b_ordering_guard_repro.json")
    sys.exit(0 if (all(checked) and before == after) else 1)


if __name__ == "__main__":
    main()
