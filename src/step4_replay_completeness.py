"""
What would the PROPOSED completeness rule produce on data already in raw/?

The Step 4 pilot failed 7 of 10 users on `error_short_read`, and the evidence
says the cause is Trakt's `X-Pagination-Item-Count` rather than a truncated
sweep. This replays those users out of the cache under both rules so the
difference is a measured number rather than an argument.

ZERO LIVE CALLS, and that is guaranteed rather than asserted:

  * the session raises on any outbound GET, so a cache miss stops the replay
    loudly instead of quietly costing budget;
  * `requests_sent` is checked at the end and must be zero;
  * the puller is constructed with offline=True, which refuses the canonical
    Step 4 state directory. That is the guard against repeating the Step 3
    accident where an offline replay overwrote the live-call ledger with the
    nothing it had spent.

`--rule page_count` was a proposal when this was written. It is now the ADOPTED
rule (decisions/0012, Human Lead, 2026-08-11). The script is kept as the
zero-call way to re-derive the comparison, and as the way to replay any FUTURE
change to the rule or the tolerance over users already decided under the
current one: the pages are on disk, so re-deciding costs nothing. It still
adopts nothing itself.

Run:
  .venv/bin/python src/step4_replay_completeness.py --rule page_count
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import step4_history_pull as s4  # noqa: E402
from trakt_client import TraktClient  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRATCH = PROJECT_ROOT / "processed" / "step4_replay"


class ReplayWentToTheNetwork(Exception):
    pass


class NoNetworkSession:
    """The zero-live-call guarantee. It cannot make a request."""

    def get(self, url, headers=None, params=None, timeout=None):
        raise ReplayWentToTheNetwork(
            f"the replay tried a live GET: {url} params={params}. Every page it "
            f"needs is supposed to be in raw/ already."
        )


def subset_pool(slugs: set[str], dest: Path) -> Path:
    """A pool file holding only the users being replayed. Carries usernames, so
    it lives under processed/, never artifacts/."""
    keep = []
    for line in s4.POOL_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("slug") in slugs:
            keep.append(line)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(keep) + "\n", encoding="utf-8")
    return dest


def slugs_from_ledger(outcomes: tuple[str, ...]) -> set[str]:
    ledger = s4.STATE_DIR / "pull_ledger.jsonl"
    latest: dict[str, str] = {}
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            latest[row["slug"]] = row["outcome"]
    return {slug for slug, outcome in latest.items() if outcome in outcomes}


def replay(slugs: set[str], rule: str, tolerance: float) -> dict[str, Any]:
    workdir = SCRATCH / rule
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    pool = subset_pool(slugs, workdir / "pool.jsonl")
    client = TraktClient(
        raw_dir=PROJECT_ROOT / "raw",          # the real cache: that is the point
        logs_dir=workdir / "logs",             # but not the real logs
        run_label=f"step4_replay_{rule}",
        session=NoNetworkSession(),
    )
    puller = s4.Step4Puller(
        client,
        state_dir=workdir / "state",
        pool_path=pool,
        sabbath_window=None,
        offline=True,
        reconcile=rule,
        residual_tolerance=tolerance,
    )
    puller.run()

    sent = client.counters["requests_sent"]
    if sent:
        raise ReplayWentToTheNetwork(f"replay sent {sent} request(s); it must send none")

    rows = puller.latest_outcomes()
    per_user = sorted(
        (
            {
                "forecast_pages": r["forecast_pages"],
                "outcome": r["outcome"],
                "pages_read": r["pages_read"],
                "page_count_reported": r["page_count_reported"],
                "item_count_reported": r["item_count_reported"],
                "item_count_residual": r.get("item_count_residual"),
                "records": r["records"],
            }
            for r in rows.values()
        ),
        key=lambda x: x["forecast_pages"],
    )
    residuals = [u["item_count_residual"] for u in per_user
                 if isinstance(u.get("item_count_residual"), int)]
    shares = [
        abs(u["item_count_residual"]) / u["item_count_reported"]
        for u in per_user
        if isinstance(u.get("item_count_residual"), int) and u["item_count_reported"]
    ]
    return {
        "rule": rule,
        "residual_tolerance": tolerance,
        "live_calls": sent,
        "cache_hits": client.counters["served_from_cache"],
        "users": len(per_user),
        "by_outcome": puller.counts()["by_outcome"],
        "records_parsed": puller.counts()["records_parsed"],
        "residual_min": min(residuals) if residuals else None,
        "residual_max": max(residuals) if residuals else None,
        "max_abs_residual_share": round(max(shares), 5) if shares else None,
        "per_user": per_user,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Zero-call completeness replay")
    parser.add_argument("--rule", choices=("exact", "page_count", "both"), default="both")
    parser.add_argument("--tolerance", type=float, default=0.02)
    parser.add_argument("--outcomes", default="error_short_read,complete",
                        help="which recorded outcomes to replay")
    args = parser.parse_args(argv)

    slugs = slugs_from_ledger(tuple(args.outcomes.split(",")))
    if not slugs:
        print("no users in the ledger match", file=sys.stderr)
        return 2
    print(f"replaying {len(slugs)} user(s) from cache, zero live calls\n")

    rules = ("exact", "page_count") if args.rule == "both" else (args.rule,)
    results = {}
    for rule in rules:
        results[rule] = replay(slugs, rule, args.tolerance)

    for rule, res in results.items():
        print(f"--- {rule} ---")
        print(json.dumps({k: v for k, v in res.items() if k != "per_user"},
                         indent=2, default=str))
    if "page_count" in results:
        print("\nper user under the proposed rule "
              "(forecast, actual pages, records, residual):")
        for u in results["page_count"]["per_user"]:
            print(f"  {u['forecast_pages']:>4} pages -> {u['page_count_reported']} "
                  f"actual, {u['records']:>6} records, "
                  f"residual {u['item_count_residual']}, {u['outcome']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
