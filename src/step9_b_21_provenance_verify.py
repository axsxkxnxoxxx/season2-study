#!/usr/bin/env python3
"""Step 9, arm `b` -- PROVENANCE: the consumer COMPARES the producer's identity, and FAILS.

Human Lead ruling 3, 2026-08-25. THE GROUND IS THE CLASS, NOT THE INSTANCE: an artifact that
asserts which script produced it, where nothing checks that the assertion is still current, is A
CLAIM ITS MECHANISM CANNOT DELIVER. This arm publishes `generator`, `generator_sha256_12`,
`source_file`, `source_sha256_12` and `sources[].sha256_12` in six files, and until this script
existed NOT ONE of them was ever compared against the thing it names. A producer could be edited
without being re-run and every consumer and every control in this arm went on exiting 0.

WHAT IT DOES. It reads each recorded claim OUT OF THE FILE THAT MAKES IT -- the producer path
and the hash are both read, never typed here, because a typed expected hash is a second
definition of the producer's identity sitting inside the checker (decisions/0123 SS6d) -- then
hashes the named file and compares. Disagreement is a hard stop.

THREE MODES, AND THE THIRD IS NOT A PASS.
  CURRENT      the claim is made by a LIVE file, so the named producer must still hash to the
               recorded value on disk. A mismatch means the artifact names a producer that no
               longer exists in that form: it must be re-emitted, not re-labelled.
  HISTORICAL   the claim is made by a SETTLED, STAMPED file. Demanding equality with today's
               working tree would condemn a correct record of an earlier build, so the test is
               that the recorded hash is one THE NAMED FILE ACTUALLY HELD -- its current content
               or any revision of it in git. A fabricated or mistyped hash still fails. This is
               a weaker claim than CURRENT and it is labelled as one.
  UNVERIFIABLE the producer is under processed/, which is gitignored, and the recorded hash is
               not the file's current hash. There is NO evidence on this machine that can settle
               it. IT IS COUNTED SEPARATELY AND NEVER COUNTED AS A PASS. A precondition that
               cannot fail on the vector it polices is not a check (decisions/0123 SS3), so this
               script refuses to report such an edge as verified.

WHAT IS DELIBERATELY NOT CHECKED, AND WHY. logs/step9_b_controls_after_rerun.json carries a
`files_after_the_last_edit` map written AFTER every control has run -- including this one. This
script runs inside that control set, so comparing the map inside the same run compares against
the PREVIOUS run's disk state by construction. That is circular, and a check whose outcome is
determined by the order it runs in is not a check. The map is printed as an INFORMATIONAL
currency count, labelled as such, and it does not reach the exit status.

COVERAGE IS PRINTED AND ZERO IS A FAILURE. An empty result and a clean result are the same
value, and only the control knows which it produced.

SCOPE. Every path is this arm's own or a shared input this arm is required to consume (Step 8's
approved artifacts, the adopted rule). No other Step 9 arm's path is read; the file list is
literal and there is no glob that could span arms. Counts and hashes only -- no user data.

Run:  python3 src/step9_b_21_provenance_verify.py          -> verify, exit non-zero on mismatch
      python3 src/step9_b_21_provenance_verify.py --probe  -> drive it to failure, both modes
"""

import hashlib
import io
import json
import os
import re
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEADLINE_LIVE = "artifacts/step9-headline-corrected-2026-08-21-b.json"
HEADLINE_LIVE_MD = "artifacts/step9-headline-corrected-2026-08-21-b.md"
HEADLINE_ORIG = "artifacts/step9-headline-b.json"
HEADLINE_ORIG_MD = "artifacts/step9-headline-b.md"
WORKING_LIVE = "artifacts/step9-working-figures-corrected-2026-08-21-b.json"
WORKING_ORIG = "artifacts/step9-working-figures-b.json"
WEIGHTS_NPZ = "processed/step9/b/boot_weights.npz"
CONTROLS_LOG = "logs/step9_b_controls_after_rerun.json"
OUTLOG = os.path.join(ROOT, "logs", "step9_b_provenance_verify.txt")

