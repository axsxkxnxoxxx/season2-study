#!/usr/bin/env python3
"""Step 9, arm b -- probe the 0124 marks in BOTH directions against src/check_surfaces.py.

A stamp may silence the control in two ways and only one of them is legitimate. It may mark the
figure, or it may DISARM the row that looks for it. The second is indistinguishable from the
first on a clean run, so it is probed rather than asserted:

  A. a superseded W108 CI value REINTRODUCED unmarked must drive exit 1  -> the row is live
  D. the two rows THIS RE-STAMP created -- the W108 started-and-left CI widths, which the
     0125 re-emission newly superseded -- fire the same way                 -> the new rows are live
  B. STRIPPING a 0124 stamp must drive exit 1 at exactly the fields it named, in the JSON and
     in the .md alike                                                    -> the mark is what silences it
  C. the untouched tree must drive exit 0                                -> no false positive

Every mutation is made on the real surface and RESTORED in a finally block; the byte hashes are
compared before and after and printed.

Run:  python3 src/step9_b_14_restamp_probe.py
"""

import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADLINE = os.path.join(ROOT, "artifacts", "step9-headline-b.json")
MD = os.path.join(ROOT, "artifacts", "step9-headline-b.md")
CHECK = os.path.join(ROOT, "src", "check_surfaces.py")

MARK = " ·**SUPERSEDED-0124**"
MARK0123 = " ·**SUPERSEDED**"
MD_TOKEN_0124 = "> **SUPERSEDED — 2026-08-23 (`decisions/0124`)."

CI_PATH = ("arms", 0, "headline", "APPLY", "by_producing_arm", "arms", "b",
           "shares", "never_started", "ci")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]


def run_check():
    r = subprocess.run([sys.executable, CHECK], cwd=ROOT, capture_output=True, text=True)
    body = r.stdout.split("NEGATIVE HALF")[1].split("SURFACE 8")[0] if "NEGATIVE HALF" in r.stdout else ""
    rows = [ln.strip() for ln in body.split("\n") if ln.strip().startswith("[")]
    return r.returncode, rows


def dig(d, path):
    for k in path:
        d = d[k]
    return d


