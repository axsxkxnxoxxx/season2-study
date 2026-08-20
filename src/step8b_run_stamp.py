"""The build stamp a Step 8b run record carries.

WHY THIS EXISTS. The v1.8.0 rerun record opened by saying every item was
reproduced BEFORE it was fixed, and then stamped `build_reproduced_on` and
`build_now` with THE SAME COMMIT -- 9e6f993 for both -- while the commit the run
actually produced, 8a7b17f, appeared nowhere in it. `logs/` is gitignored, so
nothing tied that record to a commit from either side: not to the state it
reproduced on, and not to the state it produced. A record that cannot be placed
in the history is a record whose claims cannot be checked, which is the
provenance rule (CLAUDE.md, `## Derived figures`) applied to a run rather than to
a figure.

THE HONEST SHAPE, AND THE PART THAT CANNOT BE STAMPED. A run record is written
BEFORE the commit that carries its work exists. So that commit's id is NOT
knowable at write time and this module refuses to invent one: it writes
`commit_produced_by_this_run: null` with the reason, in the record, rather than
stamping the pre-edit HEAD a second time and letting a reader take it for the
after-state. THAT SUBSTITUTION IS THE DEFECT ITSELF -- it is how one commit came
to stand for both sides of a before-and-after.

WHAT STANDS IN FOR IT, AND IT IS CHECKABLE FROM THE OTHER SIDE. The record
carries:

  * `commit_reproduced_on` -- HEAD when the run STARTED, captured before any
    edit. Passed in by the caller, because by write time it is gone.
  * `head_at_write_time` -- HEAD when the record was written. Equal to
    `commit_reproduced_on` on a run that has not committed yet, and that equality
    is now MEANINGFUL rather than a coincidence, because the third field says
    what it means.
  * `tracked_tree_digest` -- a PER-PATH CONTENT MANIFEST of everything the tree
    holds that HEAD does not, plus an aggregate over it. THIS IS THE LINK, and
    it is recomputable from the produced commit path by path.

  And the protocol that closes it: THE COMMIT MESSAGE NAMES THE RUN RECORD PATH.
  One pointer each way -- the record names the commit it reproduced on and the
  digest of what it produced, the commit names the record.

THE VERIFICATION RECIPE WAS UNPASSABLE UNTIL v1.9.1 -- reviewer-engineering, who
reproduced it against the real commit. The record used to publish: "commit this
work on top of `head_at_write_time`, then recompute `git diff <commit>^ <commit>
| shasum -a 256`. Equal digests mean this record describes that commit." The two
digests are 9fbfe282... and 741eaa7f... for a record that was entirely correct,
because `git diff HEAD` OMITS UNTRACKED CONTENT while a commit's diff carries a
new file IN FULL -- and 03da73b's new file was THIS MODULE, created by the very
run whose record the recipe was meant to verify. So the recipe returned "not
equal", which the record instructed the reader to read as `this record does not
describe that commit`.

That is not a coverage gap. IT IS AN ASSERTION THAT CANNOT PASS -- the shape a
reviewer names H5-anchor -- and it had arrived inside the module written to end a
provenance defect. Two smaller inaccuracies travelled with it: the docstring
said the digest covered the diff "plus the porcelain status" when the code
hashed the diff alone, and `changed_paths` was built with `line[3:]`, which
DISCARDS THE PORCELAIN XY CODE, so ` M path` (in the digest) and `?? path` (not
in the digest) became identical entries -- the record could not tell a reader
which of its own paths its digest covered, which is the exact distinction the
known-limit paragraph rested on.

WHAT THE DIGESTS BIND NOW, SAID PLAINLY:

  * `content_manifest` -- one row per path the tree changed, carrying the
    porcelain XY code, whether `git diff HEAD` covers it, and the sha256 of the
    file's bytes at write time. UNTRACKED CONTENT IS BOUND HERE. This is the
    part a reader recomputes, per path, from the shipping commit.
  * `content_manifest_digest` -- sha256 over the canonical `path\\tsha` rows.
    Fully recomputable from the shipping commit, because both of its inputs are.
  * `diff_digest` -- sha256 of `git diff HEAD` at write time. A WRITE-TIME
    INTEGRITY VALUE over the tracked modifications, kept because it is what the
    v1.9.0 records carry. It equals the shipping commit's diff digest only when
    that commit adds NO new file and nothing changed between write and commit;
    that condition is stated with it and is itself checkable, so the value is
    conditional rather than misleading.

A path added to the commit AFTER this record was written appears in no row and
is bound by nothing. Run records live under `logs/`, which is gitignored, so
writing one does not disturb its own manifest.
"""

from __future__ import annotations

import hashlib
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_UNAVAILABLE = "unavailable"


def _git(*args: str) -> str | None:
    try:
        return subprocess.run(
            ["git", "-C", ROOT, *args],
            capture_output=True, text=True, check=True,
        ).stdout
    except Exception:  # noqa: BLE001 -- an absent git is reported, never guessed
        return None


def head_short() -> str:
    out = _git("rev-parse", "--short", "HEAD")
    return out.strip() if out is not None else _UNAVAILABLE


