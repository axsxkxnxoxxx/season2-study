#!/usr/bin/env python3
"""Step 9, arm b -- EMIT the corrected premiere-anchored figures into artifacts/.

Human Lead ruling, 2026-08-21: *STAMP, DO NOT DELETE.* The committed premiere
figures are SUPERSEDED, not withdrawn -- correctly produced under a defective
vector, and the record of what the defect produced is the evidence for the
finding. So both must exist: the marked originals at their own paths, and this
corrected emission beside them.

WHAT THIS SCRIPT DOES, AND WHAT IT REFUSES TO DO
------------------------------------------------
It PROMOTES processed/step9/b/preview/ into artifacts/ under distinct filenames
and adds, to each file, a supersession record, an arm signature and its own
provenance. It CHANGES NO MEASUREMENT. That is asserted rather than claimed: the
promoted JSON is compared leaf-for-leaf against its source and the run stops if
anything other than the added keys differs.

THE FILENAMES, and why they are these
-------------------------------------
    artifacts/step9-headline-corrected-2026-08-21-b.json
    artifacts/step9-headline-corrected-2026-08-21-b.md
    artifacts/step9-working-figures-corrected-2026-08-21-b.json

1. They are DISTINCT from the committed paths, so the marked originals keep
   theirs and the two are readable side by side. That is the ruling's own
   requirement.
2. The ARM TOKEN STAYS LAST. This arm's isolation rule (decisions/0123) requires
   every search to be scoped in the pattern itself, and names
   ``artifacts/step9-*-b.*`` as the scope. A name like
   ``step9-headline-b-corrected-...`` would fall OUTSIDE that pattern, so this
   arm's own scoped searches would silently miss its own corrected figures --
   and a filename that defeats the isolation control is a defect, not a
   cosmetic choice.
3. "corrected" plus the EMISSION DATE says what the file is without asserting
   that it is adopted. Adoption is the Human Lead's, not an arm's.

SECOND AUTHORISED RERUN, 2026-08-21 (Human Lead rulings 1 and 2 of that date).
  RULING 1. The previous corrected emission asserted that the un-re-censored row
  set had been "CHECKED rather than assumed" after the boolean that checked it was
  removed as vacuous. A claim of having checked is either TRUE or it is REMOVED,
  and softening it was excluded. This arm RECOMPUTED it: T0PRIME-ORDER now runs in
  the pipeline, raises, and is demonstrated FAILING on the defective vector. The
  claim is emitted by a script, so it was fixed in the script and the arm re-run --
  never by editing the file.
  RULING 2. This document now carries a DISTINCT INSTANCE VALUE in $.document_scope,
  so it and the file it supersedes are distinguishable. It states nothing about what
  a merge should take: that contract is Step 13b's, and Step 13b is the Human Lead's.
  The superseded file's $.document_scope is not touched.

Run:  python3 src/step9_b_7_emit_corrected.py
"""

import datetime
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SRC_HEADLINE = os.path.join(ROOT, "processed", "step9", "b", "preview", "step9-headline-b.json")
SRC_MD = os.path.join(ROOT, "processed", "step9", "b", "preview", "step9-headline-b.md")
SRC_WORKING = os.path.join(ROOT, "processed", "step9", "b", "preview", "step9-working-figures-b.json")

OUT_HEADLINE = os.path.join(ROOT, "artifacts", "step9-headline-corrected-2026-08-21-b.json")
OUT_MD = os.path.join(ROOT, "artifacts", "step9-headline-corrected-2026-08-21-b.md")
OUT_WORKING = os.path.join(ROOT, "artifacts", "step9-working-figures-corrected-2026-08-21-b.json")

SUPERSEDED_HEADLINE = "artifacts/step9-headline-b.json"
SUPERSEDED_MD = "artifacts/step9-headline-b.md"
SUPERSEDED_WORKING = "artifacts/step9-working-figures-b.json"

WHAT = ("This emission supersedes the PREMIERE-ANCHORED 91-day arm of %s, %s and %s -- and "
        "ONLY that arm. The adopted W108_s2_finale arm is unchanged: it was verified "
        "leaf-for-leaf identical and its harness control reproduces, so nothing about it is "
        "superseded and it is not marked in those files."
        % (SUPERSEDED_HEADLINE, SUPERSEDED_MD, SUPERSEDED_WORKING))

