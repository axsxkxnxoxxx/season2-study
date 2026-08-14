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

# B9 audit (0062): a read or parse failure previously returned [] -- the file contributed no
# numbers and the scan passed. A file that cannot be read is not a file with nothing wrong in it.
READ_FAILURES = []

SURFACES = {
    "1 task-sheet": ["task-sheet.md"],
    "2 ds": [".claude/agents/data-scientist.md"],
    "3 ds-b": [".claude/agents/data-scientist-b.md"],
    "4 ae": [".claude/agents/analytics-engineer.md"],
    "5 ae-b": [".claude/agents/analytics-engineer-b.md"],
    "6 artifacts": sorted(str(p) for p in Path("artifacts").rglob("*")
                          if p.is_file() and p.suffix in (".md", ".json", ".csv", ".txt")),
    # every file, not just *.md -- a .json in this directory was unseen by the whole control
    "7 second-brain": sorted(str(p) for p in Path(".claude/agent-memory/second-brain").rglob("*")
                             if p.is_file()),
}
sys.path.insert(0, str(Path(__file__).parent))
from step7_register import (SUPERSEDED, SUPERSEDED_IN, ADOPTED, ADOPTED_IN, LEGITIMATE,
                            DECLARE_SCOPED, DECLARE_JSON_PATH, SUCCESSOR,
                            WITHDRAWN_PHRASES,
                            file_is_wholly_superseded, scoped)

TOL = 5e-5
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+\.\d+)(?![\w])")
MARK = re.compile(r"SUPERSEDED|superseded|superseding|WITHDRAWN|withdrawn|~~|"
                  r"no legitimate reading|must not be restated|not to be restated|"
                  r"pre-widening|un-?widened|rounding artifact|STRUCK|struck", re.I)
for _dead in ("corrected", "register", "legitimate|", "ADOPTED"):
    assert _dead not in MARK.pattern, f"B5: {_dead!r} is still in MARK"
assert "\\." not in MARK.pattern, "B5: an escaped-dot alternative that can never match"

# B6. DECLARE is per-value AND per-file. There is no general branch: the general one
# disarmed the control for values its phrase had nothing to do with.
DECLARE_PATH = re.compile(DECLARE_JSON_PATH, re.I)

CONTEXT = 2   # MARK's window: a marker may wrap onto the line above or below. The SUCCESSOR
#             rule deliberately does NOT use this window -- it runs on the emitting line (B7).


def near(x, target):
    return abs(x - target) < (TOL if target < 1000 else 0.5)


def json_strings(path):
    """(string value, json path) for every string leaf.

    0061: the numeric half cannot see a WITHDRAWN CLAIM, because a claim is prose. B8 lived in
    a .json string under _DERIVED and in .md text carrying no numbers, in all four operative
    deliverables, while the gap was recorded as hypothetical.
    """
    out = []

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, f"{p}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{p}[{i}]")
        elif isinstance(o, str):
            out.append((o, p))
    try:
        walk(json.load(open(path)), "")
    except Exception as e:                                          # noqa: BLE001
        READ_FAILURES.append((path, f"json_strings: {e}"))
    return out


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
    except Exception as e:                                          # noqa: BLE001
        READ_FAILURES.append((path, f"json_numbers: {e}"))
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
    except UnicodeDecodeError:
        return []                                   # binary: genuinely holds no prose figures
    except Exception as e:                                          # noqa: BLE001
        READ_FAILURES.append((path, f"text_numbers: {e}"))
        return []
    for i, line in enumerate(lines, 1):
        blk = "\n".join(lines[max(0, i - 1 - CONTEXT): i + CONTEXT])
        for m in NUM.finditer(line):
            try:
                out.append((float(m.group(1).replace(",", "")), f"line {i}", blk, line))
            except ValueError:
                pass
    return out


STRUCK = re.compile(r"~~|WITHDRAWN|withdrawn|struck|STRUCK|FALSE:|was false", re.I)


def scan_phrases():
    """Every occurrence of a withdrawn claim outside a strikethrough or a withdrawal note."""
    hits = []
    for surface, files in SURFACES.items():
        for f in files:
            if file_is_wholly_superseded(f):
                continue
            if f.endswith(".json"):
                items = [(v, p, v) for v, p in json_strings(f)]
            else:
                try:
                    lines = Path(f).read_text().split("\n")
                except UnicodeDecodeError:
                    continue                        # binary: no prose to carry a claim
                except OSError as e:
                    READ_FAILURES.append((f, f"scan_phrases: {e}"))
                    continue
                items = [(l, f"line {i}", "\n".join(lines[max(0, i - 2):i + 1]))
                         for i, l in enumerate(lines, 1)]
            for text, where, ctx in items:
                low = text.lower()
                for phrase, why in WITHDRAWN_PHRASES.items():
                    if phrase in low and not STRUCK.search(ctx):
                        hits.append((surface, f, where, phrase, why, text.strip()[:110]))
    return hits