CURRENT, HISTORICAL, UNVERIFIABLE = "CURRENT", "HISTORICAL", "UNVERIFIABLE"

REP = io.StringIO()


def w(s=""):
    print(s)
    REP.write(s + "\n")


def sha12_bytes(b):
    return hashlib.sha256(b).hexdigest()[:12]


def sha12(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return sha12_bytes(fh.read())


def exists(rel):
    return os.path.exists(os.path.join(ROOT, rel))


def jget(doc, rel, *keys):
    """Read one key path. NO DEFAULT: a missing key is a hard stop, never an empty claim."""
    node = doc
    for k in keys:
        if isinstance(k, int):
            if not isinstance(node, list) or k >= len(node):
                sys.exit("HARD STOP: %s has no $.%s" % (rel, ".".join(map(str, keys))))
            node = node[k]
        else:
            if not isinstance(node, dict) or k not in node:
                sys.exit("HARD STOP: %s has no $.%s -- a provenance claim that is absent and one "
                         "that is wrong are different defects, and this script must not turn the "
                         "first into a pass." % (rel, ".".join(map(str, keys))))
            node = node[k]
    return node


def load(rel):
    with open(os.path.join(ROOT, rel)) as fh:
        return json.load(fh)


def git_history_hashes(rel):
    """Every distinct content hash the named path has ever had in this repository.

    Path-qualified and `--format=%H` only: no commit message is read (decisions/0125 SS5d).
    Returns None when the path is untracked, which is DIFFERENT from an empty history and must
    stay distinguishable -- an untracked producer is UNVERIFIABLE, not falsified.
    """
    revs = subprocess.run(["git", "-C", ROOT, "log", "--format=%H", "--", rel],
                          capture_output=True, text=True).stdout.split()
    if not revs:
        return None
    out = set()
    for r in revs:
        b = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (r, rel)],
                           capture_output=True)
        if b.returncode == 0:
            out.add(sha12_bytes(b.stdout))
    return out


# =============================================================================================
# THE EDGE REGISTER.
#
# One row per place where a consumer would otherwise take a producer's identity or currency on
# trust. Every row states WHERE THE CLAIM IS MADE, WHAT IT NAMES, and HOW THE NAMED VALUE IS
# READ. The producer path and the hash are BOTH read out of the claiming file: this script types
# neither, so it cannot drift from what the artifact actually says.
# =============================================================================================
SHA_IN_TEXT = re.compile(r"sha256:12 `?([0-9a-f]{12})")


