"""Step 3: user discovery. Two channels, tagged, resumable, budget-capped.

THE PLAN, COMMITTED BEFORE THE RUN
==================================

Channel A - follower graph
--------------------------
Seeds: ~300 public profiles taken from authors of recent/trending/updated
comments on MOVIES. Movies cannot be in the Step 2 frame (the frame is TV shows
with two or more seasons), so this harvests nothing from comments on any show
being measured and cannot select on the outcome. It is adjacent to a
prohibition, so `seed_source` and `depth` are recorded per user and depth-0
users can be excluded wholesale at Step 11 if the Human Lead wants that.

Expansion: breadth-first over BOTH `users/:id/followers` and
`users/:id/following`. Outbound follows reach different communities than
inbound ones, so using both widens the walk.

Anti-clique measures, all chosen in advance because a follower walk from a
small seed set converges on one community if left alone:
  1. 300 seeds, not a handful, spread over many different movies.
  2. At most 100 neighbours taken per expanded user (page 1 at limit=100).
     A hub with 4,296 followers therefore contributes no more than 100.
  3. The frontier is round-robined ACROSS ORIGIN SEEDS, so no single seed's
     subtree can consume the expansion budget.
  4. Depth capped at 3.
  5. origin_seed, depth, parent, edge type and degree are recorded per user in
     raw/ so Step 11 can test whether the pool is one clique.

Channel B - public list owners
------------------------------
`lists/trending` and `lists/popular`, paged at limit=100. Both report the same
20,211-list universe, so they are two orderings of one pool and are deduped by
list id. Each record embeds its owning user.

Usable user
-----------
Defined operationally, because "usable-user yield" needs it fixed in advance:
  (a) not `deleted`, and
  (b) not `private`, and
  (c) confirmed by a 200 from `users/:id/stats` with `episodes.watched >= 10`.
(a) and (b) are free - the follower and list payloads already carry both flags.
(c) costs one call per user. The floor of 10 episodes is deliberately far below
anything the study needs: a user with fewer than 10 episodes logged cannot have
completed any season 1, so this pre-applies the frame rather than biasing it.

Yield curve
-----------
Measured against DISCOVERY calls only, never against screening calls. Screening
costs ~1 call per user and returns ~0.75 usable users no matter how saturated
the graph is, so folding it into the denominator would flatten the curve by
construction and hide the very plateau we are looking for.

  y_r = (new distinct usable-ELIGIBLE users found in round r) / (discovery calls in round r)

where usable-eligible = unseen, not deleted, not private. That quantity is
exact and free on every round.

Stopping rule, all three committed in advance
---------------------------------------------
  1. PLATEAU. Let M_k be the 3-round moving average of y and P_k its running
     peak. Stop when, after at least 10 rounds, M_k <= 0.20 * P_k on two
     CONSECUTIVE rounds. Two rounds, not one, so a single noisy round cannot
     stop the run. 20 percent of peak means we are paying 5x as many calls per
     new usable user as at the best point observed.
  2. SUFFICIENCY. Stop at TARGET_USABLE confirmed-usable users. This is a real
     stopping argument and not a budget dodge: the study needs user-show pairs,
     each user contributes several, and Step 11 splits by channel and Step 12
     by segment. A few thousand users is ample for all of that, while every
     additional user costs Step 4 roughly ceil(total_plays/250) more calls.
  3. BUDGET. A hard cap on Step 3 live calls.

Which rule actually fired is reported. If it is (2) or (3) while the yield
curve is still high, that is the finding: the follower graph does not saturate
at this scale, so pool size is a budget choice rather than a discovery limit.
Saying that plainly is worth more than manufacturing a plateau.

Privacy
-------
Usernames and user ids are written ONLY under raw/. The yield curve and the
run summary carry counts and aggregates and nothing else.

AMENDMENTS AFTER THE FIRST RUN (engineering review returned HOLD)
================================================================
The plan above is unchanged. None of the stopping thresholds, the seeding
strategy or the channel design is touched here. What changed is what the run
RECORDS and how it EXITS.

1. Exit codes. main() returned 0 after AccessBlocked and RateLimitPersistent,
   so `step3 && step4` read the two loudest failures as success, and an
   uncaught TransientFailure skipped logs/step3_run.json entirely. Now every
   terminal condition has a distinct non-zero code and the run record is
   written on every exit path, including the unexpected one.

2. Deliverables at round boundaries, not in a finally. user_pool.jsonl and
   yield_curve.jsonl are written after every round, temp-file-then-rename, so a
   SIGKILL can lose at most the round in progress and can never leave a
   truncated file that looks like a smaller complete pool.

3. Plateau vs stall. The round record carried nothing that could tell a
   saturating graph from a stalled machine. It now carries per-channel yield,
   frontier size and shape, expansion counts, neighbours returned and the dedup
   rate, and a full time decomposition: throttle sleep, 429 sleep, backoff
   sleep, time actually inside requests, the largest gap between consecutive
   requests, and whatever is left over as `unaccounted_seconds`. Round 8 of the
   first run recorded 2796 seconds with zero 429s; under this record that
   surfaces as one ~2650s gap with no rate-limit pauses, which is a suspended
   machine and reads nothing like throttling.

4. Step 4 forecast. It was recorded per user and never summed, and it was also
   WRONG: it divided `total_plays`, a field absent from 77 percent of
   users/:id/stats payloads (1827 of 2376 cached bodies), so most users
   forecast exactly one page. Where the field is present it equals
   episodes.plays + movies.plays exactly (549 of 549 bodies), so the forecast
   is now computed from that sum, which is always present, and aggregated with
   its distribution.

5. Interrupted rounds. expand_channel_a marked a user expanded BEFORE reading
   its edges and main()'s finally persisted the half-round, so a Ctrl-C left
   users permanently marked as expanded whose followers were never read. A
   round is now a transaction: it commits whole or it is journalled back out
   and recorded in `discarded_rounds`. Live call counters are deliberately NOT
   rolled back, because those calls really were spent.

6. A 403 is not a zero-follower user. A skipped 403 fell into
   `if not resp.ok: continue` and became indistinguishable from a user with no
   followers, which is the conflation decisions/0004-403-handling.md exists to
   prevent. Every expansion now carries a per-edge outcome. `access_denied_users`
   counted endpoints and counted cache replays; it is now a set of distinct
   user slugs, with endpoint-level hits counted separately under their own name.

7. Recorded for Step 11, which cannot be reconstructed once the budget is gone:
   the full edge list rather than the first parent only, seed provenance (feed,
   page, and the movie the comment was on), and Channel B provenance (trending
   vs popular, list id, and lists per owner).
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.parse import quote, unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))

from trakt_client import (  # noqa: E402
    AccessBlocked,
    RateLimitPersistent,
    TraktClient,
    TraktClientError,
    TransientFailure,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_STEP3 = PROJECT_ROOT / "raw" / "step3"
LOGS_DIR = PROJECT_ROOT / "logs"
ARTIFACTS = PROJECT_ROOT / "artifacts"

# -- the plan's numbers, in one place ---------------------------------------

N_SEEDS = 300
SEED_FEEDS = [
    ("comments/recent/all/movies", 4),
    ("comments/trending/all/movies", 4),
    ("comments/updates/all/movies", 4),
]
MAX_DEPTH = 3
NEIGHBOURS_PER_USER = 100          # page 1 at limit=100; hub contribution capped

EXPAND_USERS_PER_ROUND = 12        # 2 calls each -> 24 discovery calls
LIST_PAGES_PER_ROUND = 3           # 3 discovery calls
DISCOVERY_CALLS_PER_ROUND = EXPAND_USERS_PER_ROUND * 2 + LIST_PAGES_PER_ROUND
SCREEN_CALLS_PER_ROUND = 120

MIN_EPISODES_USABLE = 10

MIN_ROUNDS_BEFORE_PLATEAU = 10
PLATEAU_FRACTION_OF_PEAK = 0.20
PLATEAU_CONSECUTIVE_ROUNDS = 2

TARGET_USABLE = 4000
CALL_BUDGET = 6500
STEP4_PAGE_LIMIT = 250             # for the Step 4 page forecast

# A round whose wall-clock time is this much larger than the time it can account
# for (requests + throttle + 429 + backoff) is flagged. Not a stopping rule and
# it changes nothing the run decides: it exists so a reader at the checkpoint is
# not shown a suspended laptop and left to guess that it was throttling.
STALL_UNACCOUNTED_SECONDS = 60.0

# Exit codes. A chained `step3 && step4`, or any wrapper, must see the loud
# failures as failures. 0 is reserved for a run that stopped on one of its own
# three committed stopping rules.
EXIT_OK = 0
EXIT_ACCESS_BLOCKED = 2            # 403. A block, not a throttle.
EXIT_RATE_LIMIT_PERSISTENT = 3     # 429s persisted across pauses.
EXIT_TRANSIENT_EXHAUSTED = 4       # backoff attempts exhausted.
EXIT_CLIENT_ERROR = 5              # any other TraktClientError.
EXIT_UNEXPECTED = 6                # anything else, still with a run record.
EXIT_INTERRUPTED = 130             # Ctrl-C, by shell convention.


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write_text(path: Path, text: str) -> None:
    """Temp-file-then-rename. The rename is atomic on POSIX, so a reader (or a
    kill) sees either the previous complete file or the new complete file and
    never a truncated prefix that would pass for a smaller complete file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def user_slug_from_endpoint(endpoint: str) -> str | None:
    """`users/<slug>/followers` -> `<slug>`. Used so a 403 can be counted
    against the user it denied rather than against each endpoint separately."""
    parts = [p for p in endpoint.strip("/").split("/") if p]
    if len(parts) < 2 or parts[0].lower() != "users":
        return None
    return unquote(parts[1])


