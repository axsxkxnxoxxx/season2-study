"""
Step 4: pull episode-level watch histories.

Source is `GET /users/:id/history`, unfiltered, one logical sweep per user
(decisions/0002). One sweep is one logical pass, NOT one call: the endpoint
paginates, and Step 4 is costed in pages.

What this module implements that did not exist before
-----------------------------------------------------
decisions/0009  Stratified round-robin pull order. The usable pool is sorted by
                corrected `step4_pages_forecast`, cut into ten equal-count
                bins, and one user is taken from each bin in turn. Order within
                a bin is deterministic (forecast, then slug). Every prefix is
                proportional across the whole distribution including both
                tails, and `verify_prefix_proportionality` demonstrates that on
                the real order rather than assuming it.

decisions/0012  The ADOPTED completeness rule, and the three-way classification
                it explicitly forbids collapsing into one tolerance.
                A sweep is complete when every page reported by
                X-Pagination-Page-Count has been read AND the residual against
                X-Pagination-Item-Count is within 2 percent. Outside the
                tolerance the user is DISCARDED under its own outcome,
                `discarded_over_tolerance`, never truncated, and never folded
                into `unavailable` or into any skip or error category.

                THE RESIDUAL IS COMPUTED ON ACCUMULATED RECORDS, NOT ON
                DISTINCT RECORD IDS, everywhere and without exception. Cross-
                page duplicates are real on this endpoint, so de-duplicating
                before comparing to the header gives a different number; that
                number is reported too, as `residual_on_distinct_ids`, and it
                is never the quantity the tolerance is applied to.

                Three behaviours, counted separately, per user, and NOT assumed
                mutually exclusive — one user can show two of them at once:
                  header_over_count    accumulated < item_count  (benign)
                  header_under_count   accumulated > item_count  (benign, safe
                                       direction)
                  cross-page duplicate records: the same record id returned on
                                       more than one page. Real data behaviour,
                                       not a header artefact. Handled
                                       downstream by Step 1 §2.2 distinct-
                                       episode counting, but reported here as
                                       its own number — affected users AND
                                       affected records — rather than absorbed.

decisions/0010  Tail cap at 300 pages, both halves.
                (a) forecast > 300 -> the user is NEVER STARTED. Zero calls.
                    Recorded with its forecast as `skipped_length_forecast`.
                (b) ACTUAL pages > 300 -> the pages already read are DISCARDED
                    and the user is recorded as `skipped_length_actual`.
                    Never truncated. This reuses the mid-sweep discard path
                    built for decisions/0004: TraktClient.get_paginated raises
                    SweepTooLong and fetch_all throws the partial sweep away,
                    exactly as it does for a mid-sweep 403.
                The two counts are reported SEPARATELY. The second one is the
                direct measure of how wrong `step4_pages_forecast` is.

Correctness rules that are not negotiable
-----------------------------------------
A truncated sweep is indistinguishable from a genuine "never started" and
lands in the study's headline (artifacts/step1-outcome-definition.md §0). So:

  * `max_pages`, the truncating bound on get_paginated, is NEVER used here.
  * Only outcome `complete` is data. Every other outcome is its own value and
    none of them is folded into any other, and none is represented by an empty
    result:

        complete                  full, reconciled sweep
        unavailable               private / deleted profile (documented 401)
        access_denied             user-level 403, decisions/0004
        skipped_length_forecast   decisions/0010 (a)
        skipped_length_actual     decisions/0010 (b)
        discarded_over_tolerance  decisions/0012: residual beyond 2 percent
        error_short_read          item count did not reconcile (the superseded
                                  exact rule; unreachable under page_count)
        error_pagination          pagination headers unusable
        error_other               any other per-user TraktClientError

  * `deferred_budget` is deliberately NOT terminal and is not written to the
    ledger: the user has not been decided, only postponed.

pull_date (D11)
---------------
D11 fixes `pull_date` as a single global frozen cutoff no later than the
earliest per-user fetch date, and its VALUE is the Human Lead's to set once
Step 4's schedule is known. This module records what that decision needs: for
every user, the fetch timestamp of the FIRST page of its sweep and of the last.
The first page is the conservative anchor, because history returns newest-first
and the sweep is only known complete for records older than the instant it
started. The timestamps are read back from the cache meta on disk, not from the
wall clock, so a resumed run reports when the data was actually fetched rather
than when it was replayed.

Resume and interrupt safety
---------------------------
`processed/step4/pull_ledger.jsonl` is append-only and fsynced, one row per
terminal user outcome, last row wins. It is the authoritative record. The
parsed file for a user is written and renamed into place BEFORE its ledger row
is appended, so a kill can leave a parsed file with no ledger row (the user is
simply redone, from cache, at zero API cost) but never a ledger row claiming
data that is not on disk. That ordering is the fix for the Step 3 trap where
`expanded.add()` ran before the work and an interrupt looked complete.

The live-call ledger cannot be zeroed by an offline replay
----------------------------------------------------------
`step3_backfill.py --out-dir raw/step3` zeroed Step 3's call ledger twice,
because an offline replay writes a state file that has spent nothing. Three
independent guards here:
  1. Live spend is derived by SUMMING the append-only ledger rows, not from a
     counter in state.json. Append-only means a replay cannot subtract.
  2. `_save_state` refuses to write a cumulative live-call total lower than the
     one already on disk (LedgerRegression).
  3. Offline mode refuses to use the canonical state directory at all.

Progress, for an unattended run
------------------------------
`logs/step4_progress.json` is rewritten atomically after every user with the
pid, the counts so far, the observed rate and a projected finish. It is
pollable without attaching to the process:

  .venv/bin/python src/step4_history_pull.py --status

Run:
  .venv/bin/python src/step4_history_pull.py --max-users 10 --max-calls 400
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote, unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))

from trakt_client import (  # noqa: E402
    AccessBlocked,
    PaginationDrift,
    PaginationError,
    RateLimitPersistent,
    ResidualOutOfTolerance,
    ShortRead,
    TraktClient,
    TraktClientError,
    TransientFailure,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "raw"
PROCESSED_DIR = PROJECT_ROOT / "processed"
LOGS_DIR = PROJECT_ROOT / "logs"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

POOL_PATH = RAW_DIR / "step3" / "user_pool.jsonl"
STATE_DIR = PROCESSED_DIR / "step4"

# decisions/0002: unfiltered history, and the page basis Step 3's forecast used.
HISTORY_PAGE_LIMIT = 250

# decisions/0010: the tail cap, in pages. Applies to the forecast and to the
# actual page count. A user at exactly 300 is pulled; "exceeds" is strict.
PAGE_CAP = 300

# decisions/0009: ten equal-count bins.
N_BINS = 10

# decisions/0012, ADOPTED by the Human Lead 2026-08-11. These are the defaults,
# not options: a run with no flags uses the adopted rule.
COMPLETENESS_RULE = "page_count"
RESIDUAL_TOLERANCE = 0.02

# decisions/0011, set by the Human Lead 2026-08-11. Recorded here so the run
# record carries it and the D11 constraint is checked rather than asserted.
# NOTHING IN STEP 4 FILTERS ON IT: discarding records at or after tau_pull is
# Step 8's act, on the parsed table, and doing it during the pull would destroy
# the evidence that the constraint was met.
PULL_DATE = "2026-08-11"
TAU_PULL = "2026-08-11T00:00:00Z"

# Not a discriminator, a tripwire. Per-user errors are non-fatal by design so
# an unattended run survives one bad profile, but a long unbroken run of them
# means something systemic and a human should see it before thousands more
# calls are spent.
MAX_CONSECUTIVE_USER_ERRORS = 25

# When a bounded run is nearly out of budget, every remaining user is too big
# to start. Walking the other four thousand to say so is pointless, so the run
# stops instead.
MAX_CONSECUTIVE_DEFERRALS = 20

# decisions/0012 makes an over-tolerance user a DISCARD, not an error, so it
# deliberately does not touch the error breaker above. That leaves a hole: a
# systemic residual fault would discard the whole pool quietly, one benign-
# looking user at a time. This is the tripwire for that. It is not a
# discriminator and it does not change how any user is classified.
MAX_CONSECUTIVE_OVER_TOLERANCE = 25

# Sabbath. The crawl does not run Friday sunset to Saturday sunset. Sunset
# times depend on a location this module does not know, so the window is a
# conservative configurable envelope in LOCAL time, defaulting wide on both
# ends. The Human Lead can narrow it; nothing here narrows it automatically.
DEFAULT_SABBATH_WINDOW = "FRI 17:30-SAT 20:30"
WEEKDAYS = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}

TERMINAL_OUTCOMES = (
    "complete",
    "unavailable",
    "access_denied",
    "skipped_length_forecast",
    "skipped_length_actual",
    "discarded_over_tolerance",
    "error_short_read",
    "error_pagination",
    "error_drift",
    "error_other",
)
DATA_OUTCOMES = ("complete",)
ERROR_OUTCOMES = ("error_short_read", "error_pagination", "error_drift", "error_other")

# decisions/0004 and 0010 and 0012: three different ways a user ends up with no
# data that are NOT "the user watched nothing". Named as a group only so the
# reporting can assert they are never merged; each is counted on its own.
DISCARD_OUTCOMES = (
    "access_denied",
    "skipped_length_forecast",
    "skipped_length_actual",
    "discarded_over_tolerance",
)

EXIT_OK = 0
EXIT_ACCESS_BLOCKED = 2
EXIT_RATE_LIMIT_PERSISTENT = 3
EXIT_TRANSIENT_EXHAUSTED = 4
EXIT_CLIENT_ERROR = 5
EXIT_UNEXPECTED = 6
EXIT_SYSTEMIC_STOP = 7
EXIT_INTERRUPTED = 130

EXIT_MEANINGS = {
    EXIT_OK: "stopped on a committed stopping condition",
    EXIT_ACCESS_BLOCKED: "403 treated as an application-level block",
    EXIT_RATE_LIMIT_PERSISTENT: "429s persisted beyond the configured budget",
    EXIT_TRANSIENT_EXHAUSTED: "transient backoff exhausted",
    EXIT_CLIENT_ERROR: "TraktClientError",
    EXIT_UNEXPECTED: "unexpected exception",
    EXIT_SYSTEMIC_STOP: "a per-user tripwire fired: consecutive failures or "
                        "consecutive over-tolerance discards",
    EXIT_INTERRUPTED: "interrupted",
}


class LedgerRegression(Exception):
    """A write would have reduced the recorded live-call spend. Refused."""


class OfflineGuard(Exception):
    """An offline replay tried to write to the canonical state directory."""


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_instant(stamp: str | None) -> datetime | None:
    """ISO 8601 -> aware datetime. `Z` and `+00:00` are the same instant and a
    string comparison does not know that, so the D11 constraint is checked on
    parsed instants rather than on text."""
    if not stamp:
        return None
    try:
        return datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
    except ValueError:
        return None


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _atomic_write_gzip_lines(path: Path, lines: Iterable[str]) -> int:
    """Write a parsed history file, atomically. mtime is pinned so the file is
    byte-reproducible for the same input."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    written = 0
    with open(tmp, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            for line in lines:
                gz.write((line + "\n").encode("utf-8"))
                written += 1
        raw.flush()
        os.fsync(raw.fileno())
    tmp.replace(path)
    return written


def parse_sabbath_window(spec: str | None) -> tuple[int, int, int, int] | None:
    """"FRI 17:30-SAT 20:30" -> (4, 1050, 5, 1230), in local minutes-of-week."""
    if not spec or spec.strip().lower() in {"off", "none", "disabled"}:
        return None
    m = re.fullmatch(
        r"\s*([A-Za-z]{3})\s+(\d{1,2}):(\d{2})\s*-\s*([A-Za-z]{3})\s+(\d{1,2}):(\d{2})\s*",
        spec,
    )
    if not m:
        raise ValueError(f"unparseable sabbath window {spec!r}; expected 'FRI 17:30-SAT 20:30'")
    d0, h0, m0, d1, h1, m1 = m.groups()
    return (WEEKDAYS[d0.upper()], int(h0) * 60 + int(m0),
            WEEKDAYS[d1.upper()], int(h1) * 60 + int(m1))


def in_sabbath(now: datetime, window: tuple[int, int, int, int] | None) -> bool:
    """True inside the configured local window. Wraps across the week end."""
    if window is None:
        return False
    d0, t0, d1, t1 = window
    start = d0 * 1440 + t0
    end = d1 * 1440 + t1
    now_min = now.weekday() * 1440 + now.hour * 60 + now.minute
    if start <= end:
        return start <= now_min < end
    return now_min >= start or now_min < end


# ---------------------------------------------------------------------------
# decisions/0009: the pull order
# ---------------------------------------------------------------------------


def load_pool(path: Path = POOL_PATH) -> list[dict[str, Any]]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def build_plan(
    pool_records: list[dict[str, Any]],
    n_bins: int = N_BINS,
    page_cap: int = PAGE_CAP,
) -> dict[str, Any]:
    """Stratified round-robin over ten equal-count bins (decisions/0009).

    The forecast cap (decisions/0010 a) is applied BEFORE binning, because a
    user over the cap is never started and so is not part of the pull at all.
    Binning the pullable population is what makes "every prefix is proportional
    across the full distribution" a statement about what actually gets pulled.
    The capped users are returned separately and in full, so they are recorded
    and counted rather than dropped.
    """
    entries: list[dict[str, Any]] = []
    for rec in pool_records:
        screen = rec.get("screen") or {}
        if not screen.get("usable"):
            continue
        entries.append({
            "slug": rec["slug"],
            "username": rec.get("username"),
            "channel_first": rec.get("channel_first"),
            "in_a": bool(rec.get("in_a")),
            "in_b": bool(rec.get("in_b")),
            "forecast_pages": int(screen["step4_pages_forecast"]),
            "stats_payload_variant": screen.get("stats_payload_variant"),
            "history_plays_reported": screen.get("history_plays"),
        })

    # Deterministic total order: forecast, then slug. Ties can never depend on
    # file order, so two runs of this function agree byte for byte.
    entries.sort(key=lambda e: (e["forecast_pages"], e["slug"]))

    eligible = [e for e in entries if e["forecast_pages"] <= page_cap]
    over_cap = [e for e in entries if e["forecast_pages"] > page_cap]

    n = len(eligible)
    bins: list[list[dict[str, Any]]] = []
    for i in range(n_bins):
        lo = (i * n) // n_bins
        hi = ((i + 1) * n) // n_bins
        chunk = eligible[lo:hi]
        for e in chunk:
            e["bin"] = i
        bins.append(chunk)

    order: list[dict[str, Any]] = []
    depth = 0
    while True:
        added = False
        for b in bins:
            if depth < len(b):
                order.append(b[depth])
                added = True
        if not added:
            break
        depth += 1

    for rank, e in enumerate(order):
        e["pull_rank"] = rank

    return {
        "n_bins": n_bins,
        "page_cap": page_cap,
        "usable_users": len(entries),
        "eligible_users": len(eligible),
        "skipped_forecast_users": len(over_cap),
        "skipped_forecast_pages": sum(e["forecast_pages"] for e in over_cap),
        "eligible_forecast_pages": sum(e["forecast_pages"] for e in eligible),
        "total_forecast_pages": sum(e["forecast_pages"] for e in entries),
        "bin_sizes": [len(b) for b in bins],
        "bin_forecast_ranges": [
            [b[0]["forecast_pages"], b[-1]["forecast_pages"]] if b else None for b in bins
        ],
        "order": order,
        "over_cap": over_cap,
    }


def verify_prefix_proportionality(plan: dict[str, Any]) -> dict[str, Any]:
    """Demonstrate decisions/0009's central claim instead of asserting it.

    Claim: every prefix of the order is proportional across the full forecast
    distribution, both tails included. Operationally, at every prefix length
    and over the bins that are not yet exhausted, the per-bin counts differ by
    at most one. A bin that has run out cannot be under-represented by the
    order; it has simply been fully pulled.
    """
    order = plan["order"]
    n_bins = plan["n_bins"]
    sizes = plan["bin_sizes"]
    counts = [0] * n_bins
    worst = 0
    worst_at = 0
    for k, entry in enumerate(order, start=1):
        counts[entry["bin"]] += 1
        live = [counts[i] for i in range(n_bins) if counts[i] < sizes[i]]
        if len(live) >= 2:
            spread = max(live) - min(live)
            if spread > worst:
                worst, worst_at = spread, k
    return {
        "prefixes_checked": len(order),
        "max_spread_between_unexhausted_bins": worst,
        "at_prefix_length": worst_at,
        "holds": worst <= 1,
        "statement": (
            "at every prefix length, the number of users taken from any two "
            "bins that still have members differs by at most one"
        ),
    }


def prefix_page_distribution(plan: dict[str, Any], k: int) -> dict[str, Any]:
    """The realized forecast-page distribution of the first k pulled users,
    against the eligible pool's. decisions/0009 requires this reported rather
    than asserted."""

    def describe(values: list[int]) -> dict[str, Any]:
        if not values:
            return {"n": 0}
        s = sorted(values)

        def pct(p: float) -> int:
            idx = min(len(s) - 1, max(0, int(round((p / 100.0) * (len(s) - 1)))))
            return s[idx]

        return {
            "n": len(s),
            "mean": round(sum(s) / len(s), 2),
            "min": s[0],
            "p25": pct(25),
            "median": pct(50),
            "p75": pct(75),
            "p95": pct(95),
            "max": s[-1],
        }

    order = plan["order"]
    return {
        "prefix": describe([e["forecast_pages"] for e in order[:k]]),
        "eligible_pool": describe([e["forecast_pages"] for e in order]),
        "prefix_bin_counts": Counter(e["bin"] for e in order[:k]),
    }


# ---------------------------------------------------------------------------
# parsing
# ---------------------------------------------------------------------------


def classify_sweep(
    items: list[Any],
    page_item_counts: list[int] | None,
    item_count_reported: int | None,
) -> dict[str, Any]:
    """decisions/0012's three behaviours, per user, counted separately.

    They are NOT mutually exclusive and nothing here treats them as though they
    were: a user can be a header over-count AND carry cross-page duplicates,
    and it is counted in both.

      header_over_count    accumulated < item_count. The header claims more
                           records than the endpoint returns. Benign.
      header_under_count   accumulated > item_count. Benign, and in the safe
                           direction: more data than advertised, not less.
      cross-page duplicate the same record id on more than one page. REAL DATA
                           BEHAVIOUR, not a header artefact. Reported as
                           affected ids and as affected (surplus) records.

    WHICH RESIDUAL. `residual_on_accumulated` is accumulated records minus the
    header, and it is the ONLY quantity the 2 percent tolerance is ever applied
    to, here and in TraktClient. `residual_on_distinct_ids` is the same
    subtraction after de-duplication. They differ by exactly the duplicate
    surplus, which is why both are carried: quoting one where the other was
    meant is precisely the confusion 0012 was written to prevent.

    Page attribution comes from `page_item_counts`, the per-page record counts
    in page order, because `items` is the pages concatenated. Without it a
    cross-page duplicate cannot be told from a within-page one, so when it is
    absent the cross-page figures are None rather than guessed.
    """
    accumulated = len(items)
    # ids in page order. Occurrences of one id are grouped by page and pages
    # arrive in order, so "the page changed since I last saw this id" counts
    # distinct pages without holding a set per id.
    last_page: dict[Any, int] = {}
    pages_for_id: dict[Any, int] = {}
    times_seen: dict[Any, int] = {}
    missing_id = 0

    if page_item_counts:
        bounds = []
        pos = 0
        for size in page_item_counts:
            bounds.append((pos, pos + size))
            pos += size
        if pos != accumulated:
            # The slices do not tile the record list, so page attribution is
            # not trustworthy. Say so rather than report a wrong number.
            bounds = []
    else:
        bounds = []

    if bounds:
        for page_index, (lo, hi) in enumerate(bounds):
            for rec in items[lo:hi]:
                rid = rec.get("id") if isinstance(rec, dict) else None
                if rid is None:
                    missing_id += 1
                    continue
                times_seen[rid] = times_seen.get(rid, 0) + 1
                seen_on = last_page.get(rid)
                if seen_on is None:
                    last_page[rid] = page_index
                    pages_for_id[rid] = 1
                elif seen_on != page_index:
                    last_page[rid] = page_index
                    pages_for_id[rid] = pages_for_id[rid] + 1
        cross_ids = [rid for rid, n in pages_for_id.items() if n >= 2]
        cross_records = sum(times_seen[rid] - 1 for rid in cross_ids)
        within_records = sum(
            times_seen[rid] - 1
            for rid, n in pages_for_id.items()
            if n == 1 and times_seen[rid] > 1
        )
        distinct = len(times_seen)
        page_attribution = True
    else:
        for rec in items:
            rid = rec.get("id") if isinstance(rec, dict) else None
            if rid is None:
                missing_id += 1
                continue
            times_seen[rid] = times_seen.get(rid, 0) + 1
        cross_ids, cross_records, within_records = [], None, None
        distinct = len(times_seen)
        page_attribution = False

    duplicate_surplus = sum(n - 1 for n in times_seen.values())
    residual_acc = (
        accumulated - item_count_reported
        if isinstance(item_count_reported, int) else None
    )
    residual_distinct = (
        (distinct + missing_id) - item_count_reported
        if isinstance(item_count_reported, int) else None
    )
    return {
        "accumulated_records": accumulated,
        "distinct_record_ids": distinct,
        "records_missing_an_id": missing_id,
        "item_count_header": item_count_reported,
        "residual_on_accumulated": residual_acc,
        "residual_on_distinct_ids": residual_distinct,
        "residual_basis": "accumulated_records",
        "header_over_count": residual_acc is not None and residual_acc < 0,
        "header_under_count": residual_acc is not None and residual_acc > 0,
        "header_exact": residual_acc == 0,
        "page_attribution_available": page_attribution,
        "cross_page_duplicate_ids": len(cross_ids) if page_attribution else None,
        "cross_page_duplicate_records": cross_records,
        "within_page_duplicate_records": within_records,
        "duplicate_records_total": duplicate_surplus,
    }


def parse_history(
    items: list[Any],
    page_item_counts: list[int] | None = None,
    item_count_reported: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Raw history records -> the compact rows Steps 5, 7 and 8 need.

    Kept: the record id (Step 5's import detector needs it — an id is assigned
    at insert time, so a recent id on an old watched_at is the signature of a
    bulk import), watched_at, action (decisions/0002 keeps it, Step 13 has an
    arm on it), type, and for episodes the show and episode identifiers.
    Dropped: titles, artwork ids, and show.aired_episodes, which Step 1 §0
    forbids using.

    Nothing is deduplicated or filtered here. Deduplication is a definitional
    act (Step 1 §2.2) and belongs to Step 8, not to the pull.
    """
    rows: list[dict[str, Any]] = []
    seen_ids: set[Any] = set()
    stats = {
        "records": 0,
        "episode_records": 0,
        "movie_records": 0,
        "other_type_records": 0,
        "duplicate_record_ids": 0,
        "missing_watched_at": 0,
        "missing_id": 0,
        "episode_missing_show_id": 0,
        "actions": Counter(),
        "earliest_watched_at": None,
        "latest_watched_at": None,
        "distinct_shows": 0,
    }
    shows: set[Any] = set()
    for rec in items:
        if not isinstance(rec, dict):
            continue
        stats["records"] += 1
        rid = rec.get("id")
        watched_at = rec.get("watched_at")
        rtype = rec.get("type")
        if rid is None:
            stats["missing_id"] += 1
        elif rid in seen_ids:
            stats["duplicate_record_ids"] += 1
        else:
            seen_ids.add(rid)
        if not watched_at:
            stats["missing_watched_at"] += 1
        else:
            if stats["earliest_watched_at"] is None or watched_at < stats["earliest_watched_at"]:
                stats["earliest_watched_at"] = watched_at
            if stats["latest_watched_at"] is None or watched_at > stats["latest_watched_at"]:
                stats["latest_watched_at"] = watched_at
        stats["actions"][rec.get("action")] += 1

        row: dict[str, Any] = {
            "id": rid,
            "watched_at": watched_at,
            "action": rec.get("action"),
            "type": rtype,
        }
        if rtype == "episode":
            stats["episode_records"] += 1
            ep = rec.get("episode") or {}
            sh = rec.get("show") or {}
            ep_ids = ep.get("ids") or {}
            sh_ids = sh.get("ids") or {}
            row["season"] = ep.get("season")
            row["number"] = ep.get("number")
            row["episode_trakt"] = ep_ids.get("trakt")
            row["show_trakt"] = sh_ids.get("trakt")
            row["show_slug"] = sh_ids.get("slug")
            if sh_ids.get("trakt") is None:
                stats["episode_missing_show_id"] += 1
            else:
                shows.add(sh_ids.get("trakt"))
        elif rtype == "movie":
            stats["movie_records"] += 1
        else:
            stats["other_type_records"] += 1
        rows.append(row)

    stats["distinct_shows"] = len(shows)
    stats["actions"] = dict(stats["actions"])
    # decisions/0012. `duplicate_record_ids` above is the surplus over the whole
    # sweep and does not say whether a repeat crossed a page boundary; the
    # classification does, and the cross-page number is the one 0012 asks for.
    stats["classification"] = classify_sweep(items, page_item_counts, item_count_reported)
    return rows, stats


# ---------------------------------------------------------------------------
# the puller
# ---------------------------------------------------------------------------


class Step4Puller:
    def __init__(
        self,
        client: TraktClient,
        state_dir: Path | None = None,
        pool_path: Path = POOL_PATH,
        page_cap: int = PAGE_CAP,
        page_limit: int = HISTORY_PAGE_LIMIT,
        max_users: int | None = None,
        max_calls: int | None = None,
        retry_errors: bool = False,
        retry_outcomes: Iterable[str] | None = None,
        sabbath_window: tuple[int, int, int, int] | None = None,
        offline: bool = False,
        run_label: str = "step4",
        reconcile: str = COMPLETENESS_RULE,
        residual_tolerance: float = RESIDUAL_TOLERANCE,
        exclude_slugs: Iterable[str] | None = None,
    ):
        self.client = client
        self.state_dir = Path(state_dir or STATE_DIR)
        if offline and self.state_dir.resolve() == STATE_DIR.resolve():
            raise OfflineGuard(
                "an offline run may not write to the canonical Step 4 state "
                f"directory ({STATE_DIR}). Pass --state-dir. This is the guard "
                "that stops a replay from overwriting the live-call ledger, "
                "which is exactly what happened to Step 3 twice."
            )
        self.offline = offline
        self.pool_path = Path(pool_path)
        self.page_cap = page_cap
        self.page_limit = page_limit
        self.max_users = max_users
        self.max_calls = max_calls
        self.retry_errors = retry_errors
        self.sabbath_window = sabbath_window
        self.run_label = run_label
        # Which already-decided outcomes a run is allowed to decide again. An
        # empty set means a decided user is never touched, which is the default
        # and the only safe setting for an unattended run. Re-deciding is
        # always free when the pages are cached and is what lets a rule change
        # be replayed over users decided under the old rule.
        retry = set(retry_outcomes or ())
        if retry_errors:
            retry |= set(ERROR_OUTCOMES)
        unknown = retry - set(TERMINAL_OUTCOMES)
        if unknown:
            raise ValueError(f"unknown outcome(s) to retry: {sorted(unknown)}")
        self.retry_outcomes = retry
        # decisions/0012, ADOPTED 2026-08-11: "page_count" with a 2 percent
        # residual tolerance is the default. "exact" is the superseded rule and
        # is kept only because Step 0's and Step 3's evidence was gathered
        # under it.
        if reconcile not in ("exact", "page_count"):
            raise ValueError(f"unknown reconcile mode {reconcile!r}")
        self.reconcile = reconcile
        self.residual_tolerance = residual_tolerance
        # Slugs the Human Lead has placed OUT OF SCOPE for this run. They are
        # not decided, not skipped by any rule in decisions/0004, 0010 or 0012,
        # and no ledger row is written for them: the run simply does not touch
        # them, and they stay exactly as they were for a later run. This is a
        # scope bound on a resumed run, NOT a study rule, so it is counted in
        # the run record and never turned into an outcome.
        self.exclude_slugs = set(exclude_slugs or ())
        self.excluded_this_run: list[str] = []

        self.state_path = self.state_dir / "state.json"
        self.ledger_path = self.state_dir / "pull_ledger.jsonl"
        self.order_path = self.state_dir / "pull_order.jsonl"
        self.parsed_dir = self.state_dir / "parsed"
        self.deferred_path = self.state_dir / "deferred.jsonl"
        self.failure_log_path = LOGS_DIR / "step4_failures.ndjson"
        self.progress_path = LOGS_DIR / "step4_progress.json"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.parsed_dir.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        self.started_at = utcnow()
        self.run_id = f"{self.started_at}-{os.getpid()}"
        self.stop_reason: str | None = None
        self.consecutive_errors = 0
        self.consecutive_over_tolerance = 0
        # Set when a tripwire fires rather than a committed stopping rule. It
        # is what makes a systemic fault exit non-zero instead of looking like
        # a clean finish.
        self.abnormal_stop = False
        self.started_monotonic = time.monotonic()
        self.calls_at_start = client.counters["requests_sent"]
        self.users_attempted_this_run = 0
        self.deferred_this_run: list[dict[str, Any]] = []

        self.plan = build_plan(load_pool(self.pool_path), page_cap=page_cap)
        self.ledger_rows = self._load_ledger()

    # -- ledger ------------------------------------------------------------

    def _load_ledger(self) -> list[dict[str, Any]]:
        if not self.ledger_path.exists():
            return []
        rows = []
        for line in self.ledger_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    # A row half-written by a kill. Append-only plus fsync makes
                    # this all but impossible, but a truncated tail is dropped
                    # rather than guessed at, and the user is simply redone.
                    continue
        return rows

    def latest_outcomes(self) -> dict[str, dict[str, Any]]:
        """Last row wins per user: a retry supersedes an earlier attempt."""
        out: dict[str, dict[str, Any]] = {}
        for row in self.ledger_rows:
            out[row["slug"]] = row
        return out

    def live_calls_recorded(self) -> int:
        """Total live calls ever spent by Step 4, summed over EVERY ledger row.

        Summed, not read from a counter, and over every row rather than the
        latest per user, because a superseded attempt really did spend its
        calls. Append-only means nothing offline can reduce this number.
        """
        return sum(int(row.get("live_calls") or 0) for row in self.ledger_rows)

    def _append_ledger(self, row: dict[str, Any]) -> None:
        line = json.dumps(row, sort_keys=True, default=str)
        self.client._refuse_if_secret(line, str(self.ledger_path))
        with self.ledger_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        self.ledger_rows.append(row)

    def _append_failure(self, record: dict[str, Any]) -> None:
        record = {"ts": utcnow(), "run": self.run_id, **record}
        line = json.dumps(record, sort_keys=True, default=str)
        self.client._refuse_if_secret(line, str(self.failure_log_path))
        with self.failure_log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
            os.fsync(fh.fileno())

    # -- state -------------------------------------------------------------

    def _save_state(self) -> None:
        """state.json is a convenience cache over the ledger, and it is guarded.

        The authoritative spend is the ledger sum. This file carries it too so
        a reader does not have to re-derive it, and refuses to write a smaller
        number than the one already on disk.
        """
        live_calls = self.live_calls_recorded()
        if self.state_path.exists():
            try:
                previous = json.loads(self.state_path.read_text(encoding="utf-8"))
                prior = int(previous.get("live_calls_recorded") or 0)
            except (ValueError, OSError, TypeError):
                prior = 0
            if live_calls < prior:
                raise LedgerRegression(
                    f"refusing to write a live-call total of {live_calls} over a "
                    f"recorded {prior}. The ledger is the only record of what Step 4 "
                    f"has spent, and an offline replay spends nothing."
                )
        payload = {
            "schema": 1,
            "run_id": self.run_id,
            "started_at": self.started_at,
            "saved_at": utcnow(),
            "page_cap": self.page_cap,
            "page_limit": self.page_limit,
            "n_bins": self.plan["n_bins"],
            "users_in_plan": len(self.plan["order"]),
            "users_over_forecast_cap": self.plan["skipped_forecast_users"],
            "users_decided": len(self.latest_outcomes()),
            "live_calls_recorded": live_calls,
            "stop_reason": self.stop_reason,
        }
        _atomic_write_text(self.state_path, json.dumps(payload, indent=2))

    def write_progress(self) -> Path:
        """logs/step4_progress.json — pollable without attaching to the process.

        Counts only: no slug, no username, nothing per-user. Rewritten
        atomically after every user, so a reader never sees a half-written file
        and a kill leaves the last complete snapshot rather than a truncated
        one.
        """
        latest = self.latest_outcomes()
        by_outcome = Counter(row["outcome"] for row in latest.values())
        elapsed = max(time.monotonic() - self.started_monotonic, 1e-9)
        attempted = self.users_attempted_this_run
        live = self._live_calls_this_run()
        remaining = max(0, len(self.plan["order"]) - sum(
            1 for r in latest.values() if r.get("pull_rank") is not None))
        users_per_hour = attempted / (elapsed / 3600.0) if attempted else None
        eta_hours = (remaining / users_per_hour) if users_per_hour else None
        payload = {
            "pid": os.getpid(),
            "run_id": self.run_id,
            "started_at": self.started_at,
            "updated_at": utcnow(),
            "elapsed_hours": round(elapsed / 3600.0, 3),
            "completeness_rule": self.reconcile,
            "residual_tolerance": self.residual_tolerance,
            "users_in_plan": len(self.plan["order"]),
            "users_over_forecast_cap": self.plan["skipped_forecast_users"],
            "users_decided_total": len(latest),
            "users_remaining_in_plan": remaining,
            "users_attempted_this_run": attempted,
            # Count only. The slugs themselves are never written here.
            "users_out_of_scope_this_run": len(self.exclude_slugs),
            "users_skipped_as_out_of_scope": len(self.excluded_this_run),
            "by_outcome": dict(by_outcome),
            "live_calls_this_run": live,
            "live_calls_recorded_all_runs": self.live_calls_recorded(),
            "cache_hits_this_run": self.client.counters["served_from_cache"],
            "live_calls_per_minute_observed": round(live / (elapsed / 60.0), 2),
            "users_per_hour_observed": round(users_per_hour, 2) if users_per_hour else None,
            "projected_hours_remaining": round(eta_hours, 2) if eta_hours else None,
            "consecutive_errors": self.consecutive_errors,
            "consecutive_over_tolerance": self.consecutive_over_tolerance,
            "rate_limit_pauses_429": self.client.counters.get("rate_limit_pauses", 0),
            "user_403_skipped": self.client.counters.get("user_403_skipped", 0),
            "http_5xx": self.client.counters.get("http_5xx", 0),
            "transport_errors": self.client.counters.get("transport_errors", 0),
            "unavailable": self.client.counters.get("unavailable", 0),
            "stop_reason": self.stop_reason,
            "abnormal_stop": self.abnormal_stop,
            "finished": self.stop_reason is not None,
        }
        text = json.dumps(payload, indent=2, default=str)
        self.client._refuse_if_secret(text, str(self.progress_path))
        leaked = names_in(payload, pool_names(self))
        if leaked:
            raise RuntimeError(
                f"refusing to write {len(leaked)} pool name(s) to the progress file")
        _atomic_write_text(self.progress_path, text)
        return self.progress_path

    def write_order(self) -> Path:
        """The pull order, materialised. Carries usernames, so processed/ only."""
        lines = []
        for e in self.plan["order"]:
            lines.append(json.dumps({**e, "eligible": True}, sort_keys=True))
        for e in self.plan["over_cap"]:
            lines.append(json.dumps(
                {**e, "eligible": False, "reason": "forecast_over_cap"}, sort_keys=True))
        _atomic_write_text(self.order_path, "".join(l + "\n" for l in lines))
        return self.order_path

    # -- one user ----------------------------------------------------------

    def _endpoint(self, slug: str) -> str:
        return f"users/{quote(slug, safe='')}/history"

    def _page_fetch_times(self, endpoint: str, pages: int) -> tuple[str | None, str | None]:
        """Per-user fetch timestamps for D11, read from the cache meta on disk.

        Not the wall clock: on a resumed run the wall clock is when the pages
        were replayed, and `pull_date` has to be no later than when they were
        actually fetched.
        """
        stamps: list[str] = []
        for page in range(1, max(pages, 1) + 1):
            _, meta_path = self.client.cache_paths(
                endpoint, {"page": page, "limit": self.page_limit})
            if not meta_path.exists():
                continue
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                continue
            stamp = meta.get("fetched_at")
            if stamp:
                stamps.append(stamp)
        if not stamps:
            return None, None
        return min(stamps), max(stamps)

    def _record(self, entry: dict[str, Any], outcome: str, **fields: Any) -> dict[str, Any]:
        row = {
            "run_id": self.run_id,
            "recorded_at": utcnow(),
            "slug": entry["slug"],
            "username": entry.get("username"),
            "channel_first": entry.get("channel_first"),
            "in_a": entry.get("in_a"),
            "in_b": entry.get("in_b"),
            "bin": entry.get("bin"),
            "pull_rank": entry.get("pull_rank"),
            "forecast_pages": entry["forecast_pages"],
            "outcome": outcome,
            "is_data": outcome in DATA_OUTCOMES,
            "live_calls": 0,
            "cache_hits": 0,
            "pages_read": 0,
            "page_count_reported": None,
            "item_count_reported": None,
            "first_page_fetched_at": None,
            "last_page_fetched_at": None,
            "parsed_path": None,
            "records": 0,
            "detail": None,
        }
        row.update(fields)
        return row

    def pull_user(self, entry: dict[str, Any]) -> dict[str, Any]:
        """One user, one logical sweep. Returns the ledger row (already written).

        Raises only the four run-level stops: AccessBlocked, RateLimitPersistent,
        TransientFailure and KeyboardInterrupt. Every other failure is recorded
        against the user and the run continues.
        """
        slug = entry["slug"]
        endpoint = self._endpoint(slug)

        # decisions/0010 (a). Never started. Zero calls, and the forecast is
        # recorded with it because that is what the decision asks to report.
        if entry["forecast_pages"] > self.page_cap:
            row = self._record(
                entry, "skipped_length_forecast",
                detail=(f"forecast {entry['forecast_pages']} pages exceeds the "
                        f"{self.page_cap}-page cap; never started"),
            )
            self._append_ledger(row)
            return row

        calls_before = self.client.counters["requests_sent"]
        cache_before = self.client.counters["served_from_cache"]
        budget_pages = None
        if self.max_calls is not None:
            budget_pages = max(0, self.max_calls - self._live_calls_this_run())

        started = time.time()
        try:
            items, info = self.client.fetch_all(
                endpoint,
                limit=self.page_limit,
                page_cap=self.page_cap,
                budget_pages=budget_pages,
                reconcile=self.reconcile,
                residual_tolerance=self.residual_tolerance,
            )
        except ResidualOutOfTolerance as exc:
            # Defensive only: fetch_all turns this into the
            # `discarded_over_tolerance` outcome and does not re-raise it. If it
            # ever does reach here it must NOT be filed as an error, because
            # decisions/0012 requires the discard to stay its own count.
            return self._record_user_error(entry, "discarded_over_tolerance", exc,
                                           calls_before, cache_before)
        except ShortRead as exc:
            return self._record_user_error(entry, "error_short_read", exc,
                                           calls_before, cache_before)
        except PaginationDrift as exc:
            # The history moved while we were reading it. Not a fault of ours
            # and not a statement about the user: a later re-sweep is the fix.
            return self._record_user_error(entry, "error_drift", exc,
                                           calls_before, cache_before)
        except PaginationError as exc:
            return self._record_user_error(entry, "error_pagination", exc,
                                           calls_before, cache_before)
        except (AccessBlocked, RateLimitPersistent, TransientFailure):
            raise
        except TraktClientError as exc:
            return self._record_user_error(entry, "error_other", exc,
                                           calls_before, cache_before)

        live = self.client.counters["requests_sent"] - calls_before
        cached = self.client.counters["served_from_cache"] - cache_before
        first_fetch, last_fetch = self._page_fetch_times(endpoint, info["pages"])

        if info["outcome"] == "budget_exhausted":
            # NOT terminal and NOT a ledger row. The user has been postponed,
            # not decided. Nothing partial was kept: fetch_all discarded it.
            deferred = {
                "slug": slug,
                "forecast_pages": entry["forecast_pages"],
                "page_count_reported": info.get("page_count_reported"),
                "pages_read_before_stop": info["pages"],
                "items_discarded": info["discarded_items"],
                "live_calls": live,
                "reason": "run call budget could not cover the sweep",
            }
            self.deferred_this_run.append(deferred)
            self._append_failure({"event": "deferred_budget", **deferred})
            return {"outcome": "deferred_budget", "live_calls": live, **deferred}

        outcome = {
            "complete": "complete",
            "unavailable": "unavailable",
            "access_denied": "access_denied",
            "skipped_too_long": "skipped_length_actual",
            "discarded_over_tolerance": "discarded_over_tolerance",
        }[info["outcome"]]

        parsed_path = None
        records = 0
        parse_stats: dict[str, Any] = {}
        if outcome == "complete":
            rows, parse_stats = parse_history(
                items,
                page_item_counts=info.get("page_item_counts"),
                item_count_reported=info.get("item_count_reported"),
            )
            parsed_path = self.parsed_dir / f"{_safe_name(slug)}.jsonl.gz"
            # Data first, then the claim that the data exists. A kill between
            # the two redoes the user from cache; the reverse order would leave
            # a ledger row pointing at nothing.
            records = _atomic_write_gzip_lines(
                parsed_path, (json.dumps(r, sort_keys=True) for r in rows))

        detail = None
        if outcome == "skipped_length_actual":
            detail = (f"actual sweep is {info.get('page_count_reported')} pages against a "
                      f"forecast of {entry['forecast_pages']}; over the {self.page_cap}-page "
                      f"cap, so the {info['pages']} page(s) read were discarded, not truncated")
            self._append_failure({
                "event": "skipped_length_actual",
                "slug": slug,
                "forecast_pages": entry["forecast_pages"],
                "page_count_reported": info.get("page_count_reported"),
                "pages_read_before_cap": info["pages"],
                "items_discarded": info["discarded_items"],
            })
        elif outcome == "discarded_over_tolerance":
            # decisions/0012. Every page was read; the residual was too large to
            # be the known header artefact. Discarded, logged, never truncated,
            # and its own outcome — never folded into `unavailable`, into a skip
            # or into an error, and never represented as an empty result.
            detail = (
                f"read all {info.get('page_count_reported')} page(s) and accumulated "
                f"{info.get('accumulated_records')} records against a reported item "
                f"count of {info.get('item_count_reported')} "
                f"(residual {info.get('item_count_residual')}), beyond the "
                f"{self.residual_tolerance:.1%} tolerance; the sweep was discarded, "
                f"not truncated"
            )
            self._append_failure({
                "event": "discarded_over_tolerance",
                "slug": slug,
                "forecast_pages": entry["forecast_pages"],
                "page_count_reported": info.get("page_count_reported"),
                "pages_read": info["pages"],
                "accumulated_records": info.get("accumulated_records"),
                "item_count_reported": info.get("item_count_reported"),
                "item_count_residual": info.get("item_count_residual"),
                "residual_tolerance": self.residual_tolerance,
                "items_discarded": info["discarded_items"],
            })
        elif outcome in ("unavailable", "access_denied"):
            detail = f"fetch_all outcome {info['outcome']}; no history was seen"
            self._append_failure({
                "event": outcome,
                "slug": slug,
                "forecast_pages": entry["forecast_pages"],
                "pages_read": info["pages"],
                "items_discarded": info["discarded_items"],
            })

        row = self._record(
            entry, outcome,
            live_calls=live,
            cache_hits=cached,
            pages_read=info["pages"],
            page_count_reported=info.get("page_count_reported"),
            item_count_reported=info.get("item_count_reported"),
            # Named for what it is. The tolerance is applied to this and to
            # nothing else; the de-duplicated figure lives under `parse`.
            item_count_residual=info.get("item_count_residual"),
            residual_basis="accumulated_records",
            accumulated_records=info.get("accumulated_records"),
            residual_tolerance=self.residual_tolerance,
            reconcile=info.get("reconcile"),
            items_discarded=info["discarded_items"],
            first_page_fetched_at=first_fetch,
            last_page_fetched_at=last_fetch,
            parsed_path=str(parsed_path) if parsed_path else None,
            records=records,
            seconds=round(time.time() - started, 2),
            parse=parse_stats or None,
            detail=detail,
        )
        self._append_ledger(row)
        if outcome == "complete":
            self.consecutive_errors = 0
            self.consecutive_over_tolerance = 0
        elif outcome == "discarded_over_tolerance":
            self.consecutive_over_tolerance += 1
        return row

    def _record_user_error(
        self, entry: dict[str, Any], outcome: str, exc: Exception,
        calls_before: int, cache_before: int,
    ) -> dict[str, Any]:
        live = self.client.counters["requests_sent"] - calls_before
        cached = self.client.counters["served_from_cache"] - cache_before
        # A discard is not an error and must not move the error breaker; it has
        # its own tripwire. decisions/0012.
        if outcome in ERROR_OUTCOMES:
            self.consecutive_errors += 1
        elif outcome == "discarded_over_tolerance":
            self.consecutive_over_tolerance += 1
        row = self._record(
            entry, outcome,
            live_calls=live,
            cache_hits=cached,
            detail=f"{type(exc).__name__}: {str(exc)[:400]}",
        )
        self._append_ledger(row)
        self._append_failure({
            "event": outcome,
            "slug": entry["slug"],
            "forecast_pages": entry["forecast_pages"],
            "error_type": type(exc).__name__,
            "error_detail": str(exc)[:800],
            "live_calls": live,
            "note": ("recorded as terminal so an unattended run cannot loop on it; "
                     "re-attempt with --retry-errors"),
        })
        return row

    # -- the run -----------------------------------------------------------

    def _live_calls_this_run(self) -> int:
        return self.client.counters["requests_sent"] - self.calls_at_start

    def _should_stop(self) -> str | None:
        if self.max_users is not None and self.users_attempted_this_run >= self.max_users:
            return f"reached --max-users {self.max_users}"
        if self.max_calls is not None and self._live_calls_this_run() >= self.max_calls:
            return f"reached --max-calls {self.max_calls}"
        if self.consecutive_errors >= MAX_CONSECUTIVE_USER_ERRORS:
            self.abnormal_stop = True
            return (f"{self.consecutive_errors} consecutive per-user failures; stopping "
                    f"rather than spending more calls on a systemic fault")
        if self.consecutive_over_tolerance >= MAX_CONSECUTIVE_OVER_TOLERANCE:
            self.abnormal_stop = True
            return (f"{self.consecutive_over_tolerance} consecutive users discarded for "
                    f"an out-of-tolerance residual; that is a systemic fault, not a "
                    f"property of the users, and it would otherwise discard the pool "
                    f"one benign-looking user at a time")
        if in_sabbath(datetime.now().astimezone(), self.sabbath_window):
            return "entered the configured Sabbath window; stopped at a user boundary"
        return None

    def run(self) -> None:
        if in_sabbath(datetime.now().astimezone(), self.sabbath_window):
            self.stop_reason = "refused to start: inside the configured Sabbath window"
            print(self.stop_reason)
            return

        self.write_order()
        self.write_progress()
        decided = self.latest_outcomes()

        # decisions/0010 (a) first: zero calls, and it puts the skipped-for-
        # length users in the ledger up front rather than at whatever point the
        # run happens to reach them.
        for entry in self.plan["over_cap"]:
            if entry["slug"] in decided or entry["slug"] in self.exclude_slugs:
                continue
            self.pull_user(entry)
        decided = self.latest_outcomes()

        consecutive_deferrals = 0
        for entry in self.plan["order"]:
            # Out of scope for this run by instruction. Left undecided on
            # purpose: no ledger row, no outcome, no state change at all.
            if entry["slug"] in self.exclude_slugs:
                self.excluded_this_run.append(entry["slug"])
                continue
            prior = decided.get(entry["slug"])
            if prior is not None:
                if prior["outcome"] not in self.retry_outcomes:
                    continue
            stop = self._should_stop()
            if stop:
                self.stop_reason = stop
                break
            # Do not start a sweep the remaining budget plainly cannot cover.
            # A forecast is not a promise, so the budget_pages guard inside the
            # sweep is what actually bounds the spend; this only avoids the
            # obviously wasted first page. Deferral is not a decision about the
            # user, so it is not written to the ledger.
            if self.max_calls is not None:
                remaining = self.max_calls - self._live_calls_this_run()
                if remaining < entry["forecast_pages"]:
                    consecutive_deferrals += 1
                    self.deferred_this_run.append({
                        "slug": entry["slug"],
                        "forecast_pages": entry["forecast_pages"],
                        "reason": "forecast exceeds the remaining run budget; not started",
                        "remaining_calls": remaining,
                    })
                    if consecutive_deferrals >= MAX_CONSECUTIVE_DEFERRALS:
                        self.stop_reason = (
                            f"{consecutive_deferrals} users in a row did not fit the "
                            f"remaining call budget; stopping rather than walking the "
                            f"rest of the plan"
                        )
                        break
                    continue
            consecutive_deferrals = 0
            self.users_attempted_this_run += 1
            row = self.pull_user(entry)
            self._save_state()
            self.write_progress()
            rank = row.get("pull_rank")
            print(f"  {rank if rank is not None else '-':>5} bin {entry.get('bin')} "
                  f"forecast {entry['forecast_pages']:>4}  "
                  f"actual {row.get('page_count_reported')}  "
                  f"{row['outcome']}  live={row.get('live_calls')}  "
                  f"records={row.get('records')}")
        self.stop_reason = self.stop_reason or "plan exhausted"
        if self.deferred_this_run:
            _atomic_write_text(
                self.deferred_path,
                "".join(json.dumps(d, sort_keys=True) + "\n" for d in self.deferred_this_run),
            )
        self._save_state()
        self.write_progress()

    # -- reporting ---------------------------------------------------------

    def classification_counts(self) -> dict[str, Any]:
        """decisions/0012's three behaviours, aggregated, and kept apart.

        Explicitly required: the tolerance must not silently absorb three
        different phenomena. So each is counted on its own, over users AND over
        records where records make sense, and the categories are NOT treated as
        mutually exclusive — `users_with_both_a_header_residual_and_duplicates`
        is reported precisely because a user can be in two of them.
        """
        rows = [r for r in self.latest_outcomes().values() if r["outcome"] == "complete"]
        cls = [(r.get("parse") or {}).get("classification") or {} for r in rows]
        measured = [c for c in cls if isinstance(c.get("residual_on_accumulated"), int)]
        attributable = [c for c in cls if c.get("page_attribution_available")]
        dup_users = [c for c in attributable if (c.get("cross_page_duplicate_ids") or 0) > 0]
        over = [c for c in measured if c["residual_on_accumulated"] < 0]
        under = [c for c in measured if c["residual_on_accumulated"] > 0]
        exact = [c for c in measured if c["residual_on_accumulated"] == 0]
        both = [
            c for c in dup_users
            if isinstance(c.get("residual_on_accumulated"), int)
            and c["residual_on_accumulated"] != 0
        ]
        return {
            "users_classified": len(cls),
            "users_with_a_measurable_residual": len(measured),
            "header_over_count": {
                "definition": "accumulated records < X-Pagination-Item-Count",
                "status": "benign for this study",
                "users": len(over),
                "records_the_header_over_claimed": sum(
                    -c["residual_on_accumulated"] for c in over),
            },
            "header_under_count": {
                "definition": "accumulated records > X-Pagination-Item-Count",
                "status": "benign, and in the safe direction",
                "users": len(under),
                "records_beyond_the_header": sum(
                    c["residual_on_accumulated"] for c in under),
            },
            "header_exact": {"users": len(exact)},
            "cross_page_duplicate_records": {
                "definition": "the same record id returned on more than one page",
                "status": ("real data behaviour, not a header artefact; handled "
                           "downstream by Step 1 §2.2 distinct-episode counting, "
                           "reported here rather than absorbed"),
                "users_with_page_attribution": len(attributable),
                "affected_users": len(dup_users),
                "affected_records": sum(
                    int(c.get("cross_page_duplicate_records") or 0) for c in attributable),
                "affected_record_ids": sum(
                    int(c.get("cross_page_duplicate_ids") or 0) for c in attributable),
                "max_affected_records_on_one_user": max(
                    (int(c.get("cross_page_duplicate_records") or 0) for c in attributable),
                    default=0),
            },
            "within_page_duplicate_records": {
                "definition": "the same record id twice on the SAME page",
                "affected_records": sum(
                    int(c.get("within_page_duplicate_records") or 0) for c in attributable),
            },
            "users_with_both_a_header_residual_and_duplicates": len(both),
            "not_mutually_exclusive": (
                "a user can be a header over- or under-count AND carry cross-page "
                "duplicates; each category counts it, and the overlap is given above"
            ),
            "totals": {
                "accumulated_records": sum(
                    int(c.get("accumulated_records") or 0) for c in cls),
                "distinct_record_ids": sum(
                    int(c.get("distinct_record_ids") or 0) for c in cls),
                "duplicate_records_total": sum(
                    int(c.get("duplicate_records_total") or 0) for c in cls),
                "records_missing_an_id": sum(
                    int(c.get("records_missing_an_id") or 0) for c in cls),
            },
        }

    def residual_distribution(self) -> dict[str, Any]:
        """The residual distribution across the pool, per decisions/0012, so the
        2 percent tolerance is judged against what was observed.

        Covers users the rule ACCEPTED and users it DISCARDED, because a
        distribution that only shows the survivors cannot say whether the
        threshold is in the right place. The residual is on accumulated
        records, everywhere.
        """
        rows = [
            r for r in self.latest_outcomes().values()
            if r["outcome"] in ("complete", "discarded_over_tolerance")
            and isinstance(r.get("item_count_residual"), int)
            and isinstance(r.get("item_count_reported"), int)
        ]
        signed = sorted(r["item_count_residual"] for r in rows)
        shares = sorted(
            abs(r["item_count_residual"]) / r["item_count_reported"]
            for r in rows if r["item_count_reported"]
        )

        def pct(values: list[Any], p: float) -> Any:
            if not values:
                return None
            idx = min(len(values) - 1, max(0, int(round((p / 100.0) * (len(values) - 1)))))
            return values[idx]

        # Bands on |residual| / item_count, so the tolerance can be read off
        # against the observed mass rather than against ten users.
        edges = [0.0, 0.0001, 0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 1.0]
        bands: dict[str, int] = {}
        for i in range(len(edges) - 1):
            lo, hi = edges[i], edges[i + 1]
            label = f"{lo:.4%}-{hi:.4%}" if i else "exactly 0"
            bands[label] = sum(
                1 for s in shares
                if (s == 0 if i == 0 else lo < s <= hi)
            )
        # The band an absolute ±1 floor would have rescued. Reported, not
        # adopted: widening the rule is the Human Lead's call.
        floor_band = sum(
            1 for r in rows
            if r["item_count_reported"]
            and 0 < abs(r["item_count_residual"]) <= 1
            and abs(r["item_count_residual"]) > self.residual_tolerance * r["item_count_reported"]
        )
        return {
            "basis": "accumulated records minus X-Pagination-Item-Count",
            "users_measured": len(rows),
            "includes_discarded_users": True,
            "signed_residual": {
                "min": signed[0] if signed else None,
                "p05": pct(signed, 5),
                "median": pct(signed, 50),
                "p95": pct(signed, 95),
                "max": signed[-1] if signed else None,
                "negative_header_over_count": sum(1 for s in signed if s < 0),
                "zero": sum(1 for s in signed if s == 0),
                "positive_header_under_count": sum(1 for s in signed if s > 0),
            },
            "abs_share_of_item_count": {
                "median": round(pct(shares, 50), 6) if shares else None,
                "p90": round(pct(shares, 90), 6) if shares else None,
                "p95": round(pct(shares, 95), 6) if shares else None,
                "p99": round(pct(shares, 99), 6) if shares else None,
                "max": round(shares[-1], 6) if shares else None,
                "tolerance": self.residual_tolerance,
                "users_within_tolerance": sum(
                    1 for s in shares if s <= self.residual_tolerance),
                "users_over_tolerance": sum(
                    1 for s in shares if s > self.residual_tolerance),
            },
            "bands_by_abs_share": bands,
            "residual_within_one_but_over_tolerance": floor_band,
            "residual_within_one_note": (
                "users a ±1 absolute floor would have rescued. The rule as adopted "
                "has no such floor. Reported so the Human Lead can see what a floor "
                "would buy; not adopted here."
            ),
        }

    def counts(self) -> dict[str, Any]:
        latest = self.latest_outcomes()
        by_outcome = Counter(row["outcome"] for row in latest.values())
        complete_rows = [r for r in latest.values() if r["outcome"] == "complete"]
        fetch_firsts = sorted(
            r["first_page_fetched_at"] for r in latest.values()
            if r.get("first_page_fetched_at"))
        fetch_lasts = sorted(
            r["last_page_fetched_at"] for r in latest.values()
            if r.get("last_page_fetched_at"))
        forecast_err = [
            {
                "forecast": r["forecast_pages"],
                "actual": r["page_count_reported"],
            }
            for r in latest.values()
            if isinstance(r.get("page_count_reported"), int)
        ]
        ratios = [e["actual"] / e["forecast"] for e in forecast_err if e["forecast"]]
        residuals = [
            (r["item_count_residual"], r["item_count_reported"])
            for r in latest.values()
            if isinstance(r.get("item_count_residual"), int)
            and isinstance(r.get("item_count_reported"), int)
            and r["item_count_reported"]
        ]
        shares = [abs(res) / total for res, total in residuals]
        by_channel = Counter(
            (r.get("channel_first"), r["outcome"]) for r in latest.values())
        return {
            "users_in_pool_usable": self.plan["usable_users"],
            "users_eligible_after_forecast_cap": self.plan["eligible_users"],
            "users_decided": len(latest),
            "by_outcome": dict(by_outcome),
            "outcomes_sum_to_decided": sum(by_outcome.values()) == len(latest),
            "skipped_length_forecast": by_outcome.get("skipped_length_forecast", 0),
            "skipped_length_actual": by_outcome.get("skipped_length_actual", 0),
            "pages_read_total": sum(int(r.get("pages_read") or 0) for r in latest.values()),
            "live_calls_recorded_all_runs": self.live_calls_recorded(),
            "live_calls_this_run": self._live_calls_this_run(),
            "records_parsed": sum(int(r.get("records") or 0) for r in complete_rows),
            "episode_records": sum(
                int(((r.get("parse") or {}).get("episode_records")) or 0)
                for r in complete_rows),
            "movie_records": sum(
                int(((r.get("parse") or {}).get("movie_records")) or 0)
                for r in complete_rows),
            "duplicate_record_ids": sum(
                int(((r.get("parse") or {}).get("duplicate_record_ids")) or 0)
                for r in complete_rows),
            "earliest_first_page_fetched_at": fetch_firsts[0] if fetch_firsts else None,
            "latest_last_page_fetched_at": fetch_lasts[-1] if fetch_lasts else None,
            "forecast_error": {
                "users_with_actual_page_count": len(ratios),
                "mean_actual_over_forecast": round(sum(ratios) / len(ratios), 3) if ratios else None,
                "max_actual_over_forecast": round(max(ratios), 3) if ratios else None,
                "min_actual_over_forecast": round(min(ratios), 3) if ratios else None,
                "users_where_actual_exceeds_forecast": sum(1 for r in ratios if r > 1.0),
            },
            "item_count_residual": {
                "users_measured": len(residuals),
                "users_with_a_nonzero_residual": sum(1 for r, _ in residuals if r != 0),
                "max_abs_share_of_item_count": round(max(shares), 5) if shares else None,
                "note": (
                    "accumulated records minus X-Pagination-Item-Count. On "
                    "/users/:id/history the header is not an exact count of the "
                    "records the API returns; the pilot proved this by getting the "
                    "identical record set at two page sizes while the header "
                    "disagreed with both."
                ),
            },
            "header_and_duplicate_classification": self.classification_counts(),
            "residual_distribution": self.residual_distribution(),
            "completeness_rule": self.reconcile,
            "residual_tolerance": self.residual_tolerance,
            "by_channel_outcome": {f"{c}|{o}": n for (c, o), n in by_channel.items()},
            "deferred_this_run": len(self.deferred_this_run),
        }


def _safe_name(slug: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", slug)[:120]


# ---------------------------------------------------------------------------
# run record, pull log, artifact
# ---------------------------------------------------------------------------


def write_pull_log(puller: Step4Puller, path: Path | None = None) -> Path:
    """logs/step4_pull_log.json — success, private and error counts, per Step 4's
    deliverable. Carries no usernames: the per-user detail is in processed/."""
    latest = puller.latest_outcomes()
    by_outcome = Counter(row["outcome"] for row in latest.values())
    record = {
        "generated_at": utcnow(),
        "run_id": puller.run_id,
        "success": by_outcome.get("complete", 0),
        "private_or_absent": by_outcome.get("unavailable", 0),
        "access_denied": by_outcome.get("access_denied", 0),
        "skipped_length_forecast": by_outcome.get("skipped_length_forecast", 0),
        "skipped_length_actual": by_outcome.get("skipped_length_actual", 0),
        # decisions/0012: reported separately from every other skip and failure
        # category, and never merged into one of them.
        "discarded_over_tolerance": by_outcome.get("discarded_over_tolerance", 0),
        "errors": sum(by_outcome.get(o, 0) for o in ERROR_OUTCOMES),
        "errors_by_kind": {o: by_outcome.get(o, 0) for o in ERROR_OUTCOMES},
        "deferred_not_decided": len(puller.deferred_this_run),
        "counts": puller.counts(),
    }
    text = json.dumps(record, indent=2, default=str)
    target = path or (LOGS_DIR / "step4_pull_log.json")
    puller.client._refuse_if_secret(text, str(target))
    _atomic_write_text(target, text)
    return target


def write_run_record(
    puller: Step4Puller,
    client: TraktClient,
    error: dict[str, Any] | None,
    exit_code: int,
    path: Path | None = None,
) -> Path:
    record = {
        "started_at": puller.started_at,
        "finished_at": utcnow(),
        "run_id": puller.run_id,
        "exit_code": exit_code,
        "exit_meaning": EXIT_MEANINGS.get(exit_code, "unknown"),
        "stop_reason": puller.stop_reason,
        "error": error,
        "plan": {
            "source": str(puller.pool_path),
            "page_limit": puller.page_limit,
            "page_cap": puller.page_cap,
            "n_bins": puller.plan["n_bins"],
            "usable_users": puller.plan["usable_users"],
            "eligible_users": puller.plan["eligible_users"],
            "skipped_forecast_users": puller.plan["skipped_forecast_users"],
            "skipped_forecast_pages": puller.plan["skipped_forecast_pages"],
            "eligible_forecast_pages": puller.plan["eligible_forecast_pages"],
            "bin_sizes": puller.plan["bin_sizes"],
            "bin_forecast_ranges": puller.plan["bin_forecast_ranges"],
        },
        "bounds": {
            "max_users": puller.max_users,
            "max_calls": puller.max_calls,
            # A scope bound set for this run, not a study rule. Counts only:
            # this file is read alongside artifacts, so no slug goes in it.
            "users_placed_out_of_scope": len(puller.exclude_slugs),
            "users_skipped_as_out_of_scope": len(puller.excluded_this_run),
        },
        "proportionality": verify_prefix_proportionality(puller.plan),
        "counts": puller.counts(),
        "client_counters": client.summary(),
        "throttle": client.throttle.spent(),
    }
    text = json.dumps(client._redact(record), indent=2, default=str)
    target = path or (LOGS_DIR / "step4_run.json")
    client._refuse_if_secret(text, str(target))
    _atomic_write_text(target, text)
    return target


def names_in(payload: Any, names: set[str]) -> list[str]:
    """Privacy guard for anything bound for artifacts/.

    Same three tests Step 3 used: exact string match against the name set,
    identifier-shaped tokens of ten characters or more, and any `users/<seg>`
    path. A bare substring sweep is useless because the pool holds slugs that
    are ordinary English words.
    """
    strings: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(key, str):
                    strings.add(key)
                walk(value)
        elif isinstance(node, (list, tuple)):
            for value in node:
                walk(value)
        elif isinstance(node, str):
            strings.add(node)

    if isinstance(payload, str):
        blob = payload
    else:
        walk(payload)
        blob = json.dumps(payload, default=str)
    found = set(strings) & names
    found |= {t for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9_.\-]{9,}", blob)} & names
    found |= {unquote(s) for s in re.findall(r"users/([^/\s\"']+)", blob)} & names
    return sorted(found)


def pool_names(puller: Step4Puller) -> set[str]:
    names: set[str] = set()
    for entry in puller.plan["order"] + puller.plan["over_cap"]:
        if entry.get("slug"):
            names.add(entry["slug"])
        if entry.get("username"):
            names.add(entry["username"])
    return names


def write_artifact(puller: Step4Puller, label: str = "pilot") -> list[Path]:
    """artifacts/ gets counts and aggregates only, and it is checked."""
    counts = puller.counts()
    plan = puller.plan
    prop = verify_prefix_proportionality(plan)
    ranks = sorted(r["pull_rank"] for r in puller.latest_outcomes().values()
                   if r.get("pull_rank") is not None)
    k = len(ranks)
    contiguous = bool(ranks) and ranks == list(range(k))
    dist = prefix_page_distribution(plan, k)

    payload = {
        "step": 4,
        "label": label,
        "generated_at": utcnow(),
        "source_decisions": ["0002", "0004", "0009", "0010", "0011", "0012"],
        "page_limit": puller.page_limit,
        "page_cap": puller.page_cap,
        "completeness_rule": {
            "rule": puller.reconcile,
            "residual_tolerance": puller.residual_tolerance,
            "decision": "decisions/0012, adopted by the Human Lead 2026-08-11",
            "test": ("every page reported by X-Pagination-Page-Count read, headers "
                     "steady across the sweep, and |accumulated - "
                     "X-Pagination-Item-Count| within the tolerance"),
            "residual_basis": "accumulated records, never de-duplicated ones",
            "outside_the_tolerance": ("discarded and logged under its own outcome "
                                      "`discarded_over_tolerance`; never truncated, "
                                      "never folded into unavailable, a skip or an "
                                      "error, never an empty result"),
        },
        "plan": {
            "usable_users": plan["usable_users"],
            "eligible_users": plan["eligible_users"],
            "skipped_forecast_users": plan["skipped_forecast_users"],
            "skipped_forecast_pages": plan["skipped_forecast_pages"],
            "eligible_forecast_pages": plan["eligible_forecast_pages"],
            "bin_sizes": plan["bin_sizes"],
            "bin_forecast_ranges": plan["bin_forecast_ranges"],
        },
        "proportionality": prop,
        "realized_page_distribution": {
            "users_decided_in_order": k,
            "decided_set_is_a_contiguous_prefix_of_the_order": contiguous,
            "pulled_prefix": dist["prefix"],
            "eligible_pool": dist["eligible_pool"],
            "prefix_bin_counts": {str(b): n
                                  for b, n in sorted(dist["prefix_bin_counts"].items())},
        },
        "counts": counts,
        "pull_date_D11": {
            "pull_date": PULL_DATE,
            "tau_pull": TAU_PULL,
            "source": "decisions/0011, set by the Human Lead 2026-08-11",
            "earliest_first_page_fetched_at": counts["earliest_first_page_fetched_at"],
            "latest_last_page_fetched_at": counts["latest_last_page_fetched_at"],
            "constraint_pull_date_no_later_than_earliest_fetch": (
                _as_instant(counts["earliest_first_page_fetched_at"]) is None
                or _as_instant(TAU_PULL)
                <= _as_instant(counts["earliest_first_page_fetched_at"])
            ),
            "note": (
                "D11 constrains pull_date to be no later than the earliest per-user "
                "fetch date. The first-page timestamp is the conservative anchor: "
                "history returns newest-first, so a sweep is known complete only for "
                "records older than the instant it started. Records at or after "
                "tau_pull are discarded at Step 8, not here: this step does not "
                "filter the pull."
            ),
        },
        "stop_reason": puller.stop_reason,
    }

    names = pool_names(puller)
    leaked = names_in(payload, names)
    if leaked:
        raise RuntimeError(
            f"refusing to write {len(leaked)} pool name(s) to artifacts/: {leaked[:5]}")

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = ARTIFACTS_DIR / f"step4-{label}-counts.json"
    text = json.dumps(payload, indent=2, default=str)
    puller.client._refuse_if_secret(text, str(json_path))
    _atomic_write_text(json_path, text)
    return [json_path]


# ---------------------------------------------------------------------------


def print_status(path: Path | None = None) -> int:
    """Poll an unattended run without attaching to it. Makes no calls, opens no
    state, and never writes."""
    target = path or (LOGS_DIR / "step4_progress.json")
    if not target.exists():
        print(f"no progress file at {target}")
        return 1
    payload = json.loads(target.read_text(encoding="utf-8"))
    pid = payload.get("pid")
    alive = False
    if isinstance(pid, int):
        try:
            os.kill(pid, 0)   # signal 0: existence check, sends nothing
            alive = True
        except OSError:
            alive = False
    print(json.dumps(payload, indent=2, default=str))
    print(f"\npid {pid} alive: {alive}")
    if payload.get("finished"):
        print(f"finished: {payload.get('stop_reason')}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Step 4 watch-history pull")
    parser.add_argument("--state-dir", default=None)
    parser.add_argument("--pool", default=str(POOL_PATH))
    parser.add_argument("--max-users", type=int, default=None)
    parser.add_argument("--max-calls", type=int, default=None,
                        help="bound on LIVE calls this run; cached pages are free")
    parser.add_argument("--page-cap", type=int, default=PAGE_CAP)
    parser.add_argument("--retry-errors", action="store_true",
                        help="re-decide users whose latest outcome is an error")
    parser.add_argument("--retry-outcomes", default=None,
                        help="comma-separated terminal outcomes to re-decide. Cached "
                             "pages make this free; nothing already on disk is "
                             "re-requested. Default: none.")
    parser.add_argument("--completeness-rule", choices=("exact", "page_count"),
                        default=COMPLETENESS_RULE,
                        help="'page_count' is the ADOPTED rule (decisions/0012, Human "
                             "Lead, 2026-08-11) and the default. 'exact' is the "
                             "superseded rule, kept because Step 0's and Step 3's "
                             "evidence was gathered under it.")
    parser.add_argument("--residual-tolerance", type=float, default=RESIDUAL_TOLERANCE,
                        help="only meaningful with --completeness-rule page_count")
    parser.add_argument("--status", action="store_true",
                        help="print logs/step4_progress.json and whether its pid is "
                             "alive, then exit. Makes no calls and touches no state.")
    parser.add_argument("--sabbath", default=DEFAULT_SABBATH_WINDOW,
                        help="local window in which the pull will not run, or 'off'")
    parser.add_argument("--artifact", default=None,
                        help="write artifacts/step4-<label>-counts.json")
    parser.add_argument("--plan-only", action="store_true",
                        help="build and verify the pull order; make no calls")
    parser.add_argument("--exclude-slugs-file", default=None,
                        help="path to a newline-delimited list of slugs this run "
                             "must not touch. They are left UNDECIDED: no ledger "
                             "row, no outcome, no state change. A scope bound on "
                             "one run, never a study rule. The file carries user "
                             "identifiers, so it belongs in processed/, and the "
                             "flag exists so no slug is ever typed into a code "
                             "file or a command line.")
    args = parser.parse_args(argv)

    if args.status:
        return print_status()

    exclude_slugs: list[str] = []
    if args.exclude_slugs_file:
        exclude_slugs = [
            line.strip()
            for line in Path(args.exclude_slugs_file).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]

    client = TraktClient(run_label="step4_history_pull")
    puller = Step4Puller(
        client,
        state_dir=Path(args.state_dir) if args.state_dir else None,
        pool_path=Path(args.pool),
        page_cap=args.page_cap,
        max_users=args.max_users,
        max_calls=args.max_calls,
        retry_errors=args.retry_errors,
        retry_outcomes=[s.strip() for s in args.retry_outcomes.split(",") if s.strip()]
        if args.retry_outcomes else None,
        sabbath_window=parse_sabbath_window(args.sabbath),
        reconcile=args.completeness_rule,
        residual_tolerance=args.residual_tolerance,
        exclude_slugs=exclude_slugs,
    )

    if args.plan_only:
        puller.write_order()
        report = {
            "plan": {k: v for k, v in puller.plan.items() if k not in ("order", "over_cap")},
            "proportionality": verify_prefix_proportionality(puller.plan),
            "first_cycle_forecast_pages": sum(
                e["forecast_pages"] for e in puller.plan["order"][:puller.plan["n_bins"]]),
        }
        print(json.dumps(report, indent=2, default=str))
        return EXIT_OK

    error: dict[str, Any] | None = None
    exit_code = EXIT_OK
    try:
        puller.run()
        if puller.abnormal_stop:
            # A tripwire fired. It is not a committed stopping rule and it must
            # not look like a clean finish to whatever is watching the exit
            # code of a 22-hour unattended run.
            error = {"type": "SystemicStop", "detail": puller.stop_reason}
            exit_code = EXIT_SYSTEMIC_STOP
            print(f"\n*** {puller.stop_reason}", file=sys.stderr)
    except AccessBlocked as exc:
        puller.stop_reason = "HARD STOP: 403 classified as an application-level block"
        error = {"type": "AccessBlocked", "detail": str(exc)[:2000]}
        exit_code = EXIT_ACCESS_BLOCKED
        print(f"\n*** {puller.stop_reason}\n{exc}", file=sys.stderr)
    except RateLimitPersistent as exc:
        puller.stop_reason = "HARD STOP: 429s persisted beyond the configured budget"
        error = {"type": "RateLimitPersistent", "detail": str(exc)[:2000]}
        exit_code = EXIT_RATE_LIMIT_PERSISTENT
        print(f"\n*** {puller.stop_reason}\n{exc}", file=sys.stderr)
    except TransientFailure as exc:
        puller.stop_reason = "HARD STOP: transient backoff exhausted"
        error = {"type": "TransientFailure", "detail": str(exc)[:2000]}
        exit_code = EXIT_TRANSIENT_EXHAUSTED
        print(f"\n*** {puller.stop_reason}\n{exc}", file=sys.stderr)
    except KeyboardInterrupt:
        puller.stop_reason = "interrupted"
        error = {"type": "KeyboardInterrupt", "detail": None}
        exit_code = EXIT_INTERRUPTED
        print("\ninterrupted; the user in progress was not written to the ledger",
              file=sys.stderr)
    except TraktClientError as exc:
        puller.stop_reason = f"HARD STOP: {type(exc).__name__}"
        error = {"type": type(exc).__name__, "detail": str(exc)[:2000]}
        exit_code = EXIT_CLIENT_ERROR
        print(f"\n*** {puller.stop_reason}\n{exc}", file=sys.stderr)
    except Exception as exc:  # noqa: BLE001
        puller.stop_reason = f"HARD STOP: unexpected {type(exc).__name__}"
        error = {"type": type(exc).__name__, "detail": str(exc)[:2000]}
        exit_code = EXIT_UNEXPECTED
        print(f"\n*** {puller.stop_reason}\n{exc}", file=sys.stderr)
    finally:
        try:
            puller._save_state()
            write_pull_log(puller)
            if args.artifact:
                write_artifact(puller, args.artifact)
        except Exception as exc:  # noqa: BLE001
            error = error or {}
            error["final_write_failed"] = f"{type(exc).__name__}: {exc}"[:500]
            if exit_code == EXIT_OK:
                exit_code = EXIT_UNEXPECTED
        record_path = write_run_record(puller, client, error, exit_code)

    print(f"\nrun record: {record_path}")
    print(f"exit {exit_code} ({EXIT_MEANINGS.get(exit_code)})")
    print(json.dumps(puller.counts(), indent=2, default=str))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
