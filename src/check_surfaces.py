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
import os
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
                            WITHDRAWN_PHRASES, STEP8_LEGITIMATE,
                            SUPERSEDED_STRINGS, SURFACE6_MARKERS, SURFACE6_LINE_LOCAL_CONTROLS,
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


# ============================================================ 0126: ARM-SCOPED OUTPUT
# Human Lead ruling, 2026-08-24, raised by arm b against itself.
#
# THIS CONTROL IS A LEAK VECTOR AND THE ARMS CANNOT SCOPE IT. They are DIRECTED to run it, and
# it prints every surface's paths -- including the other arm's. 0123 scoped the search PATTERN;
# 0125 SS5d scoped what a properly-scoped `git log` RETURNS; this scopes WHAT A SHARED CONTROL
# EMITS. All three exist because an arm is forbidden to re-measure what it is told, and every
# channel that tells it something has to be closed separately.
#
# THE COVERAGE NUMBER STAYS WHOLE. An arm must still be able to tell a clean result from a
# looked-nowhere one, so counts and the exit code are never reduced -- only PATHS are withheld,
# and their number is reported. Suppressing the count as well would substitute this control's
# own founding defect for a leak.
#
# Set STEP_ARM=a or STEP_ARM=b. Unset -- the Human Lead's own runs -- prints everything.
STEP_ARM = os.environ.get("STEP_ARM", "").strip().lower() or None
if STEP_ARM not in (None, "a", "b"):
    sys.exit(f"STEP_ARM={STEP_ARM!r} is not 'a' or 'b'. Refusing to run rather than guess a scope.")

# A path belongs to an arm only on these explicit forms. Anything else is SHARED and shown to
# everyone. Deliberately not a loose /a/ or -a match: `artifacts/step8-invariants-a.json` is
# arm a's, but `processed/step2/frame.csv` is nobody's and must stay visible.
_ARM_PAT = re.compile(r"(?:[-_/])(a|b)(?:\d*)(?:[./_]|$)")


def arm_of(path):
    """'a', 'b' or None (shared). Named forms only."""
    m = _ARM_PAT.search(str(path).replace("\\", "/"))
    return m.group(1) if m else None


_WITHHELD = {"a": 0, "b": 0}


def visible(path):
    """False iff STEP_ARM is set and this path belongs to the OTHER arm. Counts the withholding."""
    if STEP_ARM is None:
        return True
    owner = arm_of(path)
    if owner is None or owner == STEP_ARM:
        return True
    _WITHHELD[owner] += 1
    return False


def show(path):
    """The path as this run may print it."""
    return str(path) if visible(path) else f"<withheld: arm {arm_of(path)} path>"


def withheld_report():
    n = sum(_WITHHELD.values())
    if STEP_ARM is None:
        return "STEP_ARM unset -- every path printed in full (Human Lead view)."
    return (f"STEP_ARM={STEP_ARM}: {n} path(s) belonging to another arm were WITHHELD from this "
            f"output ({_WITHHELD}). THE COUNTS AND THE EXIT CODE ABOVE ARE WHOLE -- nothing was "
            f"excluded from the CHECK, only from the PRINTING. If you needed one of those paths, "
            f"you needed the other arm's work: report it, do not seek it.")


def _selftest_arm_scope():
    """The scoper must withhold what it claims to, and must NOT withhold shared or own paths."""
    global STEP_ARM
    assert arm_of("artifacts/step9-headline-a.json") == "a"
    assert arm_of("artifacts/step9-headline-corrected-2026-08-21-b.json") == "b"
    assert arm_of("src/step9_b_2_bootstrap.py") == "b"
    assert arm_of("processed/step9/a/measured.json") == "a"
    assert arm_of("artifacts/step7-liveness-a2.json") == "a"
    # SHARED must never be attributed to an arm
    for shared in ("task-sheet.md", "CLAUDE.md", "processed/step2/frame.csv",
                   "src/check_surfaces.py", "src/step7_register.py",
                   "processed/step5/adopted_rule.json"):
        assert arm_of(shared) is None, f"{shared} was attributed to arm {arm_of(shared)}"
    keep = STEP_ARM
    try:
        STEP_ARM = "b"; _WITHHELD.update(a=0, b=0)
        assert visible("artifacts/step9-headline-corrected-2026-08-21-b.json") is True
        assert visible("task-sheet.md") is True
        assert visible("artifacts/step9-headline-a.json") is False
        assert _WITHHELD["a"] == 1, "a withheld path was not counted"
    finally:
        STEP_ARM = keep; _WITHHELD.update(a=0, b=0)


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