def main():
    before = {HEADLINE: sha(HEADLINE), MD: sha(MD)}
    orig_json = open(HEADLINE).read()
    orig_md = open(MD).read()
    out = []
    try:
        code, rows = run_check()
        out.append(("C  untouched tree", code, len(rows), rows[:1]))

        # A -- reintroduce a superseded CI endpoint at a fresh, unstamped path
        d = json.loads(orig_json)
        superseded_lower = dig(d, CI_PATH)["lower"]
        m = re.search(r"\d+\.\d+", str(superseded_lower))
        d["probe_reintroduced_unmarked"] = superseded_lower
        json.dump(d, open(HEADLINE, "w"), indent=2, ensure_ascii=False)
        code, rows = run_check()
        out.append(("A  %r reintroduced unmarked in the JSON" % round(superseded_lower, 6),
                    code, len(rows), [r for r in rows if "probe" in r][:1]))
        open(HEADLINE, "w").write(orig_json)

        # B1 -- strip the 0124 stamp from one ci.note; its lower/upper lose the exemption
        d = json.loads(orig_json)
        note = dig(d, CI_PATH)["note"]
        assert "SUPERSEDED 2026-08-23" in note, "the site under probe carries no 0124 stamp"
        dig(d, CI_PATH)["note"] = note.split(" || ", 1)[1]
        json.dump(d, open(HEADLINE, "w"), indent=2, ensure_ascii=False)
        code, rows = run_check()
        hit = [r for r in rows if "never_started.ci" in r]
        out.append(("B1 0124 stamp stripped from one ci.note", code, len(rows), hit[:2]))
        open(HEADLINE, "w").write(orig_json)

        # B2 -- the whole 0124 .md layer removed: every inline mark AND every 0124 stamp
        # block, i.e. the file exactly as it stood before this re-stamping. It must drive
        # exit 1 on the adopted arm's superseded md figures, or the marking silenced nothing
        # and the register rows on those figures were never live.
        lines = orig_md.split("\n")
        pre, i = [], 0
        while i < len(lines):
            if MD_TOKEN_0124 in lines[i]:
                i += 1
                if i < len(lines) and lines[i].strip() == "":
                    i += 1
                continue
            pre.append(lines[i].replace(MARK, ""))
            i += 1
        open(MD, "w").write("\n".join(pre))
        code, rows = run_check()
        md_rows = [r for r in rows if "step9-headline-b.md" in r]
        out.append(("B2 the whole 0124 .md layer removed (%d stamps, %d marks)"
                    % (orig_md.count(MD_TOKEN_0124), orig_md.count(MARK)),
                    code, len(rows), md_rows[:2]))
        open(MD, "w").write(orig_md)

        # B3 -- THE MEASURED LIMIT, probed rather than claimed. Strip every 0124 mark from ONE
        # row and nothing else. The control stays at exit 0, because src/check_surfaces.py
        # labels a .md figure from a +/-2 LINE WINDOW and from the block stamp above the
        # table -- so inside a densely marked table no single cell mark can be shown to be
        # load-bearing. An INDIVIDUAL .md cell mark is therefore for the READER; what the
        # numeric control actually enforces is the block. Reported, not worked around: this
        # is a shared control and not this arm's to edit.
        target = next(i for i, ln in enumerate(lines)
                      if ln.startswith("| W108_s2_finale__step9__r6 | DERIV | continued")
                      and MARK in ln)
        one = list(lines)
        one[target] = one[target].replace(MARK, "")
        open(MD, "w").write("\n".join(one))
        code, rows = run_check()
        out.append(("B3 LIMIT: all marks off .md line %d only; +/-2 window still labels it"
                    % (target + 1), code, len(rows),
                    [r for r in rows if "step9-headline-b.md" in r][:2]))
        open(MD, "w").write(orig_md)

        # D -- THE ROWS THIS RERUN CREATED, probed rather than assumed.
        #
        # decisions/0125's re-emission moved the corrected figures, which RE-PARTITIONED this
        # file's conditional marks: two W108 started-and-left CI WIDTHS became superseded and
        # were unmarked, and one ratio coincided again and was over-marked. A CONDITIONAL MARK
        # IS A FUNCTION OF TWO FILES -- see CONDITIONAL_MARK_RULE in the stamper.
        #
        # Marking them also made them REGISTRABLE: src/step9_b_13_register_0124.py takes its
        # .md-only rows from the numbers inside MARKED cells, so before the re-stamp these two
        # were neither marked nor registered -- unmarked AND unpoliced, the "passed because it
        # never looked" shape. A clean run proves nothing about a row that does not exist, so
        # the two new rows are shown FIRING on a fresh, unmarked occurrence.
        newly = [w for w in (0.0224, 0.0318)]
        open(MD, "w").write(orig_md + "\nPROBE D, restored below: "
                            + " and ".join("%.4f pp" % w for w in newly) + "\n")
        code, rows = run_check()
        hit = [r for r in rows if "PROBE" in r or "step9-headline-b.md" in r]
        out.append(("D  %s reintroduced unmarked in the .md (rows created by THIS re-stamp)"
                    % ", ".join("%.4f" % w for w in newly), code, len(rows), hit[:2]))
        open(MD, "w").write(orig_md)

        code, rows = run_check()
        out.append(("C' restored tree", code, len(rows), rows[:1]))
    finally:
        open(HEADLINE, "w").write(orig_json)
        open(MD, "w").write(orig_md)

    after = {HEADLINE: sha(HEADLINE), MD: sha(MD)}
    for label, code, n, sample in out:
        print("  %-52s exit %d, %d negative row(s)" % (label, code, n))
        for s in sample:
            print("        %s" % s[:150])
    print("\nrestored: %s" % ("byte-identical, both files" if before == after else "MISMATCH %s %s" % (before, after)))
    expect = [0, 1, 1, 1, 0, 1, 0]
    got = [c for _, c, _, _ in out]
    print("expected exit sequence %s, got %s -- %s"
          % (expect, got, "AS SPECIFIED" if expect == got else "*** NOT AS SPECIFIED ***"))
    sys.exit(0 if (expect == got and before == after) else 1)


if __name__ == "__main__":
    main()