class _RoundJournal:
    """Undo log making one round all-or-nothing.

    The first run marked a user expanded before reading its edges and persisted
    whatever a Ctrl-C happened to catch, so an interrupted round left users
    permanently marked expanded whose followers were never read. Resume never
    revisited them and the pool looked complete while missing those subtrees,
    undetectably.

    Every mutation a round makes to crawl state is journalled here, so an
    interruption discards the round whole. Nothing is lost by discarding: every
    response is already in raw/, so the retried round is served from disk and
    costs no API budget.

    Live call counters are deliberately NOT journalled. Those calls were really
    sent and the budget really was spent; pretending otherwise would understate
    real spend against CALL_BUDGET.
    """

    def __init__(self) -> None:
        self._undo: list[Callable[[], None]] = []

    def __len__(self) -> int:
        return len(self._undo)

    def on_undo(self, fn: Callable[[], None]) -> None:
        self._undo.append(fn)

    def new_key(self, container: dict, key: Any) -> None:
        self.on_undo(lambda: container.pop(key, None))

    def field(self, record: dict, key: str) -> None:
        had, old = key in record, record.get(key)

        def _undo() -> None:
            if had:
                record[key] = old
            else:
                record.pop(key, None)

        self.on_undo(_undo)

    def set_added(self, target: set, value: Any) -> None:
        self.on_undo(lambda: target.discard(value))

    def deque_popleft(self, queue: deque, item: Any) -> None:
        self.on_undo(lambda: queue.appendleft(item))

    def deque_append(self, queue: deque) -> None:
        def _undo() -> None:
            if queue:
                queue.pop()

        self.on_undo(_undo)

    def attribute(self, obj: Any, name: str) -> None:
        old = getattr(obj, name)
        if isinstance(old, dict):
            old = dict(old)
        self.on_undo(lambda: setattr(obj, name, old))

    def rollback(self) -> None:
        for fn in reversed(self._undo):
            fn()
        self._undo.clear()

    def commit(self) -> None:
        self._undo.clear()


def uid(user: dict[str, Any] | None) -> str | None:
    """Canonical id for a user object: the slug Trakt's own URLs use."""
    if not isinstance(user, dict):
        return None
    ids = user.get("ids") or {}
    slug = ids.get("slug") or user.get("username")
    if not isinstance(slug, str):
        return None
    slug = slug.strip()
    return slug or None