WHY = ("src/step9_b_1_compute.py converted the premiere-anchored T0 column to epoch seconds "
       "with prem.astype('int64') // 10 ** 9. The column's dtype is datetime64[us, UTC], so "
       "its integer view is MICROseconds; dividing by 10 ** 9 produced epoch-seconds / 1000 -- "
       "a 1970 date -- for every pair, in every entry, on both populations. The superseded "
       "figures were CORRECTLY COMPUTED from that vector and are kept, marked at each point of "
       "use, as the record of what the defect produced. src/step9_b_0_clock.py now reads the "
       "resolution off the dtype and cross-checks the cast elementwise; an unrecognised "
       "resolution is a hard stop, not a default.")

SIGNATURE = ("SIGNED OFF BY THE PRODUCING ARM. This arm attests that every figure in this file "
             "was produced by its own pipeline at the settings recorded beside it, and that "
             "this emission is byte-identical in every measurement to "
             "processed/step9/b/preview/, which is what this arm's corrected run wrote. No "
             "figure in this file was hand-entered and none was edited after emission.")

DOCUMENT_INSTANCE = "step9-b-corrected-2026-08-21"

NOT_A_SECOND_ARM = (
    "THIS IS NOT A SECOND ARM FILE. It is arm b's corrected emission of arm b's own document, "
    "and $.document_scope.arm is 'b' in both it and the file it supersedes. A merge that globbed "
    "artifacts/step9-headline-*.json on the arm field alone would pick up BOTH and could read "
    "them as two arms. THIS DOCUMENT THEREFORE CARRIES A DISTINCT INSTANCE VALUE -- "
    "'DOCUMENT INSTANCE: " + DOCUMENT_INSTANCE + "', at $.document_scope.note -- so the "
    "superseded file and this one are DISTINGUISHABLE rather than interchangeable. THAT IS ALL "
    "IT DOES: it makes the two tellable apart and states nothing about which a merge takes. "
    "The merge's input contract is Step 13b's, and Step 13b is the Human Lead's; an arm does "
    "not decide what the merge reads. Human Lead ruling 2, 2026-08-21.")

WHERE_THE_INSTANCE_VALUE_LIVES = (
    "$.document_scope carries additionalProperties: false in "
    "artifacts/step8b-output-schema.json, and its permitted keys are role, producing_step, arm, "
    "merge, also_written_by_steps, isolation_rule, note and source. A NEW KEY WOULD FAIL THE "
    "SCHEMA, and the schema is Step 8b's rather than this arm's to widen, so the instance value "
    "is carried in the permitted free-text slot -- $.document_scope.note -- with a fixed leading "
    "token 'DOCUMENT INSTANCE: ' so it can be matched exactly rather than read out of prose. "
    "REPORTED as a constraint this emission worked within, not as a preference.")

RESOLVED_IN_THIS_EMISSION = {
    "b-emit-1": (
        "A WARRANT THIS EMISSION NOW CARRIES. The previous corrected emission stated, at "
        "$.arms[1].note and in section 9 of the .md, that the un-re-censored row set was "
        "'CHECKED rather than assumed: T0 prime <= T0 holds for every pair' -- after the boolean "
        "that checked it, t0_is_earlier_or_equal_for_every_pair, had been removed as vacuous. A "
        "CLAIM OF HAVING CHECKED IS EITHER TRUE OR IT IS REMOVED, so on the Human Lead's ruling "
        "of 2026-08-21 this arm RECOMPUTED IT rather than softening the sentence. The check is "
        "T0PRIME-ORDER, src/step9_b_0_clock.py::verify_t0_prime_order; it runs in this "
        "pipeline, it RAISES, and the sentence now names it, states what each part compares and "
        "gives its coverage. IT IS NOT THE REMOVED BOOLEAN RESTORED: the bare inequality is true "
        "for the wrong reason on a collapsed T0' and cannot fail, so part 1 reconstructs T0' "
        "from the frame's own date STRINGS, which the epoch conversion never touches. "
        "DEMONSTRATED FAILING ON THE DEFECTIVE VECTOR at logs/step9_b_premiere_clock_repro.txt "
        "section 5 -- part 1 rejects it on 155,556 of 278,452 pairs, while part 2 run alone on "
        "that same vector passes, which is the whole of the case that part 1 is what makes the "
        "replacement failable. NO FIGURE IN THIS EMISSION MOVED: the recomputation added a "
        "check and rewrote three prose fields, and every numeric leaf is unchanged."),
}