# Decision numbers are 0001-9999 and every entry to date begins with 0. A bare four-digit
# backticked token is NOT a citation -- `2206` and `2329` are counts in an arm deliverable,
# and the first version of this resolver flagged both. Anchored to the leading zero.
# 0095, Red Team ninth pass F5: the backtick-only form saw ~63% of citations. Arm b writes
# predominantly as `decisions/0089 Sec 2(b)` or bare `0088 Sec 3`, and the founding defect --
# 0092 and 0094 cited before their entries existed -- would have been missed entirely in that
# form. "Prints its coverage count" was satisfied to the letter while the count was blind to
# the class it could not see. Leading-zero anchor kept: 2206 and 2329 are counts, not entries.
# 0122 SS6 (E5). THE FORM-SHAPED HOLE. My own WITHDRAWN_PHRASES rows cited "Withdrawn 0121"
# while decisions/ ran to 0120, and this resolver EXITED 0 over it: the old pattern required
# decisions/NNNN, or a BACKTICKED `NNNN`, or NNNN followed by SS/Sec/ruling. A bare
# "Withdrawn 0121" matched none of them. FIFTH cite-before-write in this study and the FIRST
# inside the register built to catch that class -- so the resolver was blind to the citation
# form its own register uses. A resolver that only recognises the citation forms someone
# happened to think of is a resolver for those forms, not for citations.
#
# Added: the WITHDRAWAL/CORRECTION verbs that this log actually writes, bare and unbackticked.
# Deliberately NOT a bare \b(0\d{3})\b -- that matches years, counts and W values, and a
# resolver that flags every four-digit token would be withdrawn within a day.
CITE = re.compile(
    r"decisions/(0\d{3})"
    r"|`(0\d{3})`"
    r"|\b(0\d{3})\s*(?:\u00a7|SS\d|Sec\b|ruling\b)"
    r"|(?:withdrawn|struck|superseded|corrected|amended|retired|ruled|recorded|filed|per)\s+"
    r"(?:at\s+|in\s+|by\s+)?(0\d{3})\b",
    re.I)


# ------------------------------------------------- 0123: FIELD-SCOPED STAMPS IN JSON
# The JSON half exempts a numeric leaf only when its own PATH carries a MARK token. Arm b's
# 0123 stamps are at the point of use in the CLAUDE.md sense -- a sibling `note` beside the
# figure -- so the leaf's path is clean and the stamp is invisible to that test.
#
# AND THE STAMP NAMES ITS FIELDS: "[SUPERSEDED ... :: fields: numerator_pairs, value_percent]".
# So this honours EXACTLY the named fields and nothing else. It is deliberately NOT an
# object-level exemption: CLAUDE.md's "a file-level stamp declares a file's STATUS, never its
# individual values" is the same defect one level down, and a stamp that exempted every sibling
# would let a corrected figure sit unflagged beside a superseded one.
# 0123, reported by arm b against MY control. The old class excluded `[` and `]`, and the
# terminator was a bare `]` -- so a field name carrying an ARRAY INDEX, e.g.
# "fields: spec_choices_this_arm_made[0], value]", made the whole match FAIL and dropped
# EVERY OTHER NAME in that stamp with it. The failure surfaces as a fresh exit-1 row on an
# UNRELATED figure, which reads like a false positive rather than like a voided stamp.
# The arm worked around it inside its own namespace and did not edit this file; the fix is mine.
# Indices are now accepted, and the list terminates at a `]` followed by whitespace or end.
STAMP_FIELDS = re.compile(r"\bfields:\s*([A-Za-z0-9_,\s\.\[\]]+?)\](?=\s|$)")