class Step3Crawler:
    def __init__(
        self,
        client: TraktClient,
        resume: bool = True,
        state_dir: Path | None = None,
        max_rounds: int | None = None,
    ):
        self.client = client
        # An offline replay writes its own artifact from merged records, so it
        # turns this off. A live run never does.
        self.write_artifact = True
        self.state_dir = Path(state_dir or RAW_STEP3)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.state_dir / "state.json"
        self.pool_path = self.state_dir / "user_pool.jsonl"
        self.curve_path = self.state_dir / "yield_curve.jsonl"
        self.edges_path = self.state_dir / "edges.jsonl"
        self.max_rounds = max_rounds

        self.users: dict[str, dict[str, Any]] = {}
        self.frontier: dict[str, deque] = {}      # origin_seed -> deque[(slug, depth)]
        self.seed_order: list[str] = []
        self.seed_cursor = 0
        self.expanded: set[str] = set()
        self.list_cursor = {"lists/trending": 1, "lists/popular": 1}
        self.list_feed_toggle = 0
        self.seen_list_ids: set[int] = set()
        self.rounds: list[dict[str, Any]] = []
        self.discarded_rounds: list[dict[str, Any]] = []
        # Calls that actually left the machine, i.e. real budget spend.
        self.calls_discovery = 0
        self.calls_screen = 0
        self.calls_seed = 0
        # Calls the algorithm made, cache hits included. Equal to the above on a
        # first run; on a resume or a replay they diverge, and the difference is
        # exactly what the cache saved.
        self.attempts_discovery = 0
        self.attempts_screen = 0
        self.attempts_seed = 0
        self.stop_reason: str | None = None
        self.forced_403_stop: dict[str, Any] | None = None
        # Distinct USERS we were refused, which is what the name says. The
        # endpoint-level tally is kept under its own name because one user can
        # 403 on followers, following and stats and that is one denied user.
        self.access_denied_user_slugs: set[str] = set()
        self.access_denied_endpoint_hits = 0
        self.access_denied_live_hits = 0
        self.started_at = utcnow()

        self._journal = _RoundJournal()
        self._round_edges: list[dict[str, Any]] = []
        self._round_request_marks: list[tuple[float, float, bool]] = []

        if resume and self.state_path.exists():
            self._load_state()

    # -- persistence -------------------------------------------------------

    def _load_state(self) -> None:
        payload = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.users = payload["users"]
        self.frontier = {k: deque(tuple(x) for x in v)
                         for k, v in payload["frontier"].items()}
        self.seed_order = payload["seed_order"]
        self.seed_cursor = payload["seed_cursor"]
        self.expanded = set(payload["expanded"])
        self.list_cursor = payload["list_cursor"]
        self.list_feed_toggle = payload["list_feed_toggle"]
        self.seen_list_ids = set(payload["seen_list_ids"])
        self.rounds = payload["rounds"]
        self.discarded_rounds = payload.get("discarded_rounds", [])
        self.calls_discovery = payload["calls_discovery"]
        self.calls_screen = payload["calls_screen"]
        self.calls_seed = payload["calls_seed"]
        self.attempts_discovery = payload.get("attempts_discovery", self.calls_discovery)
        self.attempts_screen = payload.get("attempts_screen", self.calls_screen)
        self.attempts_seed = payload.get("attempts_seed", self.calls_seed)
        denied = payload.get("access_denied_user_slugs")
        if denied is None:
            # Pre-amendment state files carried only an endpoint-hit integer and
            # no slugs, so the distinct-user count is not recoverable from them.
            # It is left empty rather than seeded with a number that would be
            # read as a user count.
            self.access_denied_user_slugs = set()
            self.access_denied_endpoint_hits = int(payload.get("access_denied_users", 0))
        else:
            self.access_denied_user_slugs = set(denied)
            self.access_denied_endpoint_hits = int(
                payload.get("access_denied_endpoint_hits", 0))
        self.access_denied_live_hits = int(payload.get("access_denied_live_hits", 0))
        self.started_at = payload.get("started_at", self.started_at)
        print(f"resumed: {len(self.users)} users, {len(self.rounds)} rounds, "
              f"{self.total_calls} calls already spent")

    def _save_state(self) -> None:
        payload = {
            "started_at": self.started_at,
            "saved_at": utcnow(),
            "users": self.users,
            "frontier": {k: list(v) for k, v in self.frontier.items()},
            "seed_order": self.seed_order,
            "seed_cursor": self.seed_cursor,
            "expanded": sorted(self.expanded),
            "list_cursor": self.list_cursor,
            "list_feed_toggle": self.list_feed_toggle,
            "seen_list_ids": sorted(self.seen_list_ids),
            "rounds": self.rounds,
            "discarded_rounds": self.discarded_rounds,
            "calls_discovery": self.calls_discovery,
            "calls_screen": self.calls_screen,
            "calls_seed": self.calls_seed,
            "attempts_discovery": self.attempts_discovery,
            "attempts_screen": self.attempts_screen,
            "attempts_seed": self.attempts_seed,
            "access_denied_user_slugs": sorted(self.access_denied_user_slugs),
            "access_denied_endpoint_hits": self.access_denied_endpoint_hits,
            "access_denied_live_hits": self.access_denied_live_hits,
            "access_denied_users": len(self.access_denied_user_slugs),
        }
        _atomic_write_text(self.state_path, json.dumps(payload))

    @property
    def total_calls(self) -> int:
        return self.calls_discovery + self.calls_screen + self.calls_seed

    @property
    def total_attempts(self) -> int:
        return self.attempts_discovery + self.attempts_screen + self.attempts_seed

    @property
    def access_denied_users(self) -> int:
        return len(self.access_denied_user_slugs)

    # -- pool bookkeeping --------------------------------------------------

    def _record_user(
        self,
        user: dict[str, Any],
        channel: str,
        edge: str,
        depth: int | None = None,
        origin_seed: str | None = None,
        parent: str | None = None,
        seed_provenance: dict[str, Any] | None = None,
        list_provenance: dict[str, Any] | None = None,
    ) -> tuple[str | None, bool]:
        """Add or update one user. Returns (slug, newly_eligible)."""
        slug = uid(user)
        if slug is None:
            return None, False
        existing = self.users.get(slug)
        if existing is not None:
            # Tag with every channel that found them; the first one stays primary.
            if channel == "A" and not existing.get("in_a"):
                self._journal.field(existing, "in_a")
                self._journal.field(existing, "depth")
                self._journal.field(existing, "origin_seed")
                existing["in_a"] = True
                existing.setdefault("depth", depth)
                existing.setdefault("origin_seed", origin_seed)
            if channel == "B" and not existing.get("in_b"):
                self._journal.field(existing, "in_b")
                existing["in_b"] = True
            if list_provenance is not None:
                self._journal.field(existing, "lists_owned")
                existing["lists_owned"] = list(existing.get("lists_owned") or [])
                existing["lists_owned"].append(list_provenance)
            return slug, False

        private = bool(user.get("private"))
        deleted = bool(user.get("deleted"))
        record = {
            "username": user.get("username"),
            "trakt_id": (user.get("ids") or {}).get("trakt"),
            "channel_first": channel,
            "in_a": channel == "A",
            "in_b": channel == "B",
            "edge": edge,
            "depth": depth,
            "origin_seed": origin_seed,
            # `parent` is the FIRST parent only and is kept for continuity. It
            # is a spanning tree, not the graph. edges.jsonl holds every edge.
            "parent": parent,
            "private": private,
            "deleted": deleted,
            "vip": bool(user.get("vip")),
            "joined_at": user.get("joined_at"),
            "first_seen_round": len(self.rounds),
            # Provenance. Step 11 asks whether the pool is one clique and
            # whether the two channels differ; neither question can be answered
            # after the budget is gone if this is not written down now.
            "seed_provenance": seed_provenance,
            "lists_owned": [list_provenance] if list_provenance else [],
            # Set when this user is expanded. Distinguishes "we read this user's
            # followers and there were none" from "we were refused".
            "expansion": None,
            "screen": None,
        }
        self.users[slug] = record
        self._journal.new_key(self.users, slug)
        eligible = not private and not deleted
        return slug, eligible

    def _enqueue_frontier(self, slug: str, depth: int, origin_seed: str) -> None:
        if depth > MAX_DEPTH or slug in self.expanded:
            return
        queue = self.frontier.setdefault(origin_seed, deque())
        queue.append((slug, depth))
        self._journal.deque_append(queue)

    def frontier_shape(self) -> dict[str, Any]:
        """Size and shape of the frontier. A plateau and a stall look the same
        in the yield number alone; they do not look the same here. A saturating
        graph drains the frontier, a stalled machine leaves it full."""
        by_depth: dict[str, int] = {}
        total = 0
        nonempty = 0
        for queue in self.frontier.values():
            if queue:
                nonempty += 1
            for _, depth in queue:
                total += 1
                by_depth[str(depth)] = by_depth.get(str(depth), 0) + 1
        return {
            "frontier_size": total,
            "frontier_seeds_nonempty": nonempty,
            "frontier_seeds_total": len(self.frontier),
            "frontier_by_depth": by_depth,
        }

    # -- guarded request ---------------------------------------------------

    def _get(self, endpoint: str, params: dict[str, Any] | None, kind: str):
        """One call. Counts it, and lets the 403 / 429 stop conditions through."""
        started = time.time()
        resp = self.client.get(endpoint, params)
        finished = time.time()
        self._round_request_marks.append((started, finished, resp.from_cache))

        if kind == "discovery":
            self.attempts_discovery += 1
        elif kind == "screen":
            self.attempts_screen += 1
        else:
            self.attempts_seed += 1

        if not resp.from_cache:
            if kind == "discovery":
                self.calls_discovery += 1
            elif kind == "screen":
                self.calls_screen += 1
            else:
                self.calls_seed += 1

        if resp.access_denied:
            # Endpoint-level, every occurrence, cache replays included: this is
            # how often we hit a denial.
            self.access_denied_endpoint_hits += 1
            if not resp.from_cache:
                self.access_denied_live_hits += 1
            # User-level, deduplicated: this is how many users were denied, and
            # it is idempotent under a replay from cache, which the old counter
            # was not.
            slug = user_slug_from_endpoint(endpoint)
            if slug and slug not in self.access_denied_user_slugs:
                self.access_denied_user_slugs.add(slug)
                self._journal.set_added(self.access_denied_user_slugs, slug)
        return resp

    # -- seeds -------------------------------------------------------------

    def build_seeds(self) -> None:
        if self.seed_order:
            return
        print(f"seeding: up to {N_SEEDS} public profiles from movie-comment authors")
        candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for endpoint, pages in SEED_FEEDS:
            for page in range(1, pages + 1):
                if len(candidates) >= N_SEEDS * 3:
                    break
                try:
                    resp = self._get(endpoint, {"page": page, "limit": 100}, "seed")
                except TraktClientError:
                    raise
                if not resp.ok or not isinstance(resp.data, list):
                    print(f"  seed feed {endpoint} p{page}: status {resp.status}, skipping")
                    break
                for item in resp.data:
                    if not isinstance(item, dict):
                        continue
                    comment = item.get("comment")
                    user = (comment or {}).get("user")
                    if not isinstance(user, dict):
                        continue
                    # Which movie, which feed, which page. The seeds are the one
                    # part of the pool taken from comment authors, so Step 11
                    # needs to be able to drop them wholesale or to check whether
                    # they cluster on a handful of films. Neither is possible if
                    # only the username is kept.
                    movie = item.get("movie") if isinstance(item.get("movie"), dict) else {}
                    candidates.append((user, {
                        "feed": endpoint,
                        "page": page,
                        "movie_title": movie.get("title"),
                        "movie_year": movie.get("year"),
                        "movie_trakt_id": (movie.get("ids") or {}).get("trakt"),
                        "movie_slug": (movie.get("ids") or {}).get("slug"),
                        "comment_id": (comment or {}).get("id"),
                        "comment_created_at": (comment or {}).get("created_at"),
                    }))

        seen: set[str] = set()
        for user, provenance in candidates:
            if len(self.seed_order) >= N_SEEDS:
                break
            slug = uid(user)
            if slug is None or slug in seen:
                continue
            if user.get("private") or user.get("deleted"):
                seen.add(slug)
                continue
            seen.add(slug)
            self._record_user(user, channel="A", edge="seed", depth=0,
                              origin_seed=slug, seed_provenance=provenance)
            self.seed_order.append(slug)
            self._enqueue_frontier(slug, 0, slug)
        print(f"  {len(self.seed_order)} seeds from {self.calls_seed} calls "
              f"({len(candidates)} comment authors seen)")

    # -- channel A ---------------------------------------------------------

    def _next_frontier_user(self) -> tuple[str, int, str] | None:
        """Round-robin across origin seeds so no one subtree eats the budget."""
        if not self.seed_order:
            return None
        for _ in range(len(self.seed_order)):
            seed = self.seed_order[self.seed_cursor % len(self.seed_order)]
            self.seed_cursor += 1
            queue = self.frontier.get(seed)
            while queue:
                item = queue.popleft()
                self._journal.deque_popleft(queue, item)
                slug, depth = item
                if slug in self.expanded:
                    continue
                return slug, depth, seed
        return None

    def expand_channel_a(self, budget_users: int) -> dict[str, Any]:
        """Breadth-first over followers and following. Returns round metrics."""
        stats: dict[str, Any] = {
            "calls": 0,
            "new_eligible": 0,
            "expanded_users": 0,
            "neighbours_returned": 0,
            "neighbours_new": 0,
            "neighbours_known": 0,
            "edges": 0,
            "edges_to_private_or_deleted": 0,
            "expansions_complete": 0,
            "expansions_access_denied": 0,
            "expansions_unavailable": 0,
            "expansions_other_status": 0,
            "frontier_exhausted": False,
        }
        for _ in range(budget_users):
            picked = self._next_frontier_user()
            if picked is None:
                stats["frontier_exhausted"] = True
                break
            slug, depth, seed = picked
            path = quote(slug, safe="")
            outcomes: dict[str, Any] = {}
            counts: dict[str, Any] = {}
            for edge in ("followers", "following"):
                resp = self._get(
                    f"users/{path}/{edge}",
                    {"page": 1, "limit": NEIGHBOURS_PER_USER},
                    "discovery",
                )
                stats["calls"] += 1
                # A user-level 403 is NOT an empty follower list. Letting it fall
                # into a bare `continue` recreated at the discovery layer exactly
                # the conflation decisions/0004-403-handling.md forbids, and it
                # is invisible afterwards: both look like a user with no edges.
                if resp.access_denied:
                    outcomes[edge] = "access_denied"
                    counts[edge] = None
                    stats["expansions_access_denied"] += 1
                    continue
                if resp.unavailable:
                    outcomes[edge] = f"unavailable_{resp.status}"
                    counts[edge] = None
                    stats["expansions_unavailable"] += 1
                    continue
                if not resp.ok or not isinstance(resp.data, list):
                    outcomes[edge] = f"status_{resp.status}"
                    counts[edge] = None
                    stats["expansions_other_status"] += 1
                    continue

                outcomes[edge] = "ok"
                counts[edge] = len(resp.data)
                stats["neighbours_returned"] += len(resp.data)
                for item in resp.data:
                    user = item.get("user") if isinstance(item, dict) else None
                    if not isinstance(user, dict):
                        continue
                    known_before = uid(user) in self.users
                    child, eligible = self._record_user(
                        user, channel="A", edge=edge, depth=depth + 1,
                        origin_seed=seed, parent=slug,
                    )
                    if child is None:
                        continue
                    stats["neighbours_known" if known_before else "neighbours_new"] += 1
                    # EVERY edge, not just the first one that reached a user.
                    # Keeping only the first parent leaves raw/ holding a
                    # spanning tree, and a spanning tree cannot answer whether
                    # the pool is one clique: a tree has no cycles by
                    # construction, so the question is decided by the data
                    # structure rather than by the data.
                    child_rec = self.users[child]
                    self._round_edges.append({
                        "round": len(self.rounds) + 1,
                        "src": slug,
                        "dst": child,
                        "endpoint_edge": edge,
                        # Direction, spelled out so Step 11 never has to guess:
                        # on /followers, dst follows src; on /following, src
                        # follows dst.
                        "follower": child if edge == "followers" else slug,
                        "followee": slug if edge == "followers" else child,
                        "src_depth": depth,
                        "dst_depth": depth + 1,
                        "origin_seed": seed,
                        "dst_new": not known_before,
                        "dst_private": bool(child_rec["private"]),
                        "dst_deleted": bool(child_rec["deleted"]),
                    })
                    stats["edges"] += 1
                    if child_rec["private"] or child_rec["deleted"]:
                        stats["edges_to_private_or_deleted"] += 1
                    if eligible:
                        stats["new_eligible"] += 1
                        self._enqueue_frontier(child, depth + 1, seed)

            # Marked expanded only now, after BOTH edge calls have resolved. The
            # old order marked it first, so an interrupt between the two calls
            # lost the second edge permanently: resume skipped the user because
            # it was already in `expanded`.
            self.expanded.add(slug)
            self._journal.set_added(self.expanded, slug)
            stats["expanded_users"] += 1

            record = self.users.get(slug)
            if record is not None:
                self._journal.field(record, "expansion")
                complete = all(v == "ok" for v in outcomes.values()) and len(outcomes) == 2
                record["expansion"] = {
                    "at_round": len(self.rounds) + 1,
                    "depth": depth,
                    "origin_seed": seed,
                    "followers_outcome": outcomes.get("followers"),
                    "following_outcome": outcomes.get("following"),
                    "followers_returned": counts.get("followers"),
                    "following_returned": counts.get("following"),
                    # False means we did not see this user's edges, which is a
                    # different object from a user whose edge lists were empty.
                    "complete": complete,
                }
                if complete:
                    stats["expansions_complete"] += 1
        return stats

    # -- channel B ---------------------------------------------------------

    def expand_channel_b(self, budget_pages: int) -> dict[str, Any]:
        stats: dict[str, Any] = {
            "calls": 0,
            "new_eligible": 0,
            "list_records": 0,
            "lists_new": 0,
            "lists_duplicate": 0,
            "owners_new": 0,
            "owners_known": 0,
            "pages_empty": 0,
            "by_feed": {},
        }
        feeds = list(self.list_cursor.keys())
        for _ in range(budget_pages):
            feed = feeds[self.list_feed_toggle % len(feeds)]
            self.list_feed_toggle += 1
            page = self.list_cursor[feed]
            resp = self._get(feed, {"page": page, "limit": 100}, "discovery")
            stats["calls"] += 1
            per_feed = stats["by_feed"].setdefault(
                feed, {"calls": 0, "lists_new": 0, "owners_new": 0, "new_eligible": 0})
            per_feed["calls"] += 1
            self.list_cursor[feed] = page + 1
            if not resp.ok or not isinstance(resp.data, list) or not resp.data:
                stats["pages_empty"] += 1
                continue
            for item in resp.data:
                lst = item.get("list") if isinstance(item, dict) else None
                if not isinstance(lst, dict):
                    continue
                stats["list_records"] += 1
                list_id = (lst.get("ids") or {}).get("trakt")
                if isinstance(list_id, int):
                    if list_id in self.seen_list_ids:
                        stats["lists_duplicate"] += 1
                        continue
                    self.seen_list_ids.add(list_id)
                    self._journal.set_added(self.seen_list_ids, list_id)
                stats["lists_new"] += 1
                per_feed["lists_new"] += 1
                owner = lst.get("user")
                if not isinstance(owner, dict):
                    continue
                known_before = uid(owner) in self.users
                # trending vs popular, the list id, and one record per list, so
                # "lists per owner" is a fact in raw/ rather than a re-derivation
                # nobody can do once the budget is gone.
                _, eligible = self._record_user(
                    owner, channel="B", edge="list_owner",
                    list_provenance={
                        "feed": feed,
                        "page": page,
                        "list_id": list_id,
                        "list_slug": (lst.get("ids") or {}).get("slug"),
                        "item_count": lst.get("item_count"),
                        "likes": lst.get("likes"),
                        "comment_count": lst.get("comment_count"),
                        "privacy": lst.get("privacy"),
                        "updated_at": lst.get("updated_at"),
                    },
                )
                stats["owners_known" if known_before else "owners_new"] += 1
                if not known_before:
                    per_feed["owners_new"] += 1
                if eligible:
                    stats["new_eligible"] += 1
                    per_feed["new_eligible"] += 1
        return stats

    # -- screening ---------------------------------------------------------

    def _screen_queue(self) -> Iterable[str]:
        """Unscreened, public, non-deleted users, ordered for diversity.

        Screening is the binding budget: discovery finds users roughly an order
        of magnitude faster than we can screen them, so the ORDER of this queue,
        not the crawl, is what decides who ends up in the pool Step 4 receives.
        A naive ordering by discovery time would hand Step 4 the shallowest
        neighbours of the earliest seeds - exactly the narrow, tightly connected
        pool Step 11 exists to catch.

        So Channel A is round-robined across (origin_seed, depth) groups: each
        seed's subtree and each walk depth contributes its first member before
        any group contributes its second. Channel A and Channel B are then
        interleaved 50/50, which maximises the smaller arm and so maximises the
        power of Step 11's channel comparison.

        Consequence to state in the write-up: the channel mix and the depth mix
        of the screened pool are DESIGN CHOICES, not natural rates. Step 11 must
        not read either as a fact about Trakt.
        """
        a_groups: dict[tuple, list[str]] = {}
        b: list[str] = []
        for slug, rec in self.users.items():
            if rec["screen"] is not None or rec["private"] or rec["deleted"]:
                continue
            if rec["channel_first"] == "A":
                key = (rec.get("origin_seed"), rec.get("depth"))
                a_groups.setdefault(key, []).append(slug)
            else:
                b.append(slug)

        for key, members in a_groups.items():
            members.sort(key=lambda s: self.users[s]["first_seen_round"])

        # round-robin across (seed, depth) groups
        a: list[str] = []
        ranked = sorted(
            ((rank, key, slug)
             for key, members in a_groups.items()
             for rank, slug in enumerate(members)),
            key=lambda t: (t[0], t[1][1] if t[1][1] is not None else 99, str(t[1][0])),
        )
        a = [slug for _, _, slug in ranked]

        b.sort(key=lambda s: self.users[s]["first_seen_round"])

        out: list[str] = []
        for i in range(max(len(a), len(b))):
            if i < len(a):
                out.append(a[i])
            if i < len(b):
                out.append(b[i])
        return out

    def screen(self, budget_calls: int) -> dict[str, Any]:
        stats: dict[str, Any] = {
            "calls": 0,
            "newly_usable": 0,
            "below_floor": 0,
            "access_denied": 0,
            "unavailable": 0,
            "other_status": 0,
            "reduced_payloads": 0,
        }
        for slug in self._screen_queue():
            if stats["calls"] >= budget_calls:
                break
            resp = self._get(f"users/{quote(slug, safe='')}/stats", None, "screen")
            stats["calls"] += 1
            rec = self.users[slug]
            self._journal.field(rec, "screen")
            if resp.access_denied:
                rec["screen"] = {"usable": False, "reason": "access_denied"}
                stats["access_denied"] += 1
                continue
            if resp.unavailable:
                rec["screen"] = {"usable": False, "reason": f"unavailable_{resp.status}"}
                stats["unavailable"] += 1
                continue
            if not resp.ok or not isinstance(resp.data, dict):
                rec["screen"] = {"usable": False, "reason": f"status_{resp.status}"}
                stats["other_status"] += 1
                continue
            d = resp.data
            episodes = (d.get("episodes") or {})
            movies = (d.get("movies") or {})
            network = (d.get("network") or {})
            progress = (d.get("progress") or {})
            ep_watched = int(episodes.get("watched") or 0)
            usable = ep_watched >= MIN_EPISODES_USABLE

            # users/:id/stats comes back in two shapes. 1827 of 2376 cached
            # bodies (77 percent) carry only movies/shows/seasons/episodes/
            # network/ratings; the other 549 add progress, lists, total_minutes
            # and total_plays. The forecast used to divide `total_plays`, so for
            # three users in four it divided a missing field read as zero and
            # forecast exactly one page. Where the field IS present it equals
            # episodes.plays + movies.plays in 549 of 549 bodies, so that sum is
            # used instead: always available, and identical wherever both exist.
            episode_plays = int(episodes.get("plays") or 0)
            movie_plays = int(movies.get("plays") or 0)
            history_plays = episode_plays + movie_plays
            reported_total = d.get("total_plays")
            if reported_total is None:
                stats["reduced_payloads"] += 1
            rec["screen"] = {
                "usable": usable,
                "reason": "ok" if usable else "below_episode_floor",
                "episodes_watched": ep_watched,
                "episode_plays": episode_plays,
                "shows_watched": int((d.get("shows") or {}).get("watched") or 0),
                "movie_plays": movie_plays,
                # Step 4 sweeps /users/:id/history unfiltered (decision 0002), so
                # the page basis is episode plays plus movie plays.
                "history_plays": history_plays,
                "total_plays": history_plays,
                "total_plays_reported": (
                    int(reported_total) if reported_total is not None else None),
                "stats_payload_variant": "reduced" if reported_total is None else "full",
                "followers": int(network.get("followers") or 0),
                "following": int(network.get("following") or 0),
                "progress_available": bool(progress),
                "progress_started": int(progress.get("started") or 0),
                "progress_finished": int(progress.get("finished") or 0),
                "progress_dropped": int(progress.get("dropped") or 0),
                "step4_pages_forecast": max(
                    1, math.ceil(history_plays / STEP4_PAGE_LIMIT)),
            }
            if usable:
                stats["newly_usable"] += 1
            else:
                stats["below_floor"] += 1
        return stats

    # -- the Step 4 forecast, aggregated -----------------------------------

    def step4_forecast(self) -> dict[str, Any]:
        """Sum the per-user page forecast over the pool.

        This is the number the Step 3 checkpoint exists to produce, and it was
        recorded per user and never added up. It is reported with its
        distribution rather than as a mean because the distribution is the whole
        point: the cost is concentrated in a tail, and a mean alone would let a
        reader plan Step 4 as though users were interchangeable.
        """
        pages = [
            rec["screen"]["step4_pages_forecast"]
            for rec in self.users.values()
            if rec.get("screen") and rec["screen"].get("usable")
        ]
        reduced = sum(
            1 for rec in self.users.values()
            if rec.get("screen") and rec["screen"].get("stats_payload_variant") == "reduced"
        )
        if not pages:
            return {"usable_users": 0, "total_pages": 0, "note": "no usable users yet"}
        pages.sort()

        def pct(p: float) -> int:
            if len(pages) == 1:
                return pages[0]
            idx = min(len(pages) - 1, max(0, int(round((p / 100.0) * (len(pages) - 1)))))
            return pages[idx]

        total = sum(pages)
        mean = total / len(pages)
        buckets = [(1, 1), (2, 5), (6, 10), (11, 25), (26, 50),
                   (51, 100), (101, 200), (201, 500), (501, 10 ** 9)]
        head = pages[::-1]
        top10 = head[:max(1, len(pages) // 10)]
        top1 = head[:max(1, len(pages) // 100)]
        return {
            "basis": "pages = ceil((episodes.plays + movies.plays) / %d), floor 1"
                     % STEP4_PAGE_LIMIT,
            "endpoint": "GET /users/:id/history, unfiltered (decision 0002)",
            "usable_users": len(pages),
            "total_pages": total,
            "total_pages_is_total_calls": True,
            "mean_pages_per_user": round(mean, 2),
            "stdev_pages_per_user": round(statistics.pstdev(pages), 2) if len(pages) > 1 else 0.0,
            "min": pages[0],
            "p25": pct(25),
            "median": pct(50),
            "p75": pct(75),
            "p90": pct(90),
            "p95": pct(95),
            "p99": pct(99),
            "max": pages[-1],
            "share_of_pages_in_top_decile_of_users": round(sum(top10) / total, 4),
            "share_of_pages_in_top_percentile_of_users": round(sum(top1) / total, 4),
            "histogram": [
                {"pages_from": lo,
                 "pages_to": (None if hi >= 10 ** 9 else hi),
                 "users": sum(1 for p in pages if lo <= p <= hi),
                 "pages": sum(p for p in pages if lo <= p <= hi)}
                for lo, hi in buckets
            ],
            "hours_at_throttle_150_per_min": round(total / 150.0 / 60.0, 2),
            "extrapolated_to_target_usable": {
                "target_usable": TARGET_USABLE,
                "method": "mean pages per usable user times the target",
                "calls": int(round(mean * TARGET_USABLE)),
                "hours_at_throttle_150_per_min": round(
                    mean * TARGET_USABLE / 150.0 / 60.0, 2),
            },
            "screened_with_reduced_stats_payload": reduced,
        }

    # -- counts ------------------------------------------------------------

    def counts(self) -> dict[str, Any]:
        n_usable = n_screened = n_priv = n_del = n_a = n_b = n_both = 0
        n_seeds = n_denied_expansion = n_partial_expansion = 0
        by_depth: dict[str, int] = {}
        for rec in self.users.values():
            n_priv += bool(rec["private"])
            n_del += bool(rec["deleted"])
            if rec["in_a"] and rec["in_b"]:
                n_both += 1
            if rec["channel_first"] == "A":
                n_a += 1
                depth = rec.get("depth")
                by_depth[str(depth)] = by_depth.get(str(depth), 0) + 1
                if depth == 0:
                    n_seeds += 1
            else:
                n_b += 1
            expansion = rec.get("expansion")
            if isinstance(expansion, dict) and not expansion.get("complete"):
                n_partial_expansion += 1
                if "access_denied" in (expansion.get("followers_outcome"),
                                       expansion.get("following_outcome")):
                    n_denied_expansion += 1
            scr = rec["screen"]
            if scr is not None:
                n_screened += 1
                n_usable += bool(scr.get("usable"))
        return {
            "discovered": len(self.users),
            "private": n_priv,
            "deleted": n_del,
            "eligible": len(self.users) - n_priv - n_del,
            "screened": n_screened,
            "usable": n_usable,
            "channel_a_first": n_a,
            "channel_b_first": n_b,
            "in_both_channels": n_both,
            "channel_a_by_depth": by_depth,
            "seeds": n_seeds,
            "expanded": len(self.expanded),
            # An expansion we were refused is not an expansion that found
            # nothing, and the pool file keeps the two apart.
            "expansions_incomplete": n_partial_expansion,
            "expansions_access_denied": n_denied_expansion,
            "access_denied_users": self.access_denied_users,
        }

    # -- plateau -----------------------------------------------------------

    def plateau_state(self, extra_yield: float | None = None) -> dict[str, Any]:
        """The plateau rule's own state, unchanged, plus how close it came.

        The rule and every threshold in it are exactly as committed before the
        run. What is added is the margin: `ratio_to_peak` against the 0.20
        trigger, and `rounds_below_threshold_so_far`. Rounds 7 to 10 of the
        first run sat at 0.244, 0.260, 0.229 and 0.230 against a trigger of
        0.200 and then round 11 rebounded, and none of that was visible in the
        record. Reporting the margin is not tuning the rule.
        """
        ys = [r["yield_per_discovery_call"] for r in self.rounds]
        if extra_yield is not None:
            ys = ys + [extra_yield]
        movings, peak, fired = [], 0.0, 0
        below_count = 0
        for i in range(len(ys)):
            window = ys[max(0, i - 2): i + 1]
            m = sum(window) / len(window)
            movings.append(m)
            peak = max(peak, m)
            eligible = (i + 1) >= MIN_ROUNDS_BEFORE_PLATEAU
            below = peak > 0 and m <= PLATEAU_FRACTION_OF_PEAK * peak
            if below:
                below_count += 1
            if eligible and below:
                fired += 1
            else:
                fired = 0
        ratio = (movings[-1] / peak) if (movings and peak) else None
        return {
            "moving_avg": movings[-1] if movings else 0.0,
            "peak_moving_avg": peak,
            "ratio_to_peak": ratio,
            "plateau_trigger_ratio": PLATEAU_FRACTION_OF_PEAK,
            "margin_above_trigger": (
                round(ratio - PLATEAU_FRACTION_OF_PEAK, 4) if ratio is not None else None),
            "consecutive_below": fired,
            "rounds_below_threshold_so_far": below_count,
            "rounds_completed": len(ys),
            "rounds_until_rule_is_eligible": max(0, MIN_ROUNDS_BEFORE_PLATEAU - len(ys)),
            "plateaued": fired >= PLATEAU_CONSECUTIVE_ROUNDS,
        }

    # -- the loop ----------------------------------------------------------

    def _time_decomposition(self, wall: float, before: dict[str, Any]) -> dict[str, Any]:
        """Where the round's wall-clock time went.

        A round that spent 2796 seconds with zero requests and no 429 is a
        suspended machine, and the first run recorded it identically to a round
        that spent 2796 seconds being throttled. Under this decomposition the
        first shows as one enormous inter-request gap with no rate-limit pauses
        and almost all of the time unaccounted; the second shows as throttle
        sleep. A reader at the checkpoint should never have to guess which.
        """
        now = self.client.counters

        def delta(key: str) -> float:
            return float(now.get(key, 0)) - float(before.get(key, 0))

        marks = self._round_request_marks
        gaps = [marks[i][0] - marks[i - 1][1] for i in range(1, len(marks))]
        throttle_s = delta("throttle_sleep_seconds")
        rate_s = delta("rate_limit_sleep_seconds")
        backoff_s = delta("backoff_sleep_seconds")
        request_s = delta("request_seconds")
        accounted = throttle_s + rate_s + backoff_s + request_s
        unaccounted = wall - accounted
        return {
            "wall_seconds": round(wall, 1),
            "request_seconds": round(request_s, 1),
            "sleep_seconds_throttle": round(throttle_s, 1),
            "sleep_seconds_rate_limit": round(rate_s, 1),
            "sleep_seconds_backoff": round(backoff_s, 1),
            "sleep_seconds_total": round(throttle_s + rate_s + backoff_s, 1),
            "unaccounted_seconds": round(unaccounted, 1),
            "max_inter_request_gap_seconds": round(max(gaps), 1) if gaps else 0.0,
            "rate_limit_pauses": int(delta("rate_limit_pauses")),
            "transient_retries": int(delta("transient_retries")),
            "http_5xx": int(delta("http_5xx")),
            "transport_errors": int(delta("transport_errors")),
            "requests_from_cache": sum(1 for m in marks if m[2]),
            "requests_live": sum(1 for m in marks if not m[2]),
            # A plateau is the graph saturating. A stall is the machine, the
            # network or the throttle. This flag says which one the clock looks
            # like; it decides nothing and stops nothing.
            "stall_suspected": bool(
                unaccounted > STALL_UNACCOUNTED_SECONDS
                and int(delta("rate_limit_pauses")) == 0
            ),
        }

    def run(self) -> None:
        self.build_seeds()
        self._save_state()
        self.write_outputs()

        while True:
            counts = self.counts()
            if counts["usable"] >= TARGET_USABLE:
                self.stop_reason = "sufficiency: reached the usable-user target"
                break
            if self.total_calls >= CALL_BUDGET:
                self.stop_reason = "budget: hit the Step 3 call cap"
                break
            plateau = self.plateau_state()
            if plateau["plateaued"]:
                self.stop_reason = "plateau: usable-user yield flattened"
                break
            if self.max_rounds is not None and len(self.rounds) >= self.max_rounds:
                self.stop_reason = f"max_rounds: stopped at {self.max_rounds} rounds"
                break

            t0 = time.time()
            before_counters = dict(self.client.counters)
            before = counts["eligible"]
            calls_at_round_start = self.total_calls
            self._journal = _RoundJournal()
            self._round_edges = []
            self._round_request_marks = []
            round_no = len(self.rounds) + 1

            # One round is one transaction. If anything interrupts it, the whole
            # round is journalled back out rather than half-persisted: a
            # half-persisted round leaves users marked expanded whose followers
            # were never read, and resume never revisits them, so the pool looks
            # complete while silently missing those subtrees.
            try:
                a = self.expand_channel_a(EXPAND_USERS_PER_ROUND)
                b = self.expand_channel_b(LIST_PAGES_PER_ROUND)
                s = self.screen(SCREEN_CALLS_PER_ROUND)
            except BaseException as exc:                      # noqa: BLE001
                self._journal.rollback()
                self._round_edges = []
                self.discarded_rounds.append({
                    "would_have_been_round": round_no,
                    "at": utcnow(),
                    "reason": type(exc).__name__,
                    "detail": str(exc)[:500],
                    "seconds_before_interruption": round(time.time() - t0, 1),
                    "live_calls_spent_in_this_round": self.total_calls - calls_at_round_start,
                    "note": "rolled back whole; every response is already in raw/, "
                            "so the retried round is served from disk and costs no "
                            "API budget",
                })
                self._save_state()
                self.write_outputs()
                raise

            after = self.counts()
            discovery_calls = a["calls"] + b["calls"]
            new_eligible = after["eligible"] - before
            shape = self.frontier_shape()
            timing = self._time_decomposition(time.time() - t0, before_counters)

            record = {
                "round": round_no,
                "at": utcnow(),
                "metrics_source": "measured",
                # -- calls -----------------------------------------------
                "discovery_calls": discovery_calls,
                "screen_calls": s["calls"],
                "channel_a_calls": a["calls"],
                "channel_b_calls": b["calls"],
                # -- yield, overall and per channel ----------------------
                # Both expanders always returned their own new-eligible count
                # and both call sites threw it away, so a round in which
                # Channel A had collapsed and Channel B was carrying the pool
                # was indistinguishable from a round in which both were healthy.
                "new_eligible_users": new_eligible,
                "yield_per_discovery_call": (new_eligible / discovery_calls)
                                            if discovery_calls else 0.0,
                "channel_a_new_eligible": a["new_eligible"],
                "channel_b_new_eligible": b["new_eligible"],
                "channel_a_yield_per_call": (a["new_eligible"] / a["calls"]) if a["calls"] else 0.0,
                "channel_b_yield_per_call": (b["new_eligible"] / b["calls"]) if b["calls"] else 0.0,
                "channel_overlap_this_round": (
                    a["new_eligible"] + b["new_eligible"] - new_eligible),
                # -- frontier: full means there is work left, empty means the
                #    walk actually ran out ---------------------------------
                "expanded_this_round": a["expanded_users"],
                "expanded_total": len(self.expanded),
                "frontier_exhausted": a["frontier_exhausted"],
                **shape,
                # -- branching and duplication ---------------------------
                "neighbours_returned": a["neighbours_returned"],
                "neighbours_new": a["neighbours_new"],
                "neighbours_already_known": a["neighbours_known"],
                "neighbour_dedup_rate": (
                    a["neighbours_known"] / a["neighbours_returned"])
                    if a["neighbours_returned"] else None,
                "neighbours_per_expanded_user": (
                    a["neighbours_returned"] / a["expanded_users"])
                    if a["expanded_users"] else None,
                "edges_recorded": a["edges"],
                "edges_to_private_or_deleted": a["edges_to_private_or_deleted"],
                # -- channel B duplication -------------------------------
                "list_records_seen": b["list_records"],
                "lists_new": b["lists_new"],
                "lists_duplicate": b["lists_duplicate"],
                "list_dedup_rate": (b["lists_duplicate"] / b["list_records"])
                                   if b["list_records"] else None,
                "list_owners_new": b["owners_new"],
                "list_owners_already_known": b["owners_known"],
                "channel_b_by_feed": b["by_feed"],
                # -- refusals, kept apart from empties -------------------
                "expansions_complete": a["expansions_complete"],
                "expansions_access_denied": a["expansions_access_denied"],
                "expansions_unavailable": a["expansions_unavailable"],
                "expansions_other_status": a["expansions_other_status"],
                "screen_access_denied": s["access_denied"],
                "screen_unavailable": s["unavailable"],
                "screen_other_status": s["other_status"],
                "screen_below_floor": s["below_floor"],
                "screen_reduced_payloads": s["reduced_payloads"],
                # -- screening -------------------------------------------
                "new_usable_confirmed": s["newly_usable"],
                # -- cumulative ------------------------------------------
                "cum_discovered": after["discovered"],
                "cum_eligible": after["eligible"],
                "cum_screened": after["screened"],
                "cum_usable": after["usable"],
                "cum_calls": self.total_calls,
                "cum_calls_live": self.total_calls,
                "cum_calls_attempted": self.total_attempts,
                "cum_access_denied_users": self.access_denied_users,
                "cum_access_denied_endpoint_hits": self.access_denied_endpoint_hits,
                "rounds_discarded_so_far": len(self.discarded_rounds),
                # -- clock, decomposed -----------------------------------
                "seconds": round(timing["wall_seconds"], 1),
                **timing,
            }
            record.update(self.plateau_state(extra_yield=record["yield_per_discovery_call"]))
            self.rounds.append(record)
            self._flush_edges()
            self._journal.commit()
            self._save_state()
            # Deliverables at the round boundary, not in a finally. A SIGKILL
            # can now lose at most the round in progress; it cannot leave the
            # study with thousands of calls spent and no pool on disk.
            self.write_outputs()

            if discovery_calls == 0 and s["calls"] == 0:
                self.stop_reason = "exhausted: no frontier and nothing left to screen"
                break

            r = self.rounds[-1]
            flag = "  STALL?" if r["stall_suspected"] else ""
            print(f"round {r['round']:>3}  calls {self.total_calls:>5}  "
                  f"disc {discovery_calls:>3} scr {s['calls']:>3}  "
                  f"new_elig {new_eligible:>5} (A{a['new_eligible']:>4}/B{b['new_eligible']:>4})  "
                  f"y={r['yield_per_discovery_call']:.1f}  "
                  f"usable {after['usable']:>5}/{after['screened']:>5}  "
                  f"pool {after['discovered']:>6}  front {shape['frontier_size']:>6}  "
                  f"{r['seconds']:.0f}s{flag}")

        self._save_state()
        self.write_outputs()

    # -- outputs -----------------------------------------------------------

    def _flush_edges(self) -> None:
        """Append this round's edges. raw/ ONLY: these are usernames."""
        if not self._round_edges:
            return
        self.edges_path.parent.mkdir(parents=True, exist_ok=True)
        with self.edges_path.open("a", encoding="utf-8") as fh:
            for edge in self._round_edges:
                fh.write(json.dumps(edge) + "\n")
            fh.flush()
        self._round_edges = []

    def write_pool(self) -> None:
        """raw/ ONLY. This file carries usernames and ids.

        Atomic. The old version opened with "w" and streamed, so a kill mid-write
        left a truncated file that is indistinguishable from a smaller complete
        pool: valid JSON on every line, just fewer lines.
        """
        lines = [json.dumps({"slug": slug, **rec}) + "\n"
                 for slug, rec in self.users.items()]
        _atomic_write_text(self.pool_path, "".join(lines))

    def write_curve(self) -> None:
        """raw/ copy of the round records. Counts only, but kept beside the pool
        so a resumed run has everything in one place."""
        _atomic_write_text(
            self.curve_path, "".join(json.dumps(r) + "\n" for r in self.rounds))

    def yield_curve_payload(self) -> dict[str, Any]:
        """Counts and aggregates only. This is what may leave the machine."""
        return {
            "step": "3 user discovery",
            "generated_at": utcnow(),
            "run_started_at": self.started_at,
            "status": "checkpoint" if self.stop_reason is None else "stopped",
            "stop_reason": self.stop_reason,
            "plan": plan_block(),
            "counts": self.counts(),
            "calls": {
                "seed": self.calls_seed,
                "discovery": self.calls_discovery,
                "screen": self.calls_screen,
                "total_live": self.total_calls,
                "total_attempted_including_cache_hits": self.total_attempts,
                "budget": CALL_BUDGET,
            },
            "access_denied": {
                "distinct_users_denied": self.access_denied_users,
                "endpoint_hits_including_cache_replays": self.access_denied_endpoint_hits,
                "endpoint_hits_live": self.access_denied_live_hits,
            },
            "plateau_state": self.plateau_state(),
            "step4_forecast": self.step4_forecast(),
            "rounds_completed": len(self.rounds),
            "rounds_discarded": len(self.discarded_rounds),
            # Counts and reason class only. An exception detail can carry an
            # endpoint, and an endpoint carries a username.
            "discarded_rounds": [
                {k: v for k, v in d.items() if k != "detail"}
                for d in self.discarded_rounds
            ],
            "rounds": self.rounds,
        }

    def write_yield_curve_artifact(self) -> Path:
        """artifacts/ . Counts only, and checked rather than asserted: every
        slug and username in the pool is searched for in the rendered text
        before it is written."""
        payload = self.yield_curve_payload()
        text = json.dumps(payload, indent=2, default=str)
        leaked = self._names_present_in(payload)
        if leaked:
            raise ValueError(
                f"refusing to write {len(leaked)} username(s) to artifacts/; "
                f"the yield curve is counts only"
            )
        self.client._refuse_if_secret(text, str(ARTIFACTS / "step3-yield-curve.json"))
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        path = ARTIFACTS / "step3-yield-curve.json"
        _atomic_write_text(path, text)

        columns = [
            "round", "metrics_source", "discovery_calls", "screen_calls",
            "channel_a_calls", "channel_b_calls", "new_eligible_users",
            "yield_per_discovery_call", "channel_a_new_eligible",
            "channel_b_new_eligible", "channel_a_yield_per_call",
            "channel_b_yield_per_call", "new_usable_confirmed",
            "expanded_this_round", "expanded_total", "frontier_size",
            "frontier_seeds_nonempty", "frontier_exhausted",
            "neighbours_returned", "neighbours_new", "neighbours_already_known",
            "neighbour_dedup_rate", "lists_new", "lists_duplicate",
            "list_dedup_rate", "expansions_access_denied",
            "cum_discovered", "cum_eligible", "cum_screened", "cum_usable",
            "cum_calls", "moving_avg", "peak_moving_avg", "ratio_to_peak",
            "consecutive_below", "wall_seconds", "request_seconds",
            "sleep_seconds_throttle", "sleep_seconds_rate_limit",
            "sleep_seconds_backoff", "unaccounted_seconds",
            "max_inter_request_gap_seconds", "rate_limit_pauses",
            "transient_retries", "http_5xx", "transport_errors",
            "stall_suspected",
        ]
        rows = [",".join(columns)]
        for r in self.rounds:
            rows.append(",".join(_csv_cell(r.get(c)) for c in columns))
        _atomic_write_text(ARTIFACTS / "step3-yield-curve.csv", "\n".join(rows) + "\n")
        return path

    def _names_present_in(self, payload: Any) -> list[str]:
        """Privacy check for anything bound for artifacts/ or decisions/.

        Three tests, none of which is a bare substring sweep over the document.
        A bare sweep is useless here: the pool holds slugs like "any", "noz" and
        "sean", which appear inside ordinary English words, so such a check
        fires on every artifact and a check that always fires is a check that
        gets deleted.

          1. Exact. Every string that appears as a JSON key or value is compared
             against the name set. This is what catches a user record that got
             serialised into the wrong file, which is the realistic failure.
          2. Long tokens. Identifier-shaped runs of 10 characters or more are
             matched against the name set. At that length an accidental
             collision with prose is not plausible.
          3. Paths. Anything of the form `users/<segment>` has its segment
             checked, which catches an endpoint that arrived inside an error
             message.
        """
        import re

        names: set[str] = set()
        for slug, rec in self.users.items():
            if slug:
                names.add(slug)
            username = rec.get("username")
            if isinstance(username, str) and username:
                names.add(username)
        if not names:
            return []

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
        found |= {unquote(seg) for seg in re.findall(r"users/([^/\s\"']+)", blob)} & names
        return sorted(found)

    def write_outputs(self) -> None:
        """Every deliverable, from whatever state is in hand right now."""
        self.write_pool()
        self.write_curve()
        self._flush_edges()
        if self.write_artifact:
            self.write_yield_curve_artifact()


def plan_block() -> dict[str, Any]:
    """The committed plan, verbatim from the module constants. Unchanged."""
    return {
        "n_seeds_target": N_SEEDS,
        "seed_source": "authors of recent/trending/updated comments on MOVIES",
        "max_depth": MAX_DEPTH,
        "neighbours_per_user": NEIGHBOURS_PER_USER,
        "expand_users_per_round": EXPAND_USERS_PER_ROUND,
        "list_pages_per_round": LIST_PAGES_PER_ROUND,
        "screen_calls_per_round": SCREEN_CALLS_PER_ROUND,
        "min_episodes_usable": MIN_EPISODES_USABLE,
        "plateau_rule": (f"3-round moving average of new eligible users per discovery "
                         f"call <= {PLATEAU_FRACTION_OF_PEAK:.0%} of its running peak, "
                         f"on {PLATEAU_CONSECUTIVE_ROUNDS} consecutive rounds, after at "
                         f"least {MIN_ROUNDS_BEFORE_PLATEAU} rounds"),
        "target_usable": TARGET_USABLE,
        "call_budget": CALL_BUDGET,
        "step4_page_limit": STEP4_PAGE_LIMIT,
    }


def _csv_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.6g}"
    text = str(value)
    if any(c in text for c in ',"\n'):
        return '"' + text.replace('"', '""') + '"'
    return text


def write_run_record(
    crawler: Step3Crawler,
    client: TraktClient,
    error: dict[str, Any] | None,
    exit_code: int,
    path: Path | None = None,
) -> Path:
    """logs/step3_run.json, on EVERY exit path.

    The old version was written only after the try/finally completed normally,
    so an uncaught TransientFailure produced a noisy traceback and no run record
    at all: the one exit where a reader most needs to know what happened left
    nothing behind. It was also the only write in the project that went out
    through a bare json.dumps with no credential guard.
    """
    record = {
        "started_at": crawler.started_at,
        "finished_at": utcnow(),
        "exit_code": exit_code,
        "exit_meaning": EXIT_MEANINGS.get(exit_code, "unknown"),
        "stop_reason": crawler.stop_reason,
        "error": error,
        "plan": plan_block(),
        "counts": crawler.counts(),
        "calls": {
            "seed": crawler.calls_seed,
            "discovery": crawler.calls_discovery,
            "screen": crawler.calls_screen,
            "total": crawler.total_calls,
            "total_attempted_including_cache_hits": crawler.total_attempts,
            "budget": CALL_BUDGET,
        },
        "plateau_state": crawler.plateau_state(),
        "step4_forecast": crawler.step4_forecast(),
        "rounds": len(crawler.rounds),
        "rounds_discarded": len(crawler.discarded_rounds),
        "discarded_rounds": crawler.discarded_rounds,
        "access_denied_users": crawler.access_denied_users,
        "access_denied_endpoint_hits": crawler.access_denied_endpoint_hits,
        "client_counters": client.summary(),
    }
    payload = json.dumps(client._redact(record), indent=2, default=str)
    target = path or (LOGS_DIR / "step3_run.json")
    client._refuse_if_secret(payload, str(target))
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(target, payload)
    return target


EXIT_MEANINGS = {
    EXIT_OK: "stopped on one of the three committed stopping rules",
    EXIT_ACCESS_BLOCKED: "403 treated as an application-level block",
    EXIT_RATE_LIMIT_PERSISTENT: "429s persisted beyond the configured budget",
    EXIT_TRANSIENT_EXHAUSTED: "transient backoff exhausted",
    EXIT_CLIENT_ERROR: "TraktClientError",
    EXIT_UNEXPECTED: "unexpected exception",
    EXIT_INTERRUPTED: "interrupted",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Step 3 user discovery")
    parser.add_argument("--state-dir", default=None,
                        help="where state, pool, curve and edges live (default raw/step3)")
    parser.add_argument("--max-rounds", type=int, default=None,
                        help="stop after N completed rounds (does not change any "
                             "stopping threshold; used by the offline replay)")
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args(argv)

    client = TraktClient(run_label="step3_user_discovery")
    crawler = Step3Crawler(
        client,
        resume=not args.no_resume,
        state_dir=Path(args.state_dir) if args.state_dir else None,
        max_rounds=args.max_rounds,
    )
    error: dict[str, Any] | None = None
    exit_code = EXIT_OK

    try:
        crawler.run()
    except AccessBlocked as exc:
        crawler.stop_reason = "HARD STOP: 403 classified as an application-level block"
        error = {"type": "AccessBlocked", "detail": str(exc)[:2000]}
        exit_code = EXIT_ACCESS_BLOCKED
        print(f"\n*** {crawler.stop_reason}\n{exc}", file=sys.stderr)
    except RateLimitPersistent as exc:
        crawler.stop_reason = "HARD STOP: 429s persisted across consecutive pauses"
        error = {"type": "RateLimitPersistent", "detail": str(exc)[:2000]}
        exit_code = EXIT_RATE_LIMIT_PERSISTENT
        print(f"\n*** {crawler.stop_reason}\n{exc}", file=sys.stderr)
    except TransientFailure as exc:
        crawler.stop_reason = "HARD STOP: transient backoff exhausted"
        error = {"type": "TransientFailure", "detail": str(exc)[:2000]}
        exit_code = EXIT_TRANSIENT_EXHAUSTED
        print(f"\n*** {crawler.stop_reason}\n{exc}", file=sys.stderr)
    except KeyboardInterrupt:
        crawler.stop_reason = "interrupted"
        error = {"type": "KeyboardInterrupt", "detail": None}
        exit_code = EXIT_INTERRUPTED
        print("\ninterrupted; the round in progress was discarded whole and "
              "state was saved", file=sys.stderr)
    except TraktClientError as exc:
        crawler.stop_reason = f"HARD STOP: {type(exc).__name__}"
        error = {"type": type(exc).__name__, "detail": str(exc)[:2000]}
        exit_code = EXIT_CLIENT_ERROR
        print(f"\n*** {crawler.stop_reason}\n{exc}", file=sys.stderr)
    except Exception as exc:                                  # noqa: BLE001
        crawler.stop_reason = f"HARD STOP: unexpected {type(exc).__name__}"
        error = {"type": type(exc).__name__, "detail": str(exc)[:2000]}
        exit_code = EXIT_UNEXPECTED
        print(f"\n*** {crawler.stop_reason}\n{exc}", file=sys.stderr)
    finally:
        # Deliverables have already been written at the last round boundary.
        # This is belt and braces, and it must not be able to suppress the run
        # record: a failure here is recorded, not raised.
        try:
            crawler._save_state()
            crawler.write_outputs()
        except Exception as exc:                              # noqa: BLE001
            error = error or {}
            error["final_write_failed"] = f"{type(exc).__name__}: {exc}"[:500]
            if exit_code == EXIT_OK:
                exit_code = EXIT_UNEXPECTED
        path = write_run_record(crawler, client, error, exit_code)

    print(f"\nrun record: {path}")
    print(f"exit {exit_code} ({EXIT_MEANINGS.get(exit_code)})")
    print(json.dumps({
        "counts": crawler.counts(),
        "calls": crawler.total_calls,
        "rounds": len(crawler.rounds),
        "stop_reason": crawler.stop_reason,
        "step4_forecast": crawler.step4_forecast(),
    }, indent=2, default=str))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
