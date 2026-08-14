"""Step 8 (instance b) -- the BUILD IDENTITY every count and every invariant carries.

decisions/0078: EVERY COUNT NAMES THE PIPELINE IT WAS MEASURED ON, NOT ONLY ITS
POPULATION -- decisions/0047's standing rule one layer down. A count without its
provenance can be correct when written and wrong when read, because the build
moved underneath it and nothing in the text says which build it belongs to.

decisions/0079 Sec 2 extends it: the rule applies to EVERY count, EVERY invariant
result and EVERY waterfall figure, NOT TWO. "Partial application is worse than
none: two labelled figures imply the other counts and the eight invariants did
not need it."

So this module exists to make the label unforgeable rather than typed: BUILD is
one string, stamped onto every emitted count group, every waterfall line and
every invariant, and the input fingerprint is measured from the files rather than
described.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

ROOT = Path("/Users/alyanashantel/Documents/season2-study")

RUN_DATE = "2026-08-14"

BUILD = ("analytics-engineer-b / Step 8 position-5 build of 2026-08-14 "
         "(rerun on the spec as amended through decisions/0080; W = 108, "
         "tau_pull = 2026-08-11T00:00:00Z, mandated filter order 1-7)")

BUILD_SHORT = "b: position-5 build of 2026-08-14"

# The ruled figures carry the build they were RULED on, which is not this one.
RULED_BUILD = "position-5 build of 2026-08-13 (both arms, the run decisions/0078 labelled)"

INPUTS = [
    "processed/step2/frame.csv",
    "processed/step5/full_scan.npz",
    "processed/step5/pair_revision5.csv",
    "processed/step5/calibration.npz",
    "processed/step5/adopted_rule.json",
    "processed/step5/user_index.json",
    "processed/step4/pull_ledger.jsonl",
    "raw/step3/user_pool.jsonl",
    "logs/step4_pull_log.json",
]


def stamp(d: dict) -> dict:
    """Attach the build to one emitted object, at the point of use."""
    d["measured_on_build"] = BUILD
    return d


def input_fingerprint() -> dict:
    """Size and mtime of every input this build reads. Measured, not described."""
    out = {}
    for rel in INPUTS:
        p = ROOT / rel
        if p.exists():
            st = p.stat()
            out[rel] = {"bytes": st.st_size,
                        "mtime_utc": __import__("datetime").datetime.utcfromtimestamp(
                            st.st_mtime).strftime("%Y-%m-%dT%H:%M:%SZ")}
        else:
            out[rel] = {"MISSING": True}
    return out


def source_fingerprint() -> dict:
    """SHA-256 of this arm's own pipeline sources, so the build is identifiable."""
    out = {}
    for rel in sorted(os.listdir(ROOT / "src")):
        if rel.startswith("step8_b_") and rel.endswith(".py"):
            h = hashlib.sha256((ROOT / "src" / rel).read_bytes()).hexdigest()[:16]
            out["src/" + rel] = h
    return out


def provenance_block() -> dict:
    return {
        "build": BUILD,
        "build_short": BUILD_SHORT,
        "rule": ("decisions/0078 and 0079 Sec 2 -- every count, every invariant result and "
                 "every waterfall figure names the PIPELINE it was measured on, not only its "
                 "population. A count without its provenance can be correct when written and "
                 "wrong when read"),
        "ruled_figures_carry_their_own_build": RULED_BUILD,
        "run_date": RUN_DATE,
        "api_calls": 0,
        "inputs": input_fingerprint(),
        "pipeline_sources": source_fingerprint(),
    }