def edges():
    E = []

    def add(eid, claim_in, claim_at, producer, recorded, mode, why):
        E.append({"id": eid, "claim_in": claim_in, "claim_at": claim_at,
                  "producer": producer, "recorded": recorded, "mode": mode, "why": why})

    # -- 1. the bootstrap's own identity, recorded INTO the weight matrix it drew ---------------
    z = np.load(os.path.join(ROOT, WEIGHTS_NPZ))
    for k in ("source_file", "source_sha256_12"):
        if k not in z.files:
            sys.exit("HARD STOP: %s carries no `%s`. The producer recorded no identity, so no "
                     "consumer can compare one." % (WEIGHTS_NPZ, k))
    add("bootstrap_source -> boot_weights.npz", WEIGHTS_NPZ, "source_sha256_12",
        str(z["source_file"]), str(z["source_sha256_12"]), CURRENT,
        "the recorded replicate set is only the one that produced the published endpoints if "
        "the script that drew it is still the script on disk")

    # -- 2/3. the emitter's identity, recorded INTO each headline -------------------------------
    for rel, mode in ((HEADLINE_LIVE, CURRENT), (HEADLINE_ORIG, HISTORICAL)):
        d = load(rel)
        add("emitter -> %s" % os.path.basename(rel), rel, "$.generated_by.generator_sha256_12",
            jget(d, rel, "generated_by", "generator"),
            jget(d, rel, "generated_by", "generator_sha256_12"), mode,
            "the file names the script that wrote it; nothing checked that the name still "
            "resolves to those bytes")

    # -- 4. the promoter's identity, recorded INTO the live headline's provenance note ----------
    d = load(HEADLINE_LIVE)
    note = jget(d, HEADLINE_LIVE, "notes", "step9_b_emission_provenance")
    m = re.search(r"into artifacts/ by (\S+\.py) \(sha256:12 ([0-9a-f]{12})\)", note)
    if not m:
        sys.exit("HARD STOP: $.notes.step9_b_emission_provenance in %s does not state a promoter "
                 "and a hash in the expected form. NO DEFAULT: an unparsed claim is not an "
                 "absent one." % HEADLINE_LIVE)
    add("promoter -> %s" % os.path.basename(HEADLINE_LIVE), HEADLINE_LIVE,
        "$.notes.step9_b_emission_provenance", m.group(1), m.group(2), CURRENT,
        "the promotion note names the script that moved the preview into artifacts/")

    # -- 5..8. the consumed working files, recorded INTO each working-figures extract ------------
    for rel, mode in ((WORKING_LIVE, CURRENT), (WORKING_ORIG, HISTORICAL)):
        d = load(rel)
        srcs = jget(d, rel, "sources")
        for i, s in enumerate(srcs):
            path = jget(s, rel, "path")
            rec = jget(s, rel, "sha256_12")
            eff = mode
            if mode is HISTORICAL and git_history_hashes(path) is None and sha12(path) != rec:
                eff = UNVERIFIABLE
            add("%s -> %s" % (os.path.basename(path), os.path.basename(rel)), rel,
                "$.sources[%d].sha256_12" % i, path, rec, eff,
                "the extract states the hash of the working file each figure was read from")

    # -- 9..N. the declared INPUTS of each headline ---------------------------------------------
    for rel, mode in ((HEADLINE_LIVE, CURRENT), (HEADLINE_ORIG, HISTORICAL)):
        d = load(rel)
        for i, line in enumerate(jget(d, rel, "generated_by", "inputs")):
            hits = SHA_IN_TEXT.findall(line)
            if not hits:
                continue
            path = line.split(" ")[0]
            add("input %s -> %s" % (os.path.basename(path), os.path.basename(rel)), rel,
                "$.generated_by.inputs[%d]" % i, path, hits[0], mode,
                "the emission states the hash of the upstream artifact it consumed")
        rec = jget(d, rel, "adopted_rule_revision", "source_sha256_12")
        path = jget(d, rel, "adopted_rule_revision", "source_file")
        eff = mode
        if git_history_hashes(path) is None and sha12(path) != rec:
            eff = UNVERIFIABLE
        add("adopted_rule -> %s" % os.path.basename(rel), rel,
            "$.adopted_rule_revision.source_sha256_12", path, rec, eff,
            "the revision is READ not typed, and the file it was read from is named with its "
            "hash at read time")

    # -- the controls run record's own identity --------------------------------------------------
    if exists(CONTROLS_LOG):
        d = load(CONTROLS_LOG)
        add("controls -> %s" % os.path.basename(CONTROLS_LOG), CONTROLS_LOG,
            "$.generator_sha256_12", jget(d, CONTROLS_LOG, "generator"),
            jget(d, CONTROLS_LOG, "generator_sha256_12"), CURRENT,
            "the run record names the script that captured it")

    return E


def check(e):
    """Compare one edge. Returns (verdict, observed, detail)."""
    if not exists(e["producer"]):
        return "FAIL", "MISSING", "the claim names a file that is not on disk"
    obs = sha12(e["producer"])
    if e["mode"] == CURRENT:
        return ("OK" if obs == e["recorded"] else "FAIL"), obs, "must equal the file on disk"
    if e["mode"] == HISTORICAL:
        hist = git_history_hashes(e["producer"])
        pool = ({obs} | hist) if hist else {obs}
        return ("OK" if e["recorded"] in pool else "FAIL"), obs, \
               "must be a hash the file actually held (%d revision(s) + current)" % (
                   len(hist) if hist else 0)
    return "UNVERIFIABLE", obs, ("producer is under processed/, which is gitignored, and the "
                                 "recorded hash is not its current one -- no evidence on this "
                                 "machine can settle it")