def stamped_field_paths(path):
    """JSON paths a sibling stamp explicitly names. Empty set for non-JSON or unreadable files."""
    if not path.endswith(".json"):
        return set()
    try:
        root = json.load(open(path))
    except Exception:                                               # noqa: BLE001
        return set()
    out = set()

    def walk(o, p):
        if isinstance(o, dict):
            stamped = set()
            # A stamp may be a sibling STRING or a sibling OBJECT holding the string one level
            # down -- arm b used `_superseded: {value: "[SUPERSEDED ... fields: value] ..."}`.
            # Reading only same-level strings missed 14 correctly-stamped leaves and reported them
            # as unmarked: a checker's own false positive, found by probing a live register.
            cands = []
            for v in o.values():
                if isinstance(v, str):
                    cands.append(v)
                elif isinstance(v, dict):
                    cands += [s for s in v.values() if isinstance(s, str)]
            for v in cands:
                if MARK.search(v):
                    for m in STAMP_FIELDS.finditer(v):
                        stamped |= {f.strip() for f in m.group(1).split(",") if f.strip()}
            for k in stamped:
                if k in o:
                    out.add(f"{p}.{k}")
            for k, v in o.items():
                walk(v, f"{p}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{p}[{i}]")
    walk(root, "")
    return out


def scan_citations():
    """Every decision citation on the eight surfaces must resolve to a file in decisions/.

    0094 SS4. 0092's entry did not exist while it was cited; 0092 SS2 recorded that no control
    could see it -- "check_surfaces.py checks the eight surfaces for wrong and withdrawn
    content; it does not check that a cited entry exists" -- and left the gap open. 0094's
    entry then did not exist either, cited 8 times. Second occurrence in three entries.

    A gap recorded and left open is a gap that recurs.
    """
    have = {f.name[:4] for f in Path("decisions").glob("[0-9][0-9][0-9][0-9]*.md")}
    seen, missing = {}, {}
    # 0122 SS6 (E5). THE SCOPE HOLE, and it is the operative one -- the FORM hole above was real
    # and was NOT why the control passed. This scan walked SURFACES, and src/ IS NOT A SURFACE,
    # so a citation in src/step7_register.py was invisible whatever the regex said.
    #
    # That is exactly backwards for the register: CLAUDE.md requires "the decision entry that adds
    # or withdraws a row CITES it", so the register's citations are WARRANTS -- the one place a
    # dangling cite disarms a control rather than merely confusing a reader. The rows citing 0121
    # were the fifth cite-before-write in this study and the first inside the register built to
    # catch that class, and BOTH halves of this scan were blind to them.
    #
    # src/ is not promoted to a propagation surface here -- that is a CLAUDE.md change and the
    # Human Lead's. It is added to THIS scan, whose subject is citations rather than figures.
    cite_scope = dict(SURFACES)
    cite_scope["src (citations only, not a propagation surface)"] = sorted(
        str(q) for q in Path("src").rglob("*.py") if q.is_file())
    for surface, files in cite_scope.items():
        for f in files:
            if f.endswith((".gz", ".npz", ".npy")):
                continue
            try:
                text = Path(f).read_text()
            except (UnicodeDecodeError, OSError):
                continue
            found = {g for m in CITE.findall(text) for g in (m if isinstance(m, tuple) else (m,)) if g}
            for n in found:
                seen.setdefault(n, set()).add(f)
                if n not in have:
                    missing.setdefault(n, set()).add(f)
    return have, seen, missing


MARKER_RE = re.compile("|".join(re.escape(m) for m in SURFACE6_MARKERS), re.I)
CHAR_WINDOW = 240   # 0095 F4: the exemption window is measured in CHARACTERS, not lines.
#                     CONTEXT=2 lines is +/-200 chars on a hard-wrapped file and +/-several
#                     THOUSAND on the arms' deliverables, where 137 lines exceed 400 chars and
#                     single paragraphs run to thousands. Same defect the JSON branch was fixed
#                     for; the .md branch was not wrong when written -- the unit changed
#                     underneath it when the arms began emitting paragraph-per-line.


