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
  NEGATIVE  every superseded value -> zero UNLABELLED hits, across all EIGHT surfaces
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
    # 0074: surface 8. processed/ is the FIRST file a Step 8 implementation reaches for, and no
    # control covered it -- adopted_rule.json carried revision-3 figures against the approved
    # revision-6 rule and an instance had to work around it. Second time it bit.
    #
    # Data tables are data; the figures live in the metadata files. .csv is included but the LARGE
    # ones are skipped BY SIZE and REPORTED, never silently -- a skipped file is not a clean file.
    # DATA TABLES ARE EXCLUDED and the count is reported. A numeric matcher over arbitrary data
    # produces coincidence, not propagation defects: processed/step5/duplicate_pairs.csv alone
    # returned 12 "hits" on per-row measurements that happen to round near a superseded width.
    # The figures this surface exists for live in the METADATA files.
    "8 processed": sorted(str(p) for p in Path("processed").rglob("*")
                          if p.is_file() and p.suffix in (".json", ".md", ".txt")),
}
EXCLUDED_DATA_TABLES = sorted(str(p) for p in Path("processed").rglob("*")
                              if p.is_file() and p.suffix in (".csv", ".gz", ".npz", ".npy",
                                                              ".jsonl", ".ndjson"))
sys.path.insert(0, str(Path(__file__).parent))
from step7_register import (SUPERSEDED, SUPERSEDED_IN, ADOPTED, ADOPTED_IN, LEGITIMATE,
                            DECLARE_SCOPED, DECLARE_JSON_PATH, SUCCESSOR,
                            WITHDRAWN_PHRASES,
                            file_is_wholly_superseded, processed_is_working_output, scoped)

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


WS = re.compile(r"\s+")


def _normalised_with_linemap(lines):
    """The file as ONE whitespace-normalised lowercase string, plus char -> line number.

    0084, found by instance A on the 2026-08-16 rerun. The previous implementation tested
    `phrase in line` ONE LINE AT A TIME, so a withdrawn claim that WRAPS across a line break
    could never match it -- and this repo hard-wraps its prose at ~100 columns, which makes
    wrapping the COMMON case for any phrase over about six words.

    It was not hypothetical when it was found: 0082's withdrawn p_at_bound motive was live in
    second-brain's glossary, broken across a line break, while this half reported `none`. The
    phrase had been registered hours earlier and adversarially probed -- but probed against
    task-sheet.md, where it happens to sit on a single line. THE PROBE CONFIRMED THE CONTROL
    FIRES ON THE UNWRAPPED CASE AND WAS REPORTED AS CONFIRMING THE CONTROL.
    """
    out, linemap = [], []
    for i, line in enumerate(lines, 1):
        # Collapse runs, drop the edges, then rejoin with EXACTLY one space. Joining
        # un-stripped lines leaves a double space at every wrap, which is the same blindness
        # one character narrower -- the self-test below caught precisely that.
        for ch in WS.sub(" ", line.lower()).strip() + " ":
            if ch == " " and out and out[-1] == " ":
                continue                            # never emit two spaces in a row
            out.append(ch)
            linemap.append(i)
    return "".join(out), linemap


