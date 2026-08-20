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
  * `tracked_tree_digest` -- sha256 of `git diff HEAD` over tracked files, plus
    the porcelain status. THIS IS THE LINK. When the run's work is committed on
    top of `head_at_write_time`, the diff of that commit against its parent is
    the same text, so a reader holding the produced commit can RECOMPUTE this
    digest and confirm that this record describes that commit. The link is made
    from the committed side, which is the only side that can make it.

  And the protocol that closes it: THE COMMIT MESSAGE NAMES THE RUN RECORD PATH.
  One pointer each way -- the record names the commit it reproduced on and the
  digest of what it produced, the commit names the record.

KNOWN LIMIT, STATED RATHER THAN LEFT TO BE FOUND: the digest covers TRACKED
changes. A file that is new and unstaged appears in the porcelain status (so it
is not invisible) but its CONTENT is not in `git diff HEAD`, so the digest does
not bind it. Run records live under `logs/`, which is gitignored, so writing one
does not disturb its own digest.
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


def _tracked_tree_digest() -> dict:
    """A digest of the working tree's TRACKED divergence from HEAD."""
    diff = _git("diff", "HEAD")
    status = _git("status", "--porcelain")
    if diff is None or status is None:
        return {"algorithm": "sha256(git diff HEAD)", "digest": _UNAVAILABLE,
                "dirty": None, "changed_paths": None,
                "how_to_verify": "git is unavailable here, so nothing was computed. An "
                                 "absent digest is reported, never substituted"}
    changed = sorted({line[3:].split(" -> ")[-1] for line in status.splitlines() if line[3:]})
    return {
        "algorithm": "sha256 of `git diff HEAD` (tracked files only)",
        "digest": hashlib.sha256(diff.encode("utf-8")).hexdigest(),
        "dirty": bool(status.strip()),
        "changed_paths": changed,
        "changed_path_count": len(changed),
        "how_to_verify": (
            "commit this work on top of `head_at_write_time`, then recompute: "
            "`git diff <commit>^ <commit> | shasum -a 256`. Equal digests mean this record "
            "describes that commit. UNTRACKED files are listed in `changed_paths` but their "
            "CONTENT is not bound by the digest"
        ),
    }


def build_stamp(commit_reproduced_on: str, what: str = "") -> dict:
    """The block a Step 8b run record carries, naming BOTH sides of the run.

    `commit_reproduced_on` is the caller's, because it must be captured before
    the first edit and is gone by the time a record is written. It is not
    defaulted to HEAD: a default would silently reinstate the one-commit-for-both
    -sides defect this module exists to end.
    """
    head_now = head_short()
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
            "tracked-tree digest below is recomputable from the produced commit, and the "
            "commit message names this record's path"
        ),
        "tracked_tree_digest": _tracked_tree_digest(),
        "generator": "src/step8b_run_stamp.py",
    }