def scan_superseded_strings():
    """The needle register, across ALL EIGHT surfaces -- not four files of one.

    0095 F3. SUPERSEDED_STRINGS and SURFACE6_LINE_LOCAL_CONTROLS were exercised only by
    src/step8_b_4_artifacts.py over its own four artifacts: ~4 of ~40 files on surface 6, and
    none of surfaces 1-5, 7 or 8. Arm b's own scan opens with "a surface check that does not
    open the surface the defect is on is a check that looked nowhere" and then opened four
    files. Occupied, not hypothetical: a registered needle was live in arm a's deliverable.

    Neither arm can do this under isolation -- an arm may not read the other's output, and
    surfaces 1-5 are not an arm's to police. It belongs in the shared control.
    """
    hits, cov = [], dict(files=0, needles=len(SUPERSEDED_STRINGS), chars=0, skipped=0)
    for surface, files in SURFACES.items():
        for f in files:
            if f.endswith((".gz", ".npz", ".npy")):
                cov["skipped"] += 1
                continue
            try:
                text = Path(f).read_text()
            except (UnicodeDecodeError, OSError):
                cov["skipped"] += 1
                continue
            cov["files"] += 1
            cov["chars"] += len(text)
            low = text.lower()
            for needle, why, replacement in SUPERSEDED_STRINGS:
                start = 0
                while True:
                    k = low.find(needle.lower(), start)
                    if k < 0:
                        break
                    start = k + 1
                    a = max(0, k - CHAR_WINDOW)
                    b = min(len(text), k + len(needle) + CHAR_WINDOW)
                    if not MARKER_RE.search(text[a:b]):
                        line = text.count("\n", 0, k) + 1
                        hits.append((surface, f, line, needle, why, replacement))
    return hits, cov


# ------------------------------------------------------------------ 0118: the statistic control
#
# reviewer-engineering's E11, carried in both data-scientist files as "when it IS fixed, a check
# must assert both arms' `statistic` agree -- or the fix will be recorded and unpoliced."
# 0118 fixes it, so the check is built with it rather than after it.
#
# WHY BYTE-IDENTITY AND NOT A KEYWORD SEARCH. CLAUDE.md: "Never describe the task twice in your own
# words: a difference in output would then prove nothing." Two paraphrases of one requirement are
# two definitions of it, and this study's most-repeated defect is a second definition of one figure.
# So the requirement is ONE block, delimited, and the control compares the two copies as bytes.
#
# WHY A MISSING MARKER FAILS. CLAUDE.md: "An empty result and a clean result are the same value,
# and only the control knows which it produced." If a marker is deleted the block extraction returns
# nothing, two nothings compare equal, and a byte-identity check would report clean while covering
# ZERO characters. That is the exact shape of the three controls that reported clean over zero rows.
STAT_BEGIN = "<!-- BOOTSTRAP-STATISTIC-BEGIN -->"
STAT_END = "<!-- BOOTSTRAP-STATISTIC-END -->"
# H4, reviewer-engineering on v1.6.0. BOTH markers are EXACT strings, closing `-->` included.
# The prior BEGIN was the PREFIX "<!-- BOOTSTRAP-STATISTIC-BEGIN" with no terminator, so any prose
# naming the marker moved the extraction start and silently swallowed arbitrary text into the
# "block" -- while byte-identity still passed, because both copies swallowed the same text. The
# character count 0118 SS3 cited as evidence of coverage was the quantity that stopped meaning
# anything first.
STAT_WRITERS = (".claude/agents/data-scientist.md", ".claude/agents/data-scientist-b.md")
# A block shorter than this cannot be the canonical block. This is the REAL coverage floor; see
# the H3 note below for the one it replaces.
STAT_MIN_CHARS = 800

