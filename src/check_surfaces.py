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
SPEC = ["1 task-sheet", "2 ds", "3 ds-b", "4 ae", "5 ae-b"]

# value -> what it was. A value with a live legitimate reading is NOT here; those live in
# LEGITIMATE below, which is what keeps the control armed without chasing ghosts.
SUPERSEDED = {
    9.6830: "S&L floor / sub-interval floor, APPLY",
    0.0503: "sub-interval width, APPLY",
    73.3466: "Continued value, attainable-corner floor row, APPLY",
    73.6537: "Continued ceiling, APPLY",
    11.3619: "S&L floor / sub-interval floor, DERIV",
    82.4327: "Continued ceiling, DERIV",
    0.4033: "APPLY bound width differenced from rounded endpoints",
    0.4703: "S&L bound over sampling width, arm a, pre-widening",
}
LEGITIMATE = {
    # The two-extremes table: 0055 SS2 asked both arms for the floor under extreme NONE as well
    # as extreme ALL. The NONE column IS 9.6830 / 11.3619, and the Continued ceiling under NONE
    # IS 73.6537 / 82.4327. Those are correct where they are labelled as the NONE extreme, and
    # superseded everywhere they stand as the adopted figure. Context decides, not the value.
    "extreme-NONE column": "9.6830 / 11.3619 / 73.6537 / 82.4327 are the correct extreme-NONE "
                           "readings in the two-extremes table, and superseded as adopted figures",
    0.3575: "APPLY exclusion share of population, 703 / 196,654 -- superseded only as a bound WIDTH",
    0.0672: "DERIV exclusion share of population, 99 / 147,370 -- superseded only as a bound WIDTH",
    19042: "post-liveness started-and-left POINT ESTIMATE on APPLY -- not the bound floor",
    16744: "post-liveness S&L count on 147,271, and the DERIV floor under extreme NONE",
    632: "frozen-D10 never-started component at W = 125",
    703: "adopted APPLY exclusion count",
}
ADOPTED = {
    # ae / ae-b deliberately hold NO Step 9 bound figures (0055 SS5a) -- they are not owners.
    9.6372: SPEC[:3] + ["6 artifacts", "7 second-brain"],
    0.0961: SPEC[:3] + ["6 artifacts", "7 second-brain"],
    0.4032: SPEC[:3] + ["6 artifacts", "7 second-brain"],
    73.6995: SPEC[:3] + ["6 artifacts", "7 second-brain"],
    73.3924: ["6 artifacts"],
    11.3015: SPEC[:3] + ["6 artifacts", "7 second-brain"],
    82.4930: SPEC[:3] + ["6 artifacts"],
}

TOL = 5e-5
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.\d+)(?![\w])")
MARK = re.compile(r"SUPERSEDED|superseding|WITHDRAWN|withdraw|~~|no legitimate|"
                  r"not to be restated|must not be|pre-widening|was ALT|PF-LIMIT|"
                  r"legitimate|register|corrected|ADOPTED|un-?widened|rounding artifact|not 0\\.4033|vs 0\\.4033", re.I)
# A hit is DECLARED, not a defect, when its own context says which reading it is. The
# extreme-NONE column of the two-extremes table is the main one: both arms were asked for it.
DECLARE = re.compile(r"extreme[_ ]NONE|unwidened|un-widened|proposed|superseded|SUPERSEDED|"
                     r"_DERIVED|share_of_population|_scope", re.I)
CONTEXT = 6   # markers wrap onto neighbouring lines; review 11 read three as unmarked for this


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
    neg, pos = [], {v: set() for v in ADOPTED}
    for surface, files in SURFACES.items():
        for f in files:
            is_json = f.endswith(".json")
            items = ([(v, p, p) for v, p in json_numbers(f)] if is_json
                     else text_numbers(f))
            # A file whose head carries a supersession stamp declares its whole body.
            head = ""
            if not is_json:
                try:
                    head = "\n".join(Path(f).read_text().split("\n")[:45])
                except (UnicodeDecodeError, OSError):
                    continue          # binary; nothing to read, nothing to check
            file_stamped = bool(re.search(r"SUPERSEDED", head))
            # The withdrawn-claims register exists to hold withdrawn values; every number in
            # it is there BECAUSE it was withdrawn. Declaring it by name is honest; widening
            # the marker regex to cover it would have exempted live files too.
            if is_json:
                try:
                    file_stamped = "_SUPERSEDED" in json.load(open(f))
                except Exception:
                    file_stamped = False
            if f.endswith("withdrawn-claims-register.md"):
                file_stamped = True
            for val, where, line in items:
                for s, what in SUPERSEDED.items():
                    if near(val, s):
                        # a JSON leaf can never be "labelled" -- there is no prose to carry
                        # a marker, which is exactly why review 11 found six of them there.
                        labelled = bool(line and MARK.search(line))
                        declared = bool(line and DECLARE.search(line)) or file_stamped
                        if not labelled and not declared:
                            neg.append((surface, f, where, val, what,
                                        (line or "").strip()[:110]))
                for a in ADOPTED:
                    if near(val, a):
                        pos[a].add(surface)
    return neg, pos


if __name__ == "__main__":
    neg, pos = scan()
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
    print("LEGITIMATE readings, deliberately not in the negative set:")
    for v, why in LEGITIMATE.items():
        print(f"  {v}: {why}")

    if neg or missing:
        print("\nFAIL")
        sys.exit(1)
    print("\nPASS -- both halves, all seven surfaces.")