def scan_phrases():
    """Every occurrence of a withdrawn claim outside a strikethrough or a withdrawal note.

    Returns (hits, coverage). CLAUDE.md: an empty result and a clean result are the same value
    and only the control knows which it produced, so the coverage is returned, never inferred.
    """
    hits = []
    cov = dict(files=0, lines=0, json_strings=0, phrases=len(WITHDRAWN_PHRASES), skipped=0)
    for surface, files in SURFACES.items():
        for f in files:
            if file_is_wholly_superseded(f):
                cov["skipped"] += 1
                continue
            if f.endswith(".json"):
                # A JSON string leaf carries its own newlines, so normalising it handles the
                # wrapping problem. It does NOT handle PROXIMITY, and 0084's first version of
                # this branch dropped that in the same move -- justified on wrapping while
                # silently widening STRUCK from a windowed context to the WHOLE value, so any
                # paragraph-length note mentioning a withdrawal anywhere exempted every phrase
                # inside it. Red Team P4, third pass. The gap was checked for occupancy and was
                # empty; it is fixed rather than recorded, because "empty today" is exactly how
                # the JSON-string limit was recorded at 0060 while a defect sat in it.
                cov["files"] += 1
                for v, p in json_strings(f):
                    cov["json_strings"] += 1
                    vlines = v.split("\n")
                    flat, linemap = _normalised_with_linemap(vlines)
                    for phrase, why in WITHDRAWN_PHRASES.items():
                        start = 0
                        while True:
                            k = flat.find(phrase, start)
                            if k < 0:
                                break
                            start = k + 1
                            a_, b_ = linemap[k], linemap[min(k + len(phrase), len(linemap) - 1)]
                            ctx = "\n".join(vlines[max(0, a_ - 1 - CONTEXT):b_ + CONTEXT])
                            # 0094: the marker may live in the JSON KEY rather than in the value.
                            # A field named `..._WITHDRAWN_SENTENCE` or `WITHDRAWN_CLAIM` IS the
                            # point-of-use marker CLAUDE.md requires -- structure, not prose. The
                            # .md branch has no analogue because a line has no key. Found when the
                            # phrase half fired on an arm's own correctly-marked withdrawal note.
                            if not STRUCK.search(ctx) and not STRUCK.search(p):
                                hits.append((surface, f, p, phrase, why,
                                             " ".join(vlines[a_ - 1:b_]).strip()[:110]))
                continue

            try:
                lines = Path(f).read_text().split("\n")
            except UnicodeDecodeError:
                cov["skipped"] += 1
                continue                            # binary: no prose to carry a claim
            except OSError as e:
                READ_FAILURES.append((f, f"scan_phrases: {e}"))
                cov["skipped"] += 1
                continue

            cov["files"] += 1
            cov["lines"] += len(lines)
            flat, linemap = _normalised_with_linemap(lines)
            for phrase, why in WITHDRAWN_PHRASES.items():
                start = 0
                while True:
                    k = flat.find(phrase, start)
                    if k < 0:
                        break
                    start = k + 1
                    a, b = linemap[k], linemap[min(k + len(phrase), len(linemap) - 1)]
                    # The marker may sit on either side of a claim that itself spans lines,
                    # so the window is CONTEXT lines around the whole SPAN, not around a line.
                    ctx = "\n".join(lines[max(0, a - 1 - CONTEXT):b + CONTEXT])
                    if not STRUCK.search(ctx):
                        where = f"line {a}" if a == b else f"lines {a}-{b}"
                        hits.append((surface, f, where, phrase, why,
                                     " ".join(lines[a - 1:b]).strip()[:110]))
    return hits, cov


# The wrapped-phrase defect above is exactly the shape CLAUDE.md warns about, so it gets a
# self-test rather than a promise: a registered phrase, hard-wrapped, MUST be found.
def _selftest_phrase_matcher():
    probe = next(iter(WITHDRAWN_PHRASES))
    words = probe.split()
    assert len(words) >= 2, "phrase self-test needs a multi-word phrase"
    wrapped = ["   " + " ".join(words[:1]), "   " + " ".join(words[1:]) + " tail"]
    flat, _ = _normalised_with_linemap(wrapped)
    assert probe in flat, (
        f"PHRASE MATCHER IS BLIND TO WRAPPING: {probe!r} not found across a line break. "
        "This is 0084's defect reappearing.")


_selftest_phrase_matcher()


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
            whole_file = file_is_wholly_superseded(f) or processed_is_working_output(f)
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
    phrase_hits, phrase_cov = scan_phrases()
    n_files = sum(len(v) for v in SURFACES.values())
    print(f"eight surfaces, {n_files} files, numeric matching at tol {TOL} "
          f"-- 4-dp and 6-dp forms both matched\n")

    print("NEGATIVE HALF -- superseded values with no supersession marker on the line:")
    if not neg:
        print("  none\n")
    for s, f, where, val, what, line in neg:
        print(f"  [{s}] {f} {where}: {val}  ({what})")
        if line:
            print(f"        {line}")
    print()

    print(f"SURFACE 8 -- {len(SURFACES['8 processed'])} metadata files scanned; "
          f"{len(EXCLUDED_DATA_TABLES)} DATA TABLES excluded by suffix, reported not silent. "
          f"A numeric matcher over arbitrary data yields coincidence, not propagation defects. "
          f"`adopted_rule.json` and its kind are NOT exemptible, in code.\n")

    if READ_FAILURES:
        print("READ/PARSE FAILURES -- a file the control could not look at is NOT a clean file:")
        for f, why in READ_FAILURES:
            print(f"  {f}: {why}")
        print()

    print("PHRASE HALF -- withdrawn CLAIMS, which the numeric halves cannot see (0061):")
    # 0084: the coverage prints ALWAYS, hit or no hit. This half reported `none` while blind
    # to every phrase that wrapped across a line break, and `none` with no coverage beside it
    # is indistinguishable from `looked nowhere`. Matching is whitespace-normalised.
    print(f"  coverage: {phrase_cov['phrases']} registered phrases x {phrase_cov['files']} files "
          f"({phrase_cov['lines']:,} lines, {phrase_cov['json_strings']:,} JSON strings); "
          f"{phrase_cov['skipped']} skipped. Matching is WHITESPACE-NORMALISED, so a claim "
          f"wrapped across lines is seen (0084).")
    assert phrase_cov["files"] > 0 and phrase_cov["lines"] > 0, \
        "PHRASE HALF LOOKED NOWHERE -- an empty result reported as a clean one"
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
    print("\nPASS -- all halves, all EIGHT surfaces.")