# H5. The four elements are matched as ASSERTIONS, not as substrings present somewhere.
# The prior form tested `needle in block`, which "the arms may choose between levels and paired
# movements" satisfies while REVERSING the ruling, and which "not 10,000 but 4,000" satisfies for B.
# `account` was the fragile one: a bare substring also matched "accounts", "account-clustered",
# "accounted for", and 0118 SS4 REQUIRES this block to carry prose, so one future sentence using the
# word in another sense would have disarmed the unit test silently.
# Matching runs on the block with whitespace collapsed, because the block is line-wrapped.
STAT_REQUIRED = {
    "B = 10,000": (re.compile(r"`B` = \*\*10,000\*\*"), "0103"),
    "seed = 20260818": (re.compile(r"seed = \*\*20260818\*\*"), "0103"),
    "unit = account": (re.compile(r"resampling unit = \*\*account\*\*"), "0103"),
    # ANCHORED ON ITS CLOSING **, found by the arm on the v1.7.0 run: the unanchored form
    # matched "levels and paired movements AND RATIOS", so a THIRD object appended to the ruling
    # passed both this control and the arm's derived-token check. An open-ended pattern tests that
    # the ruling's words APPEAR, not that they are the whole of it.
    "statistic = BOTH levels and paired movements":
        # LOOKAHEAD, not a consumed suffix. reviewer-engineering, v1.7.0 E1: consuming the `**`
        # put it inside group(0), and step8b_selftest.py derives the expected enum by splitting
        # group(0) -- so the token became "movements**", the comparison could never hold, and the
        # selftest emitted "the schema's vocabulary and the writers' requirement have drifted",
        # blaming the schema for a defect in the parser. AN ASSERTION THAT CANNOT PASS, which is
        # H3 inverted -- and the shared-implementation fix for H2 is what coupled them.
        # A lookahead anchors WITHOUT consuming: "movements and ratios**" still fails.
        (re.compile(r"statistic = BOTH levels and paired movements(?=\*\*)"), "0118"),
}
# And the assertion can be reversed by ADDING a sentence rather than by removing one, which no
# positive test can see. These are the reversals; `unfixed` alone is NOT forbidden, because the
# block legitimately says "the third and last unfixed bootstrap element".
STAT_FORBIDDEN = (
    re.compile(r"may choose"),
    re.compile(r"is not fixed"),
    re.compile(r"(remains|still) unfixed"),
    re.compile(r"the spec fixes n(one|either)"),
    re.compile(r"differs? between the arms"),
)


def extract_block(text):
    """THE ONE implementation of the block extraction. Returns (block, error).

    H2, reviewer-engineering on v1.6.0: there were THREE -- this function's predecessor,
    _stat_verdict's copy, and step8b_selftest.py's _extract_block -- and they ALREADY DISAGREED.
    A quoted END marker in prose made check_surfaces.py report "END precedes BEGIN" and exit 1
    while step8b_selftest.py found the real block and reported ok: TWO CONTROLS, OPPOSITE VERDICTS,
    ONE FILE. That is CLAUDE.md's "one definition per statement" applied to code, and the fix for
    a duplicated-register finding had introduced a third register of its own.

    Everything that checks this block imports THIS function and STAT_REQUIRED. Nothing restates them.
    """
    nb, ne = text.count(STAT_BEGIN), text.count(STAT_END)
    if nb != 1 or ne != 1:
        # H4: t.find() took the FIRST of each, so a second contradicting block was invisible and
        # "one definition per statement" was violated with the control passing.
        return None, (f"{nb} BEGIN and {ne} END markers; exactly one of each is required. "
                      f"A duplicate hides a second, possibly contradicting, block from a "
                      f"first-occurrence search")
    i = text.find(STAT_BEGIN)
    j = text.find(STAT_END, i)          # searched AFTER begin, which is where the three disagreed
    if j < 0:
        return None, "the END marker does not follow the BEGIN marker -- the block is malformed"
    blk = text[i:j + len(STAT_END)]
    if len(blk) < STAT_MIN_CHARS:
        return None, (f"the block is {len(blk)} characters, under the {STAT_MIN_CHARS} floor -- "
                      f"a block holding only its markers would otherwise compare equal to itself "
                      f"and report coverage")
    return blk, None


