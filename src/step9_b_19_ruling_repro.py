#!/usr/bin/env python3
"""Step 9, arm `b` -- REPRODUCTION of the three findings ruled on 2026-08-25.

REPRODUCE BEFORE FIX. Each of the three rulings names a defect in THIS ARM'S OWN work, and a
fix whose defect was never demonstrated is a change, not a correction. So each is measured
here, from the files on disk, and each measurement is one a reader can re-run.

  R1  TWELVE MEASURED INTERVALS REACH NO ARTIFACT. processed/step9/b/stage2_bootstrap.json
      carries `levels_position_5_pct` for every (arm setting, population, outcome state) --
      2 x 2 x 3 = 12 intervals, 24 endpoints. The check searches all three emitted artifacts
      for each endpoint's value and reports how many are found.

      IT IS SHOWN REJECTING AS WELL AS ACCEPTING. The same search is run for
      `levels_post_liveness_pct`, whose 24 endpoints ARE published inside `$...shares[].ci`.
      A searcher that found nothing because it looked in the wrong place would report zero for
      BOTH families, and the two families are the discriminator (decisions/0123 SS3: a check
      that cannot fail on the vector it polices is not a check).

  R2  THREE INHERITED LEAVES ARE FALSE IN A NON-PLACEHOLDER FILE. Each is compared BYTE FOR
      BYTE against artifacts/step8b-placeholder-arm-file.json at the same path -- establishing
      that it is inherited and not written -- and then evaluated against the emitted file
      itself, which is what makes it false.

  R3  A TYPED POPULATION CONSTANT. src/step9_b_3_emit.py holds `NPOP = {...}` as a literal.
      The check reads the same two figures out of Step 8's approved waterfall artifacts and
      reports whether a literal is present in the source.

Run:  python3 src/step9_b_19_ruling_repro.py        (exit 0 = every finding measured)
      python3 src/step9_b_19_ruling_repro.py --after (the same measurements, expecting the
                                                      corrected state; exit 1 if not reached)

SCOPE. Reads this arm's own files, Step 8's approved artifacts and the shared schema
placeholder. No arm-`a` path is opened and every path is a literal -- there is no glob that
could span arms.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AFTER = "--after" in sys.argv

STAGE2 = os.path.join(ROOT, "processed/step9/b/stage2_bootstrap.json")
EMITTED = [
    "artifacts/step9-headline-corrected-2026-08-21-b.json",
    "artifacts/step9-headline-corrected-2026-08-21-b.md",
    "artifacts/step9-working-figures-corrected-2026-08-21-b.json",
]
TEMPLATE = os.path.join(ROOT, "artifacts/step8b-placeholder-arm-file.json")
EMITTER = os.path.join(ROOT, "src/step9_b_3_emit.py")
HEADLINE = os.path.join(ROOT, EMITTED[0])

STATES = ("never_started", "started_and_left", "continued")
SETTINGS = ("W108_s2_finale", "W91_s2_premiere")
POPS = ("APPLY", "DERIV")

fail = []


def blob():
    parts = []
    for rel in EMITTED:
        parts.append(open(os.path.join(ROOT, rel)).read())
    return "\n".join(parts)


def numbers_in(text):
    return {m.group(0).replace(",", "") for m in re.finditer(r"-?\d[\d,]*\.?\d*", text)}


def found(value, pool, text):
    """A float endpoint counts as published if its exact repr appears, or its 4-dp rendering."""
    if repr(value) in pool:
        return True
    return ("%.4f" % value) in pool


print("=" * 92)
print("STEP 9 ARM b -- REPRODUCTION OF THE THREE FINDINGS RULED 2026-08-25   (%s)"
      % ("AFTER the fix" if AFTER else "BEFORE the fix"))
print("=" * 92)

s2 = json.load(open(STAGE2))
text = blob()
pool = numbers_in(text)

# ---------------------------------------------------------------------------------------- R1
print("\nR1  TWELVE MEASURED INTERVALS AND WHERE THEY REACH")
print("-" * 92)
tally = {}
for family in ("levels_position_5_pct", "levels_post_liveness_pct"):
    hit = miss = 0
    missing = []
    for key in SETTINGS:
        for pop in POPS:
            for st in STATES:
                node = s2[key][pop][family][st]
                for end in ("lower", "upper"):
                    if found(node[end], pool, text):
                        hit += 1
                    else:
                        miss += 1
                        missing.append("%s.%s.%s.%s.%s = %r" % (key, pop, family, st, end,
                                                                node[end]))
    tally[family] = (hit, miss, missing)
    print("    %-26s  intervals 12   endpoints 24   FOUND %2d   ABSENT %2d"
          % (family, hit, miss))
if tally["levels_position_5_pct"][1] and not tally["levels_post_liveness_pct"][1]:
    print("\n    THE SEARCH DISCRIMINATES: it finds every post-liveness endpoint and misses")
    print("    every position-5 one, so the absence is the file's and not the searcher's.")
for m in tally["levels_position_5_pct"][2][:4]:
    print("        ABSENT  %s" % m)
if tally["levels_position_5_pct"][2]:
    print("        ... %d absent in total" % len(tally["levels_position_5_pct"][2]))
print("\n    COVERAGE: %d endpoint(s) searched across %d artifact(s), %d numeric token(s) in "
      "the pool." % (2 * len(tally) * 24 // 2, len(EMITTED), len(pool)))
if AFTER and tally["levels_position_5_pct"][1]:
    fail.append("R1: %d position-5 endpoints still reach no artifact"
                % tally["levels_position_5_pct"][1])
if not AFTER and not tally["levels_position_5_pct"][1]:
    fail.append("R1 DID NOT REPRODUCE: the position-5 endpoints are already published")

# ---------------------------------------------------------------------------------------- R2
print("\nR2  THREE INHERITED LEAVES, IN A FILE WHOSE `placeholder` FLAG IS FALSE")
print("-" * 92)
doc = json.load(open(HEADLINE))
tpl = json.load(open(TEMPLATE))
# THE THREE LEAVES THE RULING NAMES, PLUS THE ONE THAT LOOKS LIKE A FOURTH AND IS NOT.
# `expect` is what a file whose `placeholder` flag is FALSE must do with the leaf.
SITES = [
    ("$.notes.reading_a_placeholder", ("notes", "reading_a_placeholder"), "OVERRIDE",
     "T1 SELF-REFERENCE: asserts THIS FILE's placeholder flag is true, and it is false."),
    ("$.notes.a_ci_endpoints_type_follows_its_statistic",
     ("notes", "a_ci_endpoints_type_follows_its_statistic"), "OVERRIDE",
     "T1 SELF-REFERENCE, AND THE TYPE-FIXTURE CLAIM: says the movement branch is occupied "
     "'in this file' by a DECLARED TYPE FIXTURE, where this file holds twelve real movement "
     "measurements, six with a negative endpoint, and no fixture. THIS IS THE STRING "
     "decisions/0127 SS3 FLAGGED AS *MOVED* AND WHOSE TRUTH-VALUE WAS NEVER CHECKED."),
    ("$.notes.bootstrap_is_fixed", ("notes", "bootstrap_is_fixed"), "OVERRIDE",
     "T2 SELF-CONTRADICTION: states a FOUR-element count where $.bootstrap_settings.b_default "
     "lists seven fields, six lines away in the emitted JSON."),
    ("$.sentinels.type_fixture_rule", ("sentinels", "type_fixture_rule"), "KEEP",
     "T3 SPEC TEXT, AND IT IS THE ONE THAT LOOKS LIKE A FOURTH. It states the SCHEMA's fixture "
     "convention -- that a fixture may appear ONLY in a placeholder -- and says nothing about "
     "this file. It is KEPT VERBATIM: rewriting it would put a second definition of the "
     "schema's convention inside an arm file, and it is the text a reader uses to CONFIRM that "
     "this file declares no fixture rather than take it on trust."),
]
print("    $.placeholder = %r   (a file flagged as real data)" % doc["placeholder"])
n_fixtures = len(re.findall(r'"is_type_fixture"\s*:\s*true', json.dumps(doc)))
n_mv = len([e for e in doc["declared_intervals"] if e["ci"]["statistic"] == "movements"])
n_neg = len([e for e in doc["declared_intervals"] if e["ci"]["statistic"] == "movements"
             and (e["ci"]["lower"] < 0 or e["ci"]["upper"] < 0)])
n_fixed = len(doc["bootstrap_settings"]["b_default"]["fields_fixed_in_spec"])
print("    declared type fixtures in this file          : %d" % n_fixtures)
print("    real movement intervals / with a negative end: %d / %d" % (n_mv, n_neg))
print("    $.bootstrap_settings.b_default fields fixed  : %d" % n_fixed)
print()
for path, (a, b), expect, what in SITES:
    mine = doc[a][b]
    theirs = tpl.get(a, {}).get(b)
    inherited = (mine == theirs)
    print("    %-48s  expect %-8s  inherited byte-for-byte: %s"
          % (path, expect, "YES" if inherited else "no -- rewritten"))
    print("        %s" % what)
    if not AFTER and not inherited:
        fail.append("R2 DID NOT REPRODUCE at %s: it is not the inherited string" % path)
    if AFTER and expect == "OVERRIDE" and inherited:
        fail.append("R2: %s is ruled OVERRIDE and is still the inherited string" % path)
    if AFTER and expect == "KEEP" and not inherited:
        fail.append("R2: %s is ruled KEEP and was rewritten. T3 says the schema's own "
                    "convention text is not an arm's to restate." % path)
if AFTER:
    for path, (a, b), expect, _ in SITES:
        if expect != "OVERRIDE":
            continue
        v = doc[a][b]
        if "This file's flag is true" in v:
            fail.append("R2: %s still asserts the flag is true" % path)
        if "occupied in this file by a DECLARED TYPE FIXTURE" in v:
            fail.append("R2: %s still claims a declared type fixture in this file" % path)
        if re.search(r"(?i)\ball four elements\b", v):
            fail.append("R2: %s still states a four-element count" % path)

# ---------------------------------------------------------------------------------------- R3
print("\nR3  THE TYPED POPULATION CONSTANT")
print("-" * 92)
src = open(EMITTER).read()
literal = re.search(r'^NPOP\s*=\s*\{[^}]*\d{5,}[^}]*\}', src, re.M)
print("    src/step9_b_3_emit.py carries a typed NPOP literal : %s"
      % ("YES -- %r" % literal.group(0) if literal else "no"))
w8b = json.load(open(os.path.join(ROOT, "artifacts/step8-waterfall-b.json")))
w8a = json.load(open(os.path.join(ROOT, "artifacts/step8-waterfall-a.json")))
for pop in POPS:
    rb = [r for r in w8b["waterfall_" + pop] if r["position"] == 5]
    ra = w8a["waterfall"][pop]["position_5_right_censoring"]
    print("    %-6s position-5: step8-waterfall-b %s / step8-waterfall-a %s / declared at "
          "$.arms[0].headline.%s.n_position_5 %s"
          % (pop, format(rb[0]["retained_pairs"], ","), format(ra, ","), pop,
             format(doc["arms"][0]["headline"][pop]["n_position_5"], ",")))
if not AFTER and not literal:
    fail.append("R3 DID NOT REPRODUCE: no typed NPOP literal in the emitter")
if AFTER and literal:
    fail.append("R3: the emitter still types NPOP")

# ------------------------------------------------------------------- R3, the negative control
# A PRECONDITION THAT CANNOT FAIL ON THE VECTOR IT POLICES IS NOT A CHECK (decisions/0123 SS3).
# The read replaces a literal with a value taken from Step 8 arm b's waterfall and REQUIRED to
# equal Step 8 arm a's at the same position on the same population -- set membership against the
# source, not a plausibility window. A window test would pass on any number of the right
# magnitude; this one is driven to failure here and shown NAMING the disagreement.
#
# The emitter is imported with its output directory repointed at a scratch directory, so the
# import writes nothing into the repository. Same technique as src/step9_b_17_ordering_repro.py.
if AFTER:
    print("\nR3-NEG  THE READ'S OWN CHECK, DRIVEN TO FAILURE")
    print("-" * 92)
    import copy
    import tempfile
    os.environ["STEP9_B_OUTDIR"] = tempfile.mkdtemp(prefix="step9b-npop-negctl-")
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import step9_b_3_emit as E                                              # noqa: E402
    cases = [
        ("arm a disagrees with arm b by one pair",
         lambda: E.step8_population(
             "APPLY", 5,
             _w8a=(lambda d: (d["waterfall"]["APPLY"].__setitem__(
                 "position_5_right_censoring", 196653), d)[1])(
                     copy.deepcopy(E.w8a)))),
        ("arm b's waterfall has no position 5",
         lambda: E.step8_population(
             "APPLY", 5,
             _w8b={"waterfall_APPLY": [r for r in E.w8b["waterfall_APPLY"]
                                       if r["position"] != 5]})),
        ("arm b's waterfall carries position 5 twice",
         lambda: E.step8_population(
             "APPLY", 5,
             _w8b={"waterfall_APPLY": E.w8b["waterfall_APPLY"]
                   + [dict(E.w8b["waterfall_APPLY"][4])]})),
        ("arm a's artifact has no waterfall block",
         lambda: E.step8_population("APPLY", 5, _w8a={})),
    ]
    for what, fn in cases:
        try:
            got = fn()
            print("    %-46s ACCEPTED %r  <-- THE CHECK DID NOT FIRE" % (what, got))
            fail.append("R3-NEG: the read accepted a source that is wrong -- %s" % what)
        except SystemExit as exc:
            print("    %-46s REJECTED: %s" % (what, str(exc).split(".")[0][:110]))
    try:
        ok = E.step8_population("APPLY", 5)
        print("    %-46s ACCEPTED %s   <-- and it must, or the rejections mean nothing"
              % ("the UNMUTATED source", format(ok, ",")))
    except SystemExit as exc:
        print("    the UNMUTATED source was REJECTED: %s" % exc)
        fail.append("R3-NEG: the read rejects the real source")

# ------------------------------------------------------------------- R1, the negative control
# THE EMISSION-COMPLETENESS GUARD, SHOWN REJECTING. Ruling 1 exists because twelve measured
# intervals reached no artifact and NOTHING COULD SEE IT -- the validator returns ok on a file
# that omits them, because a schema checks what is in a file and cannot check what a writer
# never put there. So the emitter now carries a guard, and a guard shown only passing has not
# been shown to discriminate (decisions/0123 SS3).
#
# THE MUTATED EMITTER IS DERIVED IN MEMORY AND NEVER WRITTEN TO DISK. The mutation is exactly
# the pre-ruling behaviour: drop the twelve position-5 level intervals immediately before the
# guard runs. Its output directory is repointed at a scratch directory, so nothing in the
# repository is touched by either the mutated run or the unmutated one.
if AFTER:
    print("\nR1-NEG  THE EMISSION-COMPLETENESS GUARD, DRIVEN TO FAILURE")
    print("-" * 92)
    import tempfile
    EMITTER_SRC = open(EMITTER).read()
    ANCHOR = "# EVERY MEASURED INTERVAL IS PUBLISHED, AND THAT IS ASSERTED"
    if ANCHOR not in EMITTER_SRC:
        print("    the guard's anchor is gone from the emitter -- the probe cannot aim at it")
        fail.append("R1-NEG: the emission-completeness guard's anchor is not in the emitter")
    else:
        drop = ('declared = [x for x in declared '
                'if not x["interval_id"].startswith("level_position5_")]\n'
                'doc["declared_intervals"] = declared\n')
        mutated = EMITTER_SRC.replace(ANCHOR, drop + ANCHOR, 1)
        for label, code in (("UNMUTATED", EMITTER_SRC), ("MUTATED -- the twelve withheld",
                                                         mutated)):
            os.environ["STEP9_B_OUTDIR"] = tempfile.mkdtemp(prefix="step9b-completeness-")
            ns = {"__name__": "__step9b_negctl__", "__file__": EMITTER}
            try:
                exec(compile(code, EMITTER, "exec"), ns)
                print("    %-32s ACCEPTED" % label)
                if label.startswith("MUTATED"):
                    fail.append("R1-NEG: the emitter accepted a document withholding twelve "
                                "measured intervals -- the guard did not fire")
            except SystemExit as exc:
                print("    %-32s REJECTED: %s" % (label, str(exc)[:150]))
                if label == "UNMUTATED":
                    fail.append("R1-NEG: the emitter rejects its own real document")

print("\n" + "=" * 92)
if fail:
    for f in fail:
        print("  FAIL  %s" % f)
    print("  VERDICT: NOT IN THE %s STATE" % ("CORRECTED" if AFTER else "DEFECTIVE"))
    sys.exit(1)
print("  VERDICT: all three findings measured, in the %s state."
      % ("corrected" if AFTER else "defective"))
