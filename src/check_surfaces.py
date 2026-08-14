"""Grep the seven propagation surfaces at BOTH precisions, numerically.

Human Lead ruling, 2026-08-13, from Red Team finding 6: the textual grep control cannot
see the JSONs. The register stores 4-dp strings and the JSON stores 6-dp literals, so
"9.6830" is not a substring of "9.682997" and "82.4327" is not a substring of
"82.432653". Every value that survived review 11 was one whose registered form rounds UP
and therefore could never match. The one that rounds DOWN, 73.3466, did match -- and was
read as a pass because the only hit was inside a stamp.

So matching here is NUMERIC, not textual. Every number-shaped token on every surface is
parsed and compared to the register at a tolerance, whatever precision it is written at.

Both halves of the control, per CLAUDE.md:
  NEGATIVE  every superseded value -> zero UNLABELLED hits
  POSITIVE  every adopted value    -> non-zero hits on the surfaces that own it

Exit code 1 if either half fails. Zero API calls; reads only.
"""
import json
import re
import sys
from pathlib import Path

SURFACES = {
    "1 task-sheet": ["task-sheet.md"],
    "2 ds": [".claude/agents/data-scientist.md"],
    "3 ds-b": [".claude/agents/data-scientist-b.md"],
    "4 ae": [".claude/agents/analytics-engineer.md"],
    "5 ae-b": [".claude/agents/analytics-engineer-b.md"],
    "6 artifacts": sorted(str(p) for p in Path("artifacts").rglob("*")
                          if p.is_file() and p.suffix in (".md", ".json", ".csv", ".txt")),
    "7 second-brain": sorted(str(p) for p in Path(".claude/agent-memory/second-brain").rglob("*.md")),
}
sys.path.insert(0, str(Path(__file__).parent))
from step7_register import (SUPERSEDED, SUPERSEDED_IN, ADOPTED, ADOPTED_IN, LEGITIMATE,
                            EXTREME_NONE_READINGS, SUCCESSOR,
                            file_is_wholly_superseded, scoped)

TOL = 5e-5
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.\d+)(?![\w])")
MARK = re.compile(r"SUPERSEDED|superseding|WITHDRAWN|withdraw|~~|no legitimate|"
                  r"not to be restated|must not be|pre-widening|was ALT|PF-LIMIT|"
                  r"legitimate|register|corrected|ADOPTED|un-?widened|rounding artifact|not 0\\.4033|vs 0\\.4033", re.I)
# A hit is DECLARED, not a defect, when its own context says which reading it is. The
# extreme-NONE column of the two-extremes table is the main one: both arms were asked for it.
# DECLARE says WHICH READING this occurrence is, so the value is not the adopted one.
# Narrowed with B2: bare "superseded" is gone -- MARK already covers it, and having it here
# too re-created the adjacent-contradiction pattern as a pass.
DECLARE = re.compile(r"extreme[_ ]NONE|extreme NONE|un-?widened|proposed_pct|"
                     r"_DERIVED|share_of_population|_scope|SUPERSEDED_computed_under|"
                     r"superseded_strings", re.I)
CONTEXT = 2   # a marker may wrap one line; 6 was too wide (Red Team 12)


def near(x, target):
    return abs(x - target) < (TOL if target < 1000 else 0.5)


def json_numbers(path):
    """(numeric value, json path) for every leaf, so 6-dp literals are seen."""
    out = []

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, f"{p}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{p}[{i}]")
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            out.append((float(o), p))
    try:
        walk(json.load(open(path)), "")
    except Exception:
        return []
    return out


def text_numbers(path):
    """(numeric value, 'line N', context block) for every number-shaped token.

    The context block is the line plus CONTEXT lines either side, because a supersession
    marker routinely wraps onto the previous line -- review 11 reported three such lines
    as unmarked when the marker opened one line above.
    """
    out = []
    try:
        lines = Path(path).read_text().split("\n")
    except Exception:
        return []
    for i, line in enumerate(lines, 1):
        blk = "\n".join(lines[max(0, i - 1 - CONTEXT): i + CONTEXT])
        for m in NUM.finditer(line):
            try:
                out.append((float(m.group(1).replace(",", "")), f"line {i}", blk))
            except ValueError:
                pass
    return out