def stat_verdict(text_a, text_b):
    """The whole rule, over two file CONTENTS. Both the live scan and the selftest call this.

    H3. THE ZERO-COVERAGE GUARD IT REPLACES WAS UNSATISFIABLE DEAD CODE. The old line read
    `if cov["chars"] == 0 and not fails`, and chars was assigned ONLY inside the both-blocks-found
    branch, where a block always contains both markers and so is never 0; every other path appends
    to fails before it. The condition could not be met. 0118 SS3 credited the control's
    looked-nowhere protection to that line: the property was real, delivered by the marker branches,
    and attributed to a mechanism that never fired -- CLAUDE.md's withdrawn-mechanism class, inside
    the entry that names it. The floor in extract_block() is the real guard and it CAN fail.
    """
    fails, blocks = [], {}
    for name, text in (("a", text_a), ("b", text_b)):
        blk, err = extract_block(text)
        if err:
            fails.append(f"{name}: {err}")
        else:
            blocks[name] = blk
    if len(blocks) != 2:
        return fails, 0
    a, b = blocks["a"], blocks["b"]
    chars = min(len(a), len(b))
    if a != b:
        n = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), chars)
        fails.append(f"THE TWO ARMS' DECLARATIONS DIFFER, first at character {n}:\n"
                     f"      a: ...{a[max(0, n - 40):n + 40]!r}\n"
                     f"      b: ...{b[max(0, n - 40):n + 40]!r}")
    for name, blk in blocks.items():
        flat = WS.sub(" ", blk)
        for label, (pat, ruling) in STAT_REQUIRED.items():
            if not pat.search(flat):
                fails.append(f"{name}: the block does not ASSERT {label} ({ruling})")
        for pat in STAT_FORBIDDEN:
            if pat.search(flat):
                fails.append(f"{name}: the block contains {pat.pattern!r}, which REVERSES the "
                             f"ruling it is supposed to state -- an assertion can be undone by "
                             f"ADDING a sentence, which no positive test can see")
    return fails, chars


def scan_statistic_declaration():
    """FAIL if the two arms' bootstrap-statistic declarations differ, or if the block is absent.

    KNOWN AND NOT FIXED HERE -- H1, reviewer-engineering, confirmed and WIDER than reported:
    this control reads TWO of the eight surfaces, and the one defect of this class ever found
    (0119 SS2, analytics-engineer{,-b}.md:583) sat in files it does not open. Byte-identity is
    also defeated by a contradiction placed in BOTH copies, inside the block or below it.
    The eight-surface half is scan_unfixity_phrases(), below; neither half subsumes the other.
    """
    fails, cov = [], dict(files=0, chars=0, elements=len(STAT_REQUIRED))
    texts = []
    for f in STAT_WRITERS:
        try:
            texts.append(Path(f).read_text())
            cov["files"] += 1
        except OSError as e:                                        # noqa: BLE001
            fails.append(f"{f}: unreadable ({e}) -- the declaration cannot be checked")
            texts.append("")
    v, chars = stat_verdict(*texts)
    cov["chars"] = chars
    for m in v:
        fails.append(m.replace("a: ", f"{STAT_WRITERS[0]}: ").replace("b: ", f"{STAT_WRITERS[1]}: "))
    return fails, cov


def _selftest_statistic_matcher():
    """The control must FAIL on each thing it claims to catch. Asserted, not asserted-about."""
    body = ("\n`B` = **10,000**, seed = **20260818**, resampling unit = **account**, and "
            "**statistic = BOTH levels and paired movements**.\n" + "padding. " * 90 + "\n")
    good = STAT_BEGIN + body + STAT_END
    assert stat_verdict(good, good)[0] == [], "selftest: identical valid blocks must pass"
    assert stat_verdict(good, good)[1] >= STAT_MIN_CHARS, "selftest: coverage must be reported"
    # the four originals
    assert stat_verdict(good, good.replace("**account**", "**show**"))[0], "mismatch must fail"
    assert stat_verdict(good, good.replace("10,000", "4,000"))[0], "a changed B must fail"
    assert stat_verdict(good.replace(STAT_END, ""), good)[0], "a missing marker must fail"
    assert stat_verdict("", "")[0], "two ABSENT blocks must fail, not compare equal"
    # H4 -- duplicated markers, in BOTH copies so byte-identity cannot catch them
    dup = good + "\n" + good
    assert stat_verdict(dup, dup)[0], "selftest: a duplicated block must fail"
    stray = STAT_BEGIN + "\n" + good
    assert stat_verdict(stray, stray)[0], "selftest: a duplicated BEGIN must fail"
    # H4 -- prose naming the marker must NOT be mistaken for it now that it is closed
    prose = good.replace(body, body + "\nwe write BOOTSTRAP-STATISTIC-BEGIN in prose here.\n")
    assert stat_verdict(prose, prose)[0] == [], "selftest: prose naming a marker must not match it"
    # H3 -- the coverage floor, which the dead guard could not do
    assert stat_verdict(STAT_BEGIN + STAT_END, STAT_BEGIN + STAT_END)[0], \
        "selftest: a markers-only block must fail the floor, not compare equal to itself"
    # H5 -- reversal by ADDITION, identical in both copies
    for reversal in ("the arms may choose between them.", "the statistic is not fixed.",
                     "levels-vs-movements remains unfixed.", "the spec fixes none of them."):
        bad = good.replace(STAT_END, reversal + "\n" + STAT_END)
        assert stat_verdict(bad, bad)[0], f"selftest: {reversal!r} must fail"
    # the arm's probe on v1.7.0: a THIRD object appended to the clause, identical in both copies
    third = good.replace("paired movements**", "paired movements and ratios**")
    assert stat_verdict(third, third)[0], "selftest: an appended third object must fail"
    # RESIDUAL, STATED RATHER THAN ASSERTED AWAY. A pattern match still cannot read a sentence:
    # "not `B` = **10,000** but 4,000" satisfies the B pattern. STAT_FORBIDDEN covers the reversals
    # seen in this study's own history, not the set of all reversals -- that would be a prose
    # checker, CLAUDE.md's third blindness class. NO ASSERTION IS WRITTEN HERE, because an
    # assertion that cannot fail is the defect this file exists to catch.