def _porcelain_rows() -> list[tuple[str, str, str | None]] | None:
    """`git status --porcelain -z`, parsed WITH the XY code kept.

    `-z` rather than the line form: it does not quote paths with spaces or
    non-ASCII bytes, and it makes a rename's two paths two fields rather than an
    ` -> ` inside one. The XY code is carried through because it is what says
    whether `git diff HEAD` covers the path -- the distinction the old
    `line[3:]` threw away.
    """
    out = _git("status", "--porcelain", "-z")
    if out is None:
        return None
    fields = out.split("\0")
    rows: list[tuple[str, str, str | None]] = []
    i = 0
    while i < len(fields):
        field = fields[i]
        if not field:
            i += 1
            continue
        xy, path = field[:2], field[3:]
        origin = None
        if xy and xy[0] in ("R", "C"):
            i += 1
            origin = fields[i] if i < len(fields) else None
        rows.append((xy, path, origin))
        i += 1
    return rows


def _sha256_of_file(path: str) -> str | None:
    try:
        with open(os.path.join(ROOT, path), "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def _tracked_tree_digest() -> dict:
    """A per-path content manifest of the tree's divergence from HEAD."""
    diff = _git("diff", "HEAD")
    rows = _porcelain_rows()
    if diff is None or rows is None:
        return {
            "what_this_binds": "nothing was computed",
            "diff_digest": _UNAVAILABLE,
            "content_manifest_digest": _UNAVAILABLE,
            "dirty": None,
            "content_manifest": None,
            "changed_paths": None,
            "how_to_verify": (
                "git is unavailable here, so nothing was computed. An absent digest is "
                "reported, never substituted"
            ),
        }

    manifest: list[dict] = []
    for xy, path, origin in sorted(rows, key=lambda r: r[1]):
        # `git diff HEAD` covers tracked changes -- staged and unstaged -- and
        # does NOT cover untracked (`??`) or ignored (`!!`) paths.
        covered = xy not in ("??", "!!")
        content = _sha256_of_file(path)
        entry = {
            "path": path,
            "porcelain_xy": xy,
            "tracked_at_write_time": covered,
            "content_bound_by_diff_digest": covered and content is not None,
            "content_sha256": content,
        }
        if content is None:
            entry["content_sha256_absent_because"] = (
                "the path is not readable in the working tree at write time -- a deletion, or "
                "a path removed after `git status` ran. Its content is bound by nothing here, "
                "and that is stated rather than left as a null to be read as zero"
            )
        if origin is not None:
            entry["renamed_from"] = origin
        manifest.append(entry)

    canonical = "\n".join(
        f"{e['path']}\t{e['content_sha256']}" for e in manifest if e["content_sha256"]
    )
    untracked = [e["path"] for e in manifest if not e["tracked_at_write_time"]]
    return {
        # THE PREDICATE, NAMED (v1.9.1, reviewer-engineering item 4). This block
        # says the TREE differs from HEAD at these paths. It does NOT say who
        # changed them, and a reader who takes it for an authorship claim will
        # read a path someone else edited as this arm's work. The authorship
        # predicate is a separate block, `authorship`, and the two are compared
        # there rather than left side by side to be reconciled by eye.
        "what_this_asserts": (
            "the working tree differs from HEAD at each listed path, and the file's bytes at "
            "write time hashed to `content_sha256`. IT ASSERTS NOTHING ABOUT WHO CHANGED A "
            "PATH -- see $.build.authorship, which carries that predicate separately"
        ),
        "what_this_binds": (
            "content_manifest binds the BYTES of every listed path, untracked ones included. "
            "diff_digest binds only the TRACKED modifications `git diff HEAD` renders"
        ),
        "dirty": bool(manifest),
        "content_manifest": manifest,
        "content_manifest_digest": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "content_manifest_rows": len(manifest),
        "content_manifest_rows_with_content": sum(
            1 for e in manifest if e["content_sha256"]
        ),
        "untracked_at_write_time": untracked,
        "diff_digest": hashlib.sha256(diff.encode("utf-8")).hexdigest(),
        "diff_digest_algorithm": "sha256 of `git diff HEAD` (tracked modifications only)",
        # THE PATH LIST, STILL HERE AND STILL NAMED THIS, because it is what a
        # reader looks for -- but each element now carries its XY code, so
        # `?? path` and ` M path` are no longer one string.
        "changed_paths": [f"{e['porcelain_xy']} {e['path']}" for e in manifest],
        "changed_path_count": len(manifest),
        "how_to_verify": (
            "PRIMARY, AND IT PASSES FOR A CORRECT RECORD. Commit this work on top of "
            "`head_at_write_time`; then for every content_manifest row, "
            "`git cat-file blob <commit>:<path> | shasum -a 256` equals that row's "
            "`content_sha256`. In aggregate: join the rows that carry content as "
            "`<path>\\t<sha>` in path order, newline-separated with no trailing newline, and "
            "sha256 the result -- that is `content_manifest_digest`. Both hold whether or not "
            "the commit adds new files, which is what the v1.9.0 recipe got wrong. "
            "SECONDARY AND CONDITIONAL: `git diff <commit>^ <commit> | shasum -a 256` equals "
            "`diff_digest` ONLY IF that commit adds no new file and nothing changed between "
            "this record and the commit. Check the first clause with "
            "`git diff --diff-filter=A --name-only <commit>^ <commit>`; a non-empty answer "
            "means the two digests are EXPECTED to differ and the difference is not evidence "
            "of anything. A path the commit adds that appears in no row here was created after "
            "this record was written and is bound by nothing in it"
        ),
    }


def _authorship(files_not_edited_by_this_arm, manifest) -> dict:
    """TWO PREDICATES ABOUT ONE PATH, HELD APART (v1.9.1, item 4).

    The v1.9.0 record listed `src/step7_register.py` under
    `scope.files_not_touched` AND under `changed_paths`, and a reviewer read that
    as self-contradiction. It is not one: the first says THIS ARM DID NOT EDIT
    THE FILE, the second says THE TREE SHOWS IT CHANGED, and both were true
    because another party edited it in the same working tree. But the record did
    not distinguish the predicates, so a reader could not tell them apart -- and
    a reader who resolves the apparent contradiction the other way concludes the
    arm edited a file it is not permitted to edit.

    So the overlap is COMPUTED and NAMED here rather than left to be noticed.
    """
    base = {
        "what": (
            "TWO PREDICATES, and a path may satisfy both without contradiction. "
            "(1) TREE: $.build.tracked_tree_digest lists paths where the working tree differs "
            "from HEAD -- a fact about bytes, silent about authorship. "
            "(2) ARM: `files_not_edited_by_this_arm` lists paths THIS ARM did not edit -- a "
            "fact about authorship, silent about whether they changed. A path in both was "
            "changed by someone other than this arm in the same working tree"
        ),
    }
    if files_not_edited_by_this_arm is None:
        base["files_not_edited_by_this_arm"] = None
        base["why_null"] = (
            "the caller supplied no list. NOT the same as an empty list, which would claim the "
            "arm edited every path it touched; this claims nothing"
        )
        base["changed_in_tree_but_not_edited_by_this_arm"] = None
        return base
    named = sorted(set(files_not_edited_by_this_arm))
    # READ THE MANIFEST'S OWN `path` FIELD, never a rendered `changed_paths`
    # string. Those strings are `XY path` and the X half may itself be a space,
    # so splitting one on its first space yields `M tracked.txt` and the overlap
    # silently comes back empty -- which is the failure mode this block exists to
    # prevent, arriving inside it. Caught in the sandbox reproduction, v1.9.1.
    changed_paths = {e["path"] for e in manifest if isinstance(e, dict)}
    overlap = sorted(p for p in named if p in changed_paths)
    base["files_not_edited_by_this_arm"] = named
    base["changed_in_tree_but_not_edited_by_this_arm"] = overlap
    base["overlap_count"] = len(overlap)
    base["how_to_read_the_overlap"] = (
        "each of these paths differs from HEAD and was NOT edited by this arm. Both predicates "
        "hold; the tree carries someone else's edit. This arm attests only to the second "
        "predicate -- who edited a file is the one of the two it can know"
        if overlap else
        "empty: no path this arm declined to edit shows up as changed. Stated rather than "
        "omitted, so an empty overlap is distinguishable from an overlap nobody computed"
    )
    return base


def build_stamp(commit_reproduced_on: str, what: str = "",
                files_not_edited_by_this_arm=None) -> dict:
    """The block a Step 8b run record carries, naming BOTH sides of the run.

    `commit_reproduced_on` is the caller's, because it must be captured before
    the first edit and is gone by the time a record is written. It is not
    defaulted to HEAD: a default would silently reinstate the one-commit-for-both
    -sides defect this module exists to end.

    `files_not_edited_by_this_arm` is the AUTHORSHIP predicate, optional and
    null-by-default. See `_authorship`.
    """
    head_now = head_short()
    digest = _tracked_tree_digest()
    return {
        "what": what or ("the build this run reproduced on and the build it produced. Both "
                         "sides are named, and the side that cannot be known is null rather "
                         "than a repeat of the other"),
        "commit_reproduced_on": commit_reproduced_on,
        "head_at_write_time": head_now,
        "head_equals_reproduced_on": commit_reproduced_on == head_now,
        "commit_produced_by_this_run": None,
        "why_the_produced_commit_is_null": (
            "it does not exist yet. This record is written before the work is committed, so "
            "the commit that carries the work has no id at write time. Stamping "
            "`head_at_write_time` into that slot is what made the v1.8.0 record carry one "
            "commit for both sides of a before-and-after. The link runs the other way: the "
            "tracked-tree manifest below is recomputable from the produced commit, path by "
            "path, and the commit message names this record's path"
        ),
        "tracked_tree_digest": digest,
        "authorship": _authorship(files_not_edited_by_this_arm,
                                  digest.get("content_manifest") or []),
        "generator": "src/step8b_run_stamp.py",
    }