OPEN_DEFECTS = {
    "b-md-1": (
        "A TYPED COUNT IN THE .md. src/step9_b_4_md.py asserts 'Six of the twelve movements "
        "this arm measured have negative endpoints' as a literal. It is true of the figures in "
        "this emission, but it is ASSERTED rather than measured, so it cannot follow the "
        "figures if they move. Same class as the carried finding b-wf-1. STILL NOT FIXED: the "
        "rerun of 2026-08-21 was authorised for b-emit-1, and an arm does not widen the scope "
        "of an authorised rerun on its own. REPORTED so the count is not read as measured."),
    "how_to_read_these": (
        "This arm's own defects in this arm's own files, published with the figures rather "
        "than held back. It moves no number in this emission."),
}


def sha12_bytes(b):
    return hashlib.sha256(b).hexdigest()[:12]


def sha12(path):
    with open(path, "rb") as fh:
        return sha12_bytes(fh.read())


def leaves(obj, prefix="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, prefix + "." + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, "%s[%d]" % (prefix, i))
    else:
        yield prefix, obj


def assert_only_added(src, out, allowed_prefixes, label, allowed_modified=()):
    """No measurement may move between the source and the emission.

    `allowed_modified` names, EXHAUSTIVELY AND BY PATH, the leaves this promotion is permitted to
    rewrite. It exists for one leaf -- $.document_scope.note, which carries the instance value --
    and every such leaf must additionally be ADDITIVE: the source text has to survive inside the
    new one. A path not on the list is a hard stop whether or not it holds a number, so the
    permission cannot quietly widen into a figure.
    """
    a, b = dict(leaves(src)), dict(leaves(out))
    moved = [p for p in a if p in b and a[p] != b[p]]
    stray_moved = [p for p in moved if p not in allowed_modified]
    not_additive = [p for p in moved if p in allowed_modified
                    and not (isinstance(a[p], str) and isinstance(b[p], str) and a[p] in b[p])]
    lost = [p for p in a if p not in b]
    added = [p for p in b if p not in a]
    stray = [p for p in added if not any(p.startswith(x) for x in allowed_prefixes)]
    if stray_moved or not_additive or lost or stray:
        sys.exit("HARD STOP: %s -- the emission is not its source. moved=%s not_additive=%s "
                 "lost=%s stray=%s"
                 % (label, stray_moved[:5], not_additive[:5], lost[:5], stray[:5]))
    return {"leaves_compared": len(a), "leaves_moved_outside_the_declared_list": 0,
            "leaves_lost": 0, "keys_added_by_this_promotion": len(added),
            "leaves_rewritten_by_this_promotion": sorted(moved),
            "rewrites_verified_additive": True}


def main():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    me = sha12(os.path.abspath(__file__))
    try:
        head = subprocess.check_output(
            ["git", "-C", ROOT, "rev-parse", "--short", "HEAD"]).decode().strip()
    except Exception:
        head = None

    report = {
        "run": "Step 9, arm b -- EMIT the corrected premiere figures",
        "recorded_at_utc": now,
        "authorised_by": "Human Lead ruling, 2026-08-21.",
        "generator": "src/step9_b_7_emit_corrected.py",
        "generator_sha256_12": me,
        "git_head_short": head,
        "adopts": "nothing",
        "api_calls": 0,
        "supersedes": WHAT,
        "why": WHY,
        "second_authorised_rerun_2026_08_21": {
            "ruling_1": "b-emit-1. RECOMPUTED, not softened and not struck. See "
                        "$.resolved_in_this_emission.",
            "ruling_2": "the instance value. See $.document_instance.",
            "figures_that_moved": "NONE. The rerun added a check and rewrote three prose "
                                  "fields in the emitted JSON; every numeric leaf, on both "
                                  "arms and in every declared interval, is unchanged.",
        },
        "resolved_in_this_emission": RESOLVED_IN_THIS_EMISSION,
        "open_in_this_emission": OPEN_DEFECTS,
        "filenames_and_why": {
            "headline_json": "artifacts/step9-headline-corrected-2026-08-21-b.json",
            "headline_md": "artifacts/step9-headline-corrected-2026-08-21-b.md",
            "working_figures_json": "artifacts/step9-working-figures-corrected-2026-08-21-b.json",
            "distinct_paths": "so the marked originals keep theirs and both are readable side by side",
            "arm_token_last": ("this arm's isolation rule names artifacts/step9-*-b.* as its "
                               "search scope; a name with the arm token in the middle would "
                               "fall outside it, and a filename that defeats the isolation "
                               "control is a defect"),
            "corrected_plus_date": "says what the file is without asserting that it is adopted",
        },
    }

    # ---- headline JSON -----------------------------------------------------
    src_bytes = open(SRC_HEADLINE, "rb").read()
    doc = json.loads(src_bytes)
    src_doc = json.loads(src_bytes)

    notes = doc["notes"]
    notes["step9_b_this_emission_supersedes"] = WHAT
    notes["step9_b_why_it_supersedes"] = WHY
    notes["step9_b_emission_provenance"] = (
        "PROMOTED from processed/step9/b/preview/step9-headline-b.json (sha256:12 %s) into "
        "artifacts/ by src/step9_b_7_emit_corrected.py (sha256:12 %s) at %s, git %s. The "
        "promotion added the $.notes keys prefixed step9_b_this_emission / "
        "step9_b_why_it_supersedes / step9_b_emission / step9_b_arm_signature / "
        "step9_b_not_a_second_arm_file / step9_b_where_the_instance_value_lives / "
        "step9_b_open_defect_ / step9_b_resolved_defect_, and REWROTE EXACTLY ONE EXISTING "
        "LEAF -- $.document_scope.note, to carry this document's instance value, additively, "
        "with the source text surviving inside the new one and the addition asserted to be "
        "additive. NOTHING ELSE CHANGED; every measurement is leaf-for-leaf identical to that "
        "source and the promotion asserts it numerically rather than claiming it. "
        "$.generated_by still names the generator that computed the figures, which is not "
        "this script."
        % (sha12_bytes(src_bytes), me, now, head))
    notes["step9_b_arm_signature"] = SIGNATURE
    notes["step9_b_not_a_second_arm_file"] = NOT_A_SECOND_ARM
    notes["step9_b_where_the_instance_value_lives"] = WHERE_THE_INSTANCE_VALUE_LIVES
    for k, v in OPEN_DEFECTS.items():
        notes["step9_b_open_defect_" + k.replace("-", "_")] = v
    for k, v in RESOLVED_IN_THIS_EMISSION.items():
        notes["step9_b_resolved_defect_" + k.replace("-", "_")] = v

    # THE INSTANCE VALUE. It names THIS document as the corrected instance and does nothing
    # else: it makes the superseded file and this one distinguishable, and says nothing about
    # which a merge takes. $.document_scope forbids additional properties, so it goes in the
    # permitted `note` slot behind a fixed token, APPENDED rather than substituted.
    doc["document_scope"]["note"] = (
        "DOCUMENT INSTANCE: " + DOCUMENT_INSTANCE + ". This document is arm b's CORRECTED "
        "emission of arm b's own Step 9 document, superseding the premiere-anchored arm of "
        + SUPERSEDED_HEADLINE + ". The value is here so the two are distinguishable; what is "
        "done with that is the Human Lead's, at Step 13b. " + doc["document_scope"]["note"])

    report["headline_json"] = assert_only_added(
        src_doc, doc, ("$.notes.step9_b_this_emission", "$.notes.step9_b_why_it_supersedes",
                       "$.notes.step9_b_emission", "$.notes.step9_b_arm_signature",
                       "$.notes.step9_b_not_a_second_arm_file",
                       "$.notes.step9_b_where_the_instance_value_lives",
                       "$.notes.step9_b_open_defect_",
                       "$.notes.step9_b_resolved_defect_"), "headline JSON",
        allowed_modified=("$.document_scope.note",))
    report["document_instance"] = {
        "value": DOCUMENT_INSTANCE,
        "where": "$.document_scope.note, behind the fixed token 'DOCUMENT INSTANCE: '",
        "why_not_a_new_key": WHERE_THE_INSTANCE_VALUE_LIVES,
        "what_it_does_not_do": "it states nothing about which file a merge takes; the merge's "
                               "input contract is Step 13b's and Step 13b is the Human Lead's",
        "superseded_file_untouched": True,
    }
    with open(OUT_HEADLINE, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    report["headline_json"]["source_sha256_12"] = sha12_bytes(src_bytes)
    report["headline_json"]["emitted_sha256_12"] = sha12(OUT_HEADLINE)

    # ---- working-figures JSON ---------------------------------------------
    wsrc_bytes = open(SRC_WORKING, "rb").read()
    wdoc = json.loads(wsrc_bytes)
    wsrc = json.loads(wsrc_bytes)
    wdoc["_emission"] = {
        "document": "Step 9 working-figures extract -- ARM b -- CORRECTED EMISSION",
        "document_instance": DOCUMENT_INSTANCE,
        "document_instance_note": NOT_A_SECOND_ARM,
        "supersedes": SUPERSEDED_WORKING,
        "what_it_supersedes": WHAT,
        "why": WHY,
        "arm_signature": SIGNATURE,
        "promoted_from": "processed/step9/b/preview/step9-working-figures-b.json",
        "promoted_from_sha256_12": sha12_bytes(wsrc_bytes),
        "promoted_by": "src/step9_b_7_emit_corrected.py",
        "promoted_by_sha256_12": me,
        "promoted_at_utc": now,
        "git_head_short": head,
        "promotion_changed_no_measurement": (
            "asserted numerically, not claimed: every leaf of the source is present here with "
            "the same value, and the only added key is this one."),
        "open_defects_in_this_emission": OPEN_DEFECTS,
        "resolved_in_this_emission": RESOLVED_IN_THIS_EMISSION,
        "privacy": "COUNTS AND ACCOUNT TOTALS ONLY. processed/step9/b/pairs.npz was not read.",
    }
    report["working_json"] = assert_only_added(wsrc, wdoc, ("$._emission",),
                                               "working-figures JSON")
    with open(OUT_WORKING, "w") as fh:
        json.dump(wdoc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    report["working_json"]["source_sha256_12"] = sha12_bytes(wsrc_bytes)
    report["working_json"]["emitted_sha256_12"] = sha12(OUT_WORKING)

    # ---- headline .md ------------------------------------------------------
    md_bytes = open(SRC_MD, "rb").read()
    md = md_bytes.decode()
    header = "\n".join([
        "> **CORRECTED EMISSION — 2026-08-21. ARM `b`.** This file supersedes the "
        "premiere-anchored 91-day arm of `" + SUPERSEDED_MD + "`, and **only** that arm. "
        "The adopted `W108_s2_finale` arm is unchanged and is not superseded: it was verified "
        "leaf-for-leaf identical and its harness control reproduces.",
        "",
        "> **Why.** `src/step9_b_1_compute.py` converted the premiere-anchored `T0` column to "
        "epoch seconds with `// 10 ** 9` against a `datetime64[us, UTC]` dtype, so every value "
        "was epoch-**seconds ÷ 1000** — a 1970 date. The superseded figures were correctly "
        "computed from that vector and are **kept and marked at each point of use** in the "
        "file above, because the record of what the defect produced is the evidence for the "
        "finding.",
        "",
        "> **Provenance.** Promoted from `processed/step9/b/preview/step9-headline-b.md` "
        "(sha256:12 `" + sha12_bytes(md_bytes) + "`) by "
        "`src/step9_b_7_emit_corrected.py` (sha256:12 `" + me + "`) at " + now +
        ", git `" + str(head) + "`. **The promotion appended this header and section 10 and "
        "changed no figure and no sentence of the body.**",
        "",
        "> **" + SIGNATURE + "**",
        "",
        "> **Document instance:** `" + DOCUMENT_INSTANCE + "`. " + NOT_A_SECOND_ARM,
        "",
        "> **Where that value lives in the JSON half.** " + WHERE_THE_INSTANCE_VALUE_LIVES,
        "",
        "---",
        "",
    ])
    lines = md.split("\n")
    # After the title line, so the document still opens with its own heading.
    out_md = "\n".join([lines[0], ""] + header.split("\n") + lines[1:])
    out_md += "\n".join([
        "",
        "## 10. Defects in this emission, found by this arm",
        "",
        "**Neither moves a number in this file.** They are published with the figures rather "
        "than held back.",
        "",
        "### Open",
        "",
        "- **`b-md-1`.** " + OPEN_DEFECTS["b-md-1"],
        "",
        "### Resolved in this emission",
        "",
        "- **`b-emit-1`.** " + RESOLVED_IN_THIS_EMISSION["b-emit-1"],
        "",
    ])
    # The body must survive verbatim. The title is lifted above the header, so
    # the check is made in two pieces rather than one.
    title, body = lines[0], "\n".join(lines[1:])
    if title not in out_md or body.strip() not in out_md:
        sys.exit("HARD STOP: the promoted .md does not contain its source body verbatim.")

    with open(OUT_MD, "w") as fh:
        fh.write(out_md)

    report["headline_md"] = {
        "source_sha256_12": sha12_bytes(md_bytes),
        "emitted_sha256_12": sha12(OUT_MD),
        "source_body_preserved_verbatim": True,
        "added": "a provenance/supersession header after the title, and section 10.",
    }

    out = os.path.join(ROOT, "logs", "step9_b_emit_corrected_run.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nrun record: logs/step9_b_emit_corrected_run.json")


if __name__ == "__main__":
    main()