def scan_step8_register():
    """Exercise the Step 8 trap register, and FAIL on a row that matches nothing.

    0101, closing R3. These figures lived only in second-brain's memory until now -- a second
    hand-maintained register, the hazard 0059 B3 forbids.

    WHAT THIS CAN AND CANNOT DO. It cannot adjudicate whether a given occurrence names its
    scope: that is prose, and CLAUDE.md's third blindness class. What it CAN do is prove the
    register is LIVE rather than inert, and catch the one failure a trap register has of its
    own -- A ROW THAT MATCHES NOTHING.

    Why a zero-match row must fail: registering a value as legitimate DISARMS the control
    against it (9.6830 was registered while superseded on four surfaces). A row for a figure
    that no longer appears anywhere cannot protect a real reading -- it can only sit there
    waiting to excuse a future coincidence. Dead rows are how a register decays into a
    blanket exemption, which is the shape second-brain found on 703.
    """
    hits, cov = {v: 0 for v in STEP8_LEGITIMATE}, dict(files=0, values=len(STEP8_LEGITIMATE))
    for surface, files in SURFACES.items():
        for f in files:
            if f.endswith((".gz", ".npz", ".npy")):
                continue
            is_json = f.endswith(".json")
            try:
                items = ([v for v, _ in json_numbers(f)] if is_json
                         else [v for v, _, _, _ in text_numbers(f)])
            except Exception:                                       # noqa: BLE001
                continue
            cov["files"] += 1
            for val in items:
                for reg in hits:
                    if near(val, float(reg)):
                        hits[reg] += 1
    return hits, cov


STAMPED: dict = {}