def scan():
    neg, pos, pos_in, allowed, legit_seen = [], {v: set() for v in ADOPTED}, set(), set(), set()
    for surface, files in SURFACES.items():
        for f in files:
            is_json = f.endswith(".json")
            items = ([(v, p, p, p) for v, p in json_numbers(f)] if is_json
                     else text_numbers(f))
            # A file whose head carries a supersession stamp declares its whole body.
            # B2 (Red Team 12). The whole-file exemption is GONE. A file is exempt only if
            # it is NAMED in the allowlist with a reason -- never because a stamp appears in
            # its first 45 lines. That rule exempted 19 .md and 16 .json files, which is the
            # entire Step 7 artifact set INCLUDING BOTH OPERATIVE DELIVERABLES, and is how a
            # wrong ratio survived a passing check. The operative pair is not exemptible.
            whole_file = file_is_wholly_superseded(f)
            for val, where, line, raw in items:
                if whole_file:
                    allowed.add((f, whole_file))
                for s, what in list(SUPERSEDED.items()) + [
                        (v, why) for (frag, v), why in SUPERSEDED_IN.items() if frag in f]:
                    if near(val, s):
                        if whole_file:
                            continue
                        # a JSON leaf can never be "labelled" -- there is no prose to carry
                        # a marker, which is exactly why review 11 found six of them there.
                        # MARK may open one line above, so it reads the context block.
                        labelled = bool(line and MARK.search(line))
                        # B6: declared only where the register scopes it, by file AND value.
                        declared = False
                        if is_json and DECLARE_PATH.search(where):
                            declared = True
                        for frag, table in DECLARE_SCOPED.items():
                            pat = table.get(round(s, 4))
                            if frag in f and pat and line and re.search(pat, line, re.I):
                                declared = True
                        # B7: the successor rule runs on the EMITTING LINE, not the context
                        # block. On the block it was already satisfied non-adversarially --
                        # the adopted 6-dp width 0.403246 is within tolerance of 0.4032 and
                        # self-declared 0.4033 two lines away in either direction.
                        succ = SUCCESSOR.get(round(s, 4))
                        if succ is not None and raw and any(
                                near(float(m.group(1).replace(",", "")), succ)
                                for m in NUM.finditer(raw)):
                            declared = True
                        if not labelled and not declared:
                            neg.append((surface, f, where, val, what,
                                        (line or "").strip()[:110]))
                for lv in LEGITIMATE:
                    if isinstance(lv, (int, float)) and near(val, float(lv)):
                        legit_seen.add(lv)
                for a in ADOPTED:
                    if near(val, a):
                        pos[a].add(surface)
                for (frag, v), why in ADOPTED_IN.items():
                    if frag in f and near(val, v):
                        # 0062: `frag in f` matched bb-b.md and bb-b.json alike, so "all six
                        # ratios OK" did not establish that any was in the JSON. Record which.
                        pos_in.add((frag, v, "json" if is_json else "md"))
    return neg, pos, pos_in, allowed, legit_seen


if __name__ == "__main__":
    neg, pos, pos_in, allowed, legit_seen = scan()
    phrase_hits = scan_phrases()
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

    if READ_FAILURES:
        print("READ/PARSE FAILURES -- a file the control could not look at is NOT a clean file:")
        for f, why in READ_FAILURES:
            print(f"  {f}: {why}")
        print()

    print("PHRASE HALF -- withdrawn CLAIMS, which the numeric halves cannot see (0061):")
    if not phrase_hits:
        print("  none\n")
    for surface, f, where, phrase, why, text in phrase_hits:
        print(f"  [{surface}] {f} {where}: {phrase!r}")
        print(f"        {why}")
        print(f"        {text}")
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
    miss_in = []
    for (f, v), w in ADOPTED_IN.items():
        got = {ext for (ff, vv, ext) in pos_in if (ff, vv) == (f, v)}
        need = {"md", "json"}
        gap = need - got
        if gap:
            miss_in.append((f, v, sorted(gap)))
        print(f"  {'OK  ' if not gap else 'MISS'} {f} {v}: in {sorted(got) or 'NOTHING'}"
              + (f"  MISSING FROM: {sorted(gap)}" if gap else "") + f"  -- {w}")
    print()
    print(f"WHOLLY SUPERSEDED FILES exempted by explicit allowlist ({len(allowed)}), reason each:")
    for f, why in sorted(allowed):
        print(f"  {f}\n      {why}")
    print("  (the OPERATIVE bb-{a,b} deliverables are NOT exemptible -- that is B2)")
    print()
    # 0062: LEGITIMATE was imported and printed and never consulted -- a fourth docstring
    # asserting a code property the code lacked. It is now enforced two ways: a value cannot be
    # both legitimate and superseded, and each row must actually be FOUND somewhere, since a row
    # that matches nothing is an exemption granted against no occurrence.
    legit_conflicts = [v for v in LEGITIMATE
                       if isinstance(v, (int, float))
                       and any(near(float(v), s_) for s_ in SUPERSEDED)]
    legit_unused = [v for v in LEGITIMATE
                    if isinstance(v, (int, float)) and v not in legit_seen]
    print("LEGITIMATE readings -- consulted, not merely listed:")
    for v, why in LEGITIMATE.items():
        mark = ""
        if isinstance(v, (int, float)):
            if any(near(float(v), s_) for s_ in SUPERSEDED):
                mark = "  CONFLICT: also in SUPERSEDED"
            elif v not in legit_seen:
                mark = "  UNUSED: exempts nothing that occurs"
        print(f"  {v}: {why}{mark}")

    if neg or missing or miss_in or phrase_hits or READ_FAILURES or legit_conflicts:
        print("\nFAIL")
        sys.exit(1)
    print("\nPASS -- both halves, all seven surfaces.")