# =============================================================================================
# THE MD RESTATEMENT. artifacts/step9-headline-*.md prints the generator and its hash, read out
# of the JSON by src/step9_b_4_md.py. That is a SECOND COPY of the claim, and two copies of one
# figure is this study's most frequent defect, so the copy is compared against the original.
# =============================================================================================
def md_edges():
    out = []
    for md, js in ((HEADLINE_LIVE_MD, HEADLINE_LIVE), (HEADLINE_ORIG_MD, HEADLINE_ORIG)):
        txt = open(os.path.join(ROOT, md)).read()
        m = re.search(r"\*\*Generated\*\*[^\n]*?by `([^`]+)` \(sha256:12 `([0-9a-f]{12})`\)", txt)
        if not m:
            sys.exit("HARD STOP: %s states no generator and hash in the expected form. The .md "
                     "is a published surface; an unparsed provenance line is a defect, not an "
                     "absence." % md)
        d = load(js)
        out.append({"md": md, "json": js, "md_gen": m.group(1), "md_sha": m.group(2),
                    "js_gen": jget(d, js, "generated_by", "generator"),
                    "js_sha": jget(d, js, "generated_by", "generator_sha256_12")})
    return out


def run_verify():
    w("=" * 94)
    w("STEP 9, ARM b -- PROVENANCE VERIFICATION (Human Lead ruling 3, 2026-08-25)")
    w("=" * 94)
    w("")
    w("Every recorded producer identity in this arm's own outputs, COMPARED against the file it")
    w("names. Nothing here is typed: the producer path and the hash are both read out of the")
    w("claiming file, so this script cannot drift from what the artifact says.")
    w("")

    E = edges()
    w("-" * 94)
    w("1. PRODUCER-IDENTITY EDGES")
    w("-" * 94)
    w("")
    w("%-46s %-12s %-13s %-13s %s" % ("edge", "mode", "recorded", "observed", "verdict"))
    fails, counts = [], {CURRENT: 0, HISTORICAL: 0, UNVERIFIABLE: 0}
    for e in E:
        verdict, obs, detail = check(e)
        counts[e["mode"]] += 1
        w("%-46s %-12s %-13s %-13s %s"
          % (e["id"][:46], e["mode"], e["recorded"], obs, verdict))
        if verdict == "FAIL":
            fails.append((e, obs, detail))
            w("    CLAIM  : %s at %s" % (e["claim_in"], e["claim_at"]))
            w("    NAMES  : %s" % e["producer"])
            w("    DETAIL : %s" % detail)
        elif verdict == "UNVERIFIABLE":
            w("    NOT A PASS: %s" % detail)
    w("")
    w("    edges          : %d" % len(E))
    w("    CURRENT        : %d   (must equal the file on disk)" % counts[CURRENT])
    w("    HISTORICAL     : %d   (settled file; must be a hash the producer actually held)"
      % counts[HISTORICAL])
    w("    UNVERIFIABLE   : %d   (counted, NEVER counted as a pass)" % counts[UNVERIFIABLE])
    w("    failures       : %d" % len(fails))
    w("")

    w("-" * 94)
    w("2. SAME-RUN CORROBORATION -- THE TWO OUTPUTS OF ONE PRODUCER, AGAINST EACH OTHER")
    w("-" * 94)
    w("")
    w("    src/step9_b_2_bootstrap.py writes the design block into stage2_bootstrap.json and the")
    w("    manifest into boot_weights.npz in ONE run. If either is re-run and the other is not,")
    w("    they describe different draws. THIS IS A COMPARISON AGAINST THE SOURCE, NOT A RANGE:")
    w("    a window like `0 < B <= 100000` would pass on every wrong value it could hold, and a")
    w("    precondition that cannot fail on the vector it polices is not a check (0123 SS3).")
    w("")
    z = np.load(os.path.join(ROOT, WEIGHTS_NPZ))
    s2 = load("processed/step9/b/stage2_bootstrap.json")
    corro = [("B", int(z["B"]), jget(s2, "stage2_bootstrap.json", "design", "B")),
             ("seed", int(z["seed"]), jget(s2, "stage2_bootstrap.json", "design", "seed")),
             ("n_frame", int(z["n_frame"]),
              jget(s2, "stage2_bootstrap.json", "design", "resampling_frame_n"))]
    corro_bad = 0
    w("    %-14s %-18s %-18s %s" % ("element", "boot_weights.npz", "stage2 design", "verdict"))
    for name, a, b in corro:
        ok = a == b
        corro_bad += (not ok)
        w("    %-14s %-18s %-18s %s" % (name, a, b, "AGREE" if ok else "DISAGREE"))
    w("")
    w("    elements corroborated : %d" % len(corro))
    w("    disagreements         : %d" % corro_bad)
    w("")

    w("-" * 94)
    w("3. THE .md RESTATEMENT OF THE .json's CLAIM")
    w("-" * 94)
    w("")
    md_bad = 0
    for r in md_edges():
        ok = (r["md_gen"] == r["js_gen"] and r["md_sha"] == r["js_sha"])
        md_bad += (not ok)
        w("    %-52s %s" % (os.path.basename(r["md"]), "MATCHES its JSON" if ok else "DIVERGES"))
        w("        .md  says %s (sha256:12 %s)" % (r["md_gen"], r["md_sha"]))
        w("        .json says %s (sha256:12 %s)" % (r["js_gen"], r["js_sha"]))
    w("")
    w("    restatements compared : %d" % len(md_edges()))
    w("    divergences           : %d" % md_bad)
    w("")

    w("-" * 94)
    w("4. INFORMATIONAL -- NOT A CHECK, AND NOT IN THE EXIT STATUS")
    w("-" * 94)
    w("")
    if exists(CONTROLS_LOG):
        m = jget(load(CONTROLS_LOG), CONTROLS_LOG, "files_after_the_last_edit")
        agree = sum(1 for k, v in m.items() if exists(k) and sha12(k) == v)
        w("    logs/…controls_after_rerun.json `files_after_the_last_edit`: %d/%d still current"
          % (agree, len(m)))
        w("    THIS IS NOT SCORED. That map is written AFTER every control in the set has run,")
        w("    and this script runs inside that set, so it necessarily compares against the")
        w("    PREVIOUS run's disk state. A check whose outcome is fixed by the order it runs")
        w("    in is not a check, and reporting it as one would be the defect this ruling names.")
    else:
        w("    no controls run record on disk yet -- nothing to report, and this is stated")
        w("    rather than passed over silently.")
    w("")

    if len(E) == 0 or len(md_edges()) == 0:
        w("HARD STOP: zero edges. An empty result and a clean result are the same value.")
        return 2
    w("=" * 94)
    if fails or md_bad or corro_bad:
        w("RESULT: %d producer-identity failure(s), %d same-run disagreement(s), %d "
          "restatement divergence(s)." % (len(fails), corro_bad, md_bad))
        w("A file naming a producer that no longer hashes to the recorded value must be")
        w("RE-EMITTED by that producer, never re-labelled by hand (CLAUDE.md, artifact sign-off).")
        w("=" * 94)
        return 1
    w("RESULT: every producer identity this arm records resolves to the file it names.")
    w("=" * 94)
    return 0