def scan():
    neg, pos, pos_in, allowed, legit_seen = [], {v: set() for v in ADOPTED}, set(), set(), set()
    for surface, files in SURFACES.items():
        for f in files:
            is_json = f.endswith(".json")
            if is_json and f not in STAMPED:
                STAMPED[f] = stamped_field_paths(f)
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
                        # 0123: a sibling stamp that NAMES this field exempts it. Field-scoped,
                        # never object-scoped -- see stamped_field_paths().
                        if is_json and where in STAMPED.get(f, frozenset()):
                            labelled = True
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
        print(f"  [{s}] {show(f)} {where}: {val}  ({what})")
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
            print(f"  {show(f)}: {why}")
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
        print(f"  [{surface}] {show(f)} {where}: {phrase!r}")
        print(f"        {why}")
        print(f"        {text}")
    print()

    _selftest_arm_scope()
    _selftest_statistic_matcher()
    stat_fails, stat_cov = scan_statistic_declaration()
    print("BOOTSTRAP STATISTIC -- 0118, closing reviewer-engineering's E11 (surfaces 2 and 3):")
    print(f"  coverage: {stat_cov['files']}/{len(STAT_WRITERS)} writer files read, "
          f"{stat_cov['chars']} characters compared byte for byte, "
          f"{stat_cov['elements']} fixed elements asserted in each copy")
    if stat_fails:
        for m in stat_fails:
            print(f"  FAIL: {m}")
    else:
        print("  the two arms' declarations are byte-identical and name all four fixed elements: "
              "B = 10,000, seed 20260818, unit = account (0103), statistic = BOTH (0118)")
    print()

    s8_hits, s8_cov = scan_step8_register()
    s8_dead = sorted(v for v, n in s8_hits.items() if n == 0)
    print("STEP 8 TRAP REGISTER -- 0101, closing R3 (these lived only in second-brain's memory):")
    print(f"  coverage: {s8_cov['values']} registered figures x {s8_cov['files']} files; "
          f"occurrences {min(s8_hits.values())}-{max(s8_hits.values())} per figure")
    assert s8_cov["files"] > 0, "STEP 8 REGISTER LOOKED NOWHERE"
    print("  It does NOT adjudicate whether an occurrence names its scope -- that is prose, and "
          "CLAUDE.md's third blindness class. It proves the register is LIVE and catches a DEAD ROW.")
    if s8_dead:
        for v in s8_dead:
            print(f"  DEAD ROW: {v:,} matches nothing on any surface -- {STEP8_LEGITIMATE[v][0][:70]}")
        print("  A row matching nothing cannot protect a real reading; it can only excuse a future "
              "coincidence. Withdraw it or fix the figure.")
    else:
        print("  no dead rows")
    print()

    ss_hits, ss_cov = scan_superseded_strings()
    print("NEEDLE REGISTER ACROSS ALL EIGHT SURFACES -- 0095 F3. *** REPORT ONLY: NOT YET A CONTROL ***")
    print(f"  coverage: {ss_cov['needles']} needles x {ss_cov['files']} files "
          f"({ss_cov['chars']:,} chars, +/-{CHAR_WINDOW}-char marker window); {ss_cov['skipped']} skipped")
    assert ss_cov["files"] > 0 and ss_cov["chars"] > 0, "NEEDLE SCAN LOOKED NOWHERE"
    print(f"  candidate hits: {len(ss_hits)} -- TRIAGE OUTSTANDING, UNREAD, and this scan"
          f" DELIBERATELY DOES NOT FAIL THE RUN.")
    print("  The register was authored for ONE arm's four artifacts. Repo-wide, short needles"
          " ('793', '97.6%', '88 columns') match legitimate HISTORICAL records -- `CLAUDE.md`:"
          " a grep hit is not a defect until you read the line.")
    print("  Failing on unread hits would block the gate on lines nobody has read; narrowing"
          " until it passes is how a control gets disarmed. Neither was done. The triage is an"
          " open item for the Human Lead.")
    for s, f, ln, needle, why, repl in ss_hits[:8]:
        print(f"    [{s}] {f}:{ln}  {needle!r}  ({why})")
    if len(ss_hits) > 8:
        print(f"    ... and {len(ss_hits) - 8} more")
    print()

    have_d, seen_d, missing_d = scan_citations()
    print("CITATION RESOLVER -- every `NNNN` cited on the eight surfaces resolves to decisions/ (0094):")
    print(f"  coverage: {len(seen_d)} distinct entries cited across the surfaces; "
          f"{len(have_d)} entry files on disk")
    assert seen_d, "CITATION RESOLVER FOUND NO CITATIONS -- a resolver that resolves nothing is not clean"
    if missing_d:
        for n in sorted(missing_d):
            print(f"  MISSING decisions/{n}* -- cited in {len(missing_d[n])} file(s): "
                  f"{[show(x) for x in sorted(missing_d[n])[:3]]}")
    else:
        print("  none unresolved")
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
        print(f"  {show(f)}\n      {why}")
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

    if (neg or missing or miss_in or phrase_hits or READ_FAILURES or legit_conflicts
            or missing_d or s8_dead or stat_fails):
        print("\n" + withheld_report())
        print("\nFAIL")
        sys.exit(1)
    print("\n" + withheld_report())
    print("\nPASS -- all halves, all EIGHT surfaces.")
