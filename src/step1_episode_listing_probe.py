"""
Access probe: the episode-listing endpoint (Section 3.3 precondition).

Purpose
-------
artifacts/step1-outcome-definition.md Section 3.3 makes the listed episode-number
set `E` load-bearing and flags that its source was never tested under
Client-ID-only auth. Section 3.3 names exactly two candidate variants:

    A   GET /shows/:id/seasons/:season
    B   GET /shows/:id/seasons?extended=episodes

This script settles, with live calls, whether either variant returns a per-season
LIST of episode `number` values on the Client ID alone, and whether `E`, `L=|E|`
and `F=max(E)` are all derivable from that same payload.

Scope discipline
----------------
Yes/no auth-and-shape probe, not a data pull. ONE show. At most three network
calls, and any request already on disk is served from raw/ and not re-requested.

Call 3 (`extended=episodes,full`) is not a third variant. It exists because
Section 3.4 requires flagging shows where `episode_count`, `aired_episodes` and
`|E|` disagree, which is only checkable if the season-level counts and the
episode list arrive in one payload. Variant B without `full` may not carry them.

The Client ID is loaded from .env by the client at runtime and appears nowhere
in this file, in logs/, or in artifacts/.

Writes:  raw/ (bodies, via the client), logs/step1_episode_listing_probe.json
Reads :  raw/ cache for anything already pulled
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from trakt_client import (  # noqa: E402
    AccessBlocked,
    RateLimitPersistent,
    TraktClient,
    TraktClientError,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = PROJECT_ROOT / "logs" / "step1_episode_listing_probe.json"

# One third-party show. Already partially on disk from Step 0, so the
# ?extended=full seasons payload costs zero network calls.
SHOW = "breaking-bad"

EPISODE_KEYS_REQUIRED = ("season", "number")


def _summarise_episode_list(episodes, season_number):
    """What the definition actually needs out of a payload: E, L, F."""
    if not isinstance(episodes, list):
        return {"error": f"not a list: {type(episodes).__name__}"}

    numbers = []
    missing_number = 0
    missing_season = 0
    wrong_season = 0
    for ep in episodes:
        if not isinstance(ep, dict):
            missing_number += 1
            continue
        num = ep.get("number")
        if not isinstance(num, int):
            missing_number += 1
            continue
        if "season" not in ep:
            missing_season += 1
        elif season_number is not None and ep.get("season") != season_number:
            wrong_season += 1
        numbers.append(num)

    E = sorted(set(numbers))
    return {
        "records": len(episodes),
        "E": E,
        "L_derived_len_E": len(E),
        "F_derived_max_E": max(E) if E else None,
        "duplicate_numbers_in_payload": len(numbers) - len(E),
        "records_missing_integer_number": missing_number,
        "records_missing_season_field": missing_season,
        "records_with_mismatched_season": wrong_season,
        "contiguous_from_1": E == list(range(1, len(E) + 1)) if E else None,
        "episode_object_keys": sorted(episodes[0].keys()) if episodes and isinstance(episodes[0], dict) else [],
    }


def _call(client, endpoint, params, label, records):
    resp = client.get(endpoint, params)
    records.append({
        "label": label,
        "method": "GET",
        "endpoint": endpoint,
        "params": params or {},
        "status": resp.status,
        "ok": resp.ok,
        "unavailable": resp.unavailable,
        "served_from_disk": resp.from_cache,
        "pagination_headers": resp.pagination,
        "raw_path": str(resp.raw_path) if resp.raw_path else None,
    })
    return resp


def main() -> int:
    client = TraktClient(run_label="step1-episode-listing-probe")
    call_records: list[dict] = []
    findings: dict = {
        "probe": "step1 section 3.3 precondition: is E derivable on Client ID alone",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "show_slug": SHOW,
        "auth_mode": "client-id-only, no OAuth",
        "network_call_budget": 3,
    }

    try:
        # --- Variant A: GET /shows/:id/seasons/:season ---------------------
        # Section 3.3 names this form exactly. No extended param: the question
        # is whether the bare, cheapest form already carries episode numbers.
        a_s1 = _call(client, f"shows/{SHOW}/seasons/1", None, "variant_A_season_1", call_records)

        # Season 2 under a sibling route is ALREADY on raw/ from an earlier
        # Step 0 probe. Served from disk, never re-requested, zero network
        # cost, and it gives a second season to compare against for free.
        a_s2 = _call(client, f"shows/{SHOW}/seasons/2/episodes", {"extended": "full"},
                     "on_disk_season_2_episodes_route", call_records)

        findings["variant_A"] = {
            "endpoint_form": "GET /shows/:id/seasons/:season",
            "calls_per_show": "one per season, so two for S1+S2",
            "season_1": {
                "status": a_s1.status,
                "pagination_headers": a_s1.pagination,
                **_summarise_episode_list(a_s1.data, 1),
            },
            "season_2_from_disk_sibling_route": {
                "endpoint_form": "GET /shows/:id/seasons/:season/episodes",
                "served_from_disk": a_s2.from_cache,
                "status": a_s2.status,
                "pagination_headers": a_s2.pagination,
                **_summarise_episode_list(a_s2.data, 2),
            },
        }

        # --- Variant B: GET /shows/:id/seasons?extended=episodes -----------
        b = _call(client, f"shows/{SHOW}/seasons", {"extended": "episodes"},
                  "variant_B_extended_episodes", call_records)

        b_seasons = []
        if isinstance(b.data, list):
            for season in b.data:
                if not isinstance(season, dict):
                    continue
                num = season.get("number")
                b_seasons.append({
                    "season_number": num,
                    "season_object_keys": sorted(season.keys()),
                    "has_episodes_key": "episodes" in season,
                    "season_level_episode_count": season.get("episode_count"),
                    "season_level_aired_episodes": season.get("aired_episodes"),
                    **_summarise_episode_list(season.get("episodes", []), num),
                })
        findings["variant_B"] = {
            "endpoint_form": "GET /shows/:id/seasons?extended=episodes",
            "calls_per_show": "one, all seasons in a single payload",
            "status": b.status,
            "pagination_headers": b.pagination,
            "seasons_returned": len(b_seasons),
            "season_numbers": [s["season_number"] for s in b_seasons],
            "includes_season_0_specials": any(s["season_number"] == 0 for s in b_seasons),
            "seasons": b_seasons,
        }

        # --- Variant B + full: does one payload carry E AND the counts? ----
        bf = _call(client, f"shows/{SHOW}/seasons", {"extended": "episodes,full"},
                   "variant_B_extended_episodes_full", call_records)

        bf_seasons = []
        if isinstance(bf.data, list):
            for season in bf.data:
                if not isinstance(season, dict):
                    continue
                num = season.get("number")
                summary = _summarise_episode_list(season.get("episodes", []), num)
                ec = season.get("episode_count")
                ae = season.get("aired_episodes")
                bf_seasons.append({
                    "season_number": num,
                    "has_episodes_key": "episodes" in season,
                    "season_level_episode_count": ec,
                    "season_level_aired_episodes": ae,
                    "season_first_aired": season.get("first_aired"),
                    "episode_has_first_aired": "first_aired" in (season.get("episodes") or [{}])[0]
                    if season.get("episodes") else None,
                    "section_3_4_disagreement": {
                        "len_E_vs_episode_count": (summary.get("L_derived_len_E"), ec),
                        "len_E_vs_aired_episodes": (summary.get("L_derived_len_E"), ae),
                        "all_three_agree": (
                            summary.get("L_derived_len_E") == ec == ae
                            if isinstance(ec, int) and isinstance(ae, int) else None
                        ),
                    },
                    **summary,
                })
        findings["variant_B_full"] = {
            "endpoint_form": "GET /shows/:id/seasons?extended=episodes,full",
            "status": bf.status,
            "pagination_headers": bf.pagination,
            "seasons_returned": len(bf_seasons),
            "seasons": bf_seasons,
        }

        # --- Cross-variant agreement on E ---------------------------------
        def _E_from_B(payload_seasons, n):
            for s in payload_seasons:
                if s.get("season_number") == n:
                    return s.get("E")
            return None

        agreement = {}
        for n, a_resp in ((1, a_s1), (2, a_s2)):
            E_a = _summarise_episode_list(a_resp.data, n).get("E")
            E_b = _E_from_B(b_seasons, n)
            E_bf = _E_from_B(bf_seasons, n)
            agreement[f"season_{n}"] = {
                "E_variant_A_source": "live GET /seasons/1" if n == 1
                                      else "on-disk GET /seasons/2/episodes",
                "E_variant_A": E_a,
                "E_variant_B": E_b,
                "E_variant_B_full": E_bf,
                "A_equals_B": E_a == E_b,
                "A_equals_B_full": E_a == E_bf,
            }
        findings["cross_variant_agreement"] = agreement

        findings["client_counters"] = client.summary()
        findings["throttle_spend"] = client.throttle.spent()
        findings["outcome"] = "completed"

    except AccessBlocked as exc:
        findings["outcome"] = "HARD STOP: 403"
        findings["error"] = str(exc)
    except RateLimitPersistent as exc:
        findings["outcome"] = "STOP: persistent 429"
        findings["error"] = str(exc)
    except TraktClientError as exc:
        findings["outcome"] = f"STOP: {type(exc).__name__}"
        findings["error"] = str(exc)

    findings["calls"] = call_records
    findings["finished_at"] = datetime.now(timezone.utc).isoformat()

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(findings, indent=2, sort_keys=True))
    return 0 if findings.get("outcome") == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