# =============================================================================================
# THE PROBE. A guard shown only passing has not been shown to discriminate (decisions/0123 SS3).
# The mutation is done IN MEMORY on the bytes, never on disk: an on-disk probe that crashed
# would leave a producer edited and un-re-run, which is the exact state this script exists to
# detect. The end-to-end on-disk demonstration -- a pre-existing consumer ACCEPTING a stale
# producer, and this script REJECTING it -- is src/step9_b_22_stale_producer_repro.py.
# =============================================================================================
def run_probe():
    w("=" * 94)
    w("STEP 9, ARM b -- PROVENANCE VERIFICATION, DRIVEN TO FAILURE")
    w("=" * 94)
    w("")
    E = edges()
    cur = [e for e in E if e["mode"] == CURRENT]
    his = [e for e in E if e["mode"] == HISTORICAL]
    if not cur or not his:
        w("HARD STOP: the probe found no edge of one of the two scored modes (CURRENT=%d, "
          "HISTORICAL=%d). A probe with nothing to drive is not a probe." % (len(cur), len(his)))
        return 2

    def compare(mode, recorded, producer_bytes, hist):
        obs = sha12_bytes(producer_bytes)
        if mode == CURRENT:
            return "OK" if obs == recorded else "FAIL"
        return "OK" if recorded in ({obs} | (hist or set())) else "FAIL"

    def fabricate(h):
        """One hex digit changed -- a hash no file in this repository has ever had."""
        return ("0" if h[0] != "0" else "1") + h[1:]

    # THE TWO MODES ARE PROBED ON DIFFERENT VECTORS, BECAUSE THEY MAKE DIFFERENT CLAIMS.
    #   CURRENT says "the producer on disk is still this one", so the vector that must be
    #     rejected is A MUTATED PRODUCER -- one edit and not re-run.
    #   HISTORICAL says "this is a hash the producer actually held", which a later edit does NOT
    #     falsify, so mutating the producer must NOT reject it and doing so would mean the mode
    #     is CURRENT under another name. The vector it must reject is A FABRICATED HASH.
    # Probing HISTORICAL with the CURRENT vector would show it "failing" for the wrong reason,
    # which is a probe that passes without testing the claim.
    rows, bad = [], 0
    for e in cur[:3] + his[:3]:
        real = open(os.path.join(ROOT, e["producer"]), "rb").read()
        mutated = real + b"\n# provenance probe\n"
        hist = git_history_hashes(e["producer"]) if e["mode"] == HISTORICAL else None
        v_real = compare(e["mode"], e["recorded"], real, hist)
        v_mut = compare(e["mode"], e["recorded"], mutated, hist)
        v_fab = compare(e["mode"], fabricate(e["recorded"]), real, hist)
        want_mut = "FAIL" if e["mode"] == CURRENT else "OK"
        ok = (v_real == "OK" and v_mut == want_mut and v_fab == "FAIL")
        bad += (not ok)
        rows.append((e["id"][:38], e["mode"], v_real, v_mut, v_fab,
                     "as required" if ok else "PROBE FAILED"))
    w("A single appended comment byte-string is enough for the CURRENT vector: the check is on")
    w("the CONTENT, so an edit that does not change the output still changes the identity --")
    w("which is the point. A producer edited and not re-run no longer matches what its own")
    w("output says produced it.")
    w("")
    w("%-40s %-11s %-10s %-16s %-10s %s"
      % ("edge", "mode", "real", "producer mutated", "hash faked", "verdict"))
    for r in rows:
        w("%-40s %-11s %-10s %-16s %-10s %s" % r)
    w("")
    w("    probes run        : %d" % len(rows))
    w("    behaved as required: %d" % (len(rows) - bad))
    w("")
    w("    READING: CURRENT accepts the real producer and REJECTS it after one appended comment.")
    w("             HISTORICAL is the weaker claim and the probe shows it is still a claim: it")
    w("             SURVIVES a later edit to the producer, by design, and REJECTS a hash the")
    w("             file never held. Each mode is driven on the vector its own claim polices.")
    w("")
    w("=" * 94)
    if bad:
        w("RESULT: %d probe(s) did not behave as required. A comparison that cannot separate a "
          "mutated producer from the real one establishes nothing." % bad)
        w("=" * 94)
        return 1
    w("RESULT: the comparison discriminates in both scored modes.")
    w("=" * 94)
    return 0


def main():
    probe = "--probe" in sys.argv[1:]
    code = run_probe() if probe else run_verify()
    with open(OUTLOG if not probe else OUTLOG.replace(".txt", "_probe.txt"), "w") as fh:
        fh.write(REP.getvalue())
    print("\nrun record: logs/%s" % os.path.basename(
        OUTLOG if not probe else OUTLOG.replace(".txt", "_probe.txt")))
    return code


if __name__ == "__main__":
    sys.exit(main())