def scan():
    neg, pos, pos_in, allowed = [], {v: set() for v in ADOPTED}, set(), set()
    for surface, files in SURFACES.items():
        for f in files:
            is_json = f.endswith(".json")
            items = ([(v, p, p) for v, p in json_numbers(f)] if is_json
                     else text_numbers(f))
            # A file whose head carries a supersession stamp declares its whole body.
            # B2 (Red Team 12). The whole-file exemption is GONE. A file is exempt only if
            # it is NAMED in the allowlist with a reason -- never because a stamp appears in
            # its first 45 lines. That rule exempted 19 .md and 16 .json files, which is the
            # entire Step 7 artifact set INCLUDING BOTH OPERATIVE DELIVERABLES, and is how a
            # wrong ratio survived a passing check. The operative pair is not exemptible.
            whole_file = file_is_wholly_superseded(f)
            for val, where, line in items:
                if whole_file:
                    allowed.add((f, whole_file))
                for s, what in list(SUPERSEDED.items()) + [
                        (v, why) for (frag, v), why in SUPERSEDED_IN.items() if frag in f]:
                    if near(val, s):
                        if whole_file:
                            continue
                        # a JSON leaf can never be "labelled" -- there is no prose to carry
                        # a marker, which is exactly why review 11 found six of them there.
                        labelled = bool(line and MARK.search(line))
                        declared = bool(line and DECLARE.search(line))
                        if s in EXTREME_NONE_READINGS and line and \
                                re.search(r"extreme[_ ]NONE", line, re.I):
                            declared = True
                        # self-declaring: the successor value is on the same line/context,
                        # so the text is narrating the transition rather than asserting the
                        # superseded value as current.
                        succ = SUCCESSOR.get(s)
                        if succ is not None and line and any(
                                near(float(m.group(1).replace(",", "")), succ)
                                for m in NUM.finditer(line)):
                            declared = True
                        if not labelled and not declared:
                            neg.append((surface, f, where, val, what,
                                        (line or "").strip()[:110]))
                for a in ADOPTED:
                    if near(val, a):
                        pos[a].add(surface)
                for (frag, v), why in ADOPTED_IN.items():
                    if frag in f and near(val, v):
                        pos_in.add((frag, v))
    return neg, pos, pos_in, allowed


if __name__ == "__main__":
    neg, pos, pos_in, allowed = scan()
    n_files = sum(len(v) for v in SURFACES.values())
    print(f"seven surfaces, {n_files} files, numeric matching at tol {TOL} "
          f"-- 4-dp and 6-dp forms both matched\n")

    print("NEGATIVE HALF -- superseded values with no supersession marker on the line:")
    if not neg:
        print("  none\n")
    for s, f, where, val, what, line in neg:
        print(f"  [{s}] {f} {where}: {val}  ({what})")
        if line:
            print(f"        {line}")
    print()

    print("POSITIVE HALF -- adopted values, surfaces that own them:")
    missing = []
    for a, want in ADOPTED.items():
        got = pos[a]
        gap = [w for w in want if w not in got]
        flag = "OK " if not gap else "MISS"
        print(f"  {flag} {a:<9} found on {len(got)}/{len(want)} owning surfaces"
              + (f"  MISSING: {gap}" if gap else ""))
        if gap:
            missing.append((a, gap))
    print()
    print("PER-ARM adopted ratios (0058's own corrections -- the positive half never reached these):")
    miss_in = [(f, v, w) for (f, v), w in ADOPTED_IN.items() if (f, v) not in pos_in]
    for (f, v), w in ADOPTED_IN.items():
        print(f"  {'OK ' if (f, v) in pos_in else 'MISS'} {f} {v}: {w}")
    print()
    print(f"WHOLLY SUPERSEDED FILES exempted by explicit allowlist ({len(allowed)}), reason each:")
    for f, why in sorted(allowed):
        print(f"  {f}\n      {why}")
    print("  (the OPERATIVE bb-{a,b} deliverables are NOT exemptible -- that is B2)")
    print()
    print("LEGITIMATE readings, deliberately not in the negative set:")
    for v, why in LEGITIMATE.items():
        print(f"  {v}: {why}")

    if neg or missing or miss_in:
        print("\nFAIL")
        sys.exit(1)
    print("\nPASS -- both halves, all seven surfaces.")
