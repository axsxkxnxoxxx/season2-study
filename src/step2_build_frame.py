"""Step 2 frame, build pass. Zero API calls.

Applies the Human Lead's written selection rules to the fetched seasons
payloads, in the order given, and emits:

  processed/step2/frame.csv              the frame table
  processed/step2/frame-summary.json     every aggregate, machine readable
  processed/step2/undecided.csv          rows the rules do not decide

Rules that the written spec does not decide are NOT resolved here. Affected
shows go to an `undecided` bucket, are counted in the ledger, and are excluded
from the frame table pending the Human Lead. See decisions/0013 condition 3.
"""
from __future__ import annotations

import gzip
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
STEP2 = ROOT / "processed" / "step2"
EXTRACT = STEP2 / "seasons_extract.jsonl.gz"
LEDGER = STEP2 / "seasons_ledger.jsonl"
DIAG = ROOT / "processed" / "s1-completer-diagnostic-per-show.csv"
OUT_FRAME = STEP2 / "frame.csv"
OUT_UNDEC = STEP2 / "excluded_s2_unaired.csv"
OUT_JSON = STEP2 / "frame-summary.json"
SHOWS = STEP2 / "shows_extract.jsonl.gz"
SCAN = ROOT / "processed" / "s1s2_scan.npz"

# Structural thresholds, Human Lead 2026-08-12 (decision 0020). Applied in
# this order: season size, then gap. No minimum season size is set.
MAX_SEASON_EPISODES = 26
MAX_GAP_DAYS = 1095

# Air period, Human Lead 2026-08-12: the calendar year of the S2 finale,
# bucketed to bracket the 2020 production shutdown and nothing finer.
AIR_PERIOD_BUCKETS = [("pre-2020", 0, 2019), ("2020-2022", 2020, 2022),
                      ("2023-2025", 2023, 2025)]


def air_period(year):
    if year is None:
        return None
    for label, lo, hi in AIR_PERIOD_BUCKETS:
        if lo <= year <= hi:
            return label
    return f"post-2025 ({year})"

# Step 1 Sec 2.4 / D13: half-open UTC instants. "aired on or before 31 Dec 2025"
# is therefore first_aired < 2026-01-01T00:00:00Z.
CUTOFF = datetime(2026, 1, 1, tzinfo=timezone.utc)
TAU_PULL = pd.Timestamp("2026-08-11", tz="UTC")  # decision 0011


def parse_dt(s):
    if not s or not isinstance(s, str):
        return None
    try:
        return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def day_delta(a, b):
    """Whole UTC calendar days from b to a (Step 1 Sec 0)."""
    if a is None or b is None:
        return None
    return (a.date() - b.date()).days


def _bucket_of(span, weekly):
    """D12 buckets, first match wins, given a span and a weekly_span."""
    if span is None or weekly is None or span < 0:
        return "C0"
    if span <= 1:
        return "C1"
    if abs(span - weekly) <= 3:
        return "C2"
    if 1 < span < weekly - 3:
        return "C3"
    if span > weekly + 3:
        return "C4"
    return "C0"


def cadence_bucket(P, F_d, L2, probe=15):
    """D12, first match wins. Returns (bucket, span, weekly_span, dist_to_boundary).

    `dist_to_boundary` is the smallest change in `span`, in days, that would put
    the show in a different bucket. D12 requires the count of shows within one
    day of any boundary, so the measure has to be "how far from flipping", not
    "how far from a threshold value" — under the latter every same-day drop
    (span 0, one day from the span<=1 threshold) counts as fragile when in fact
    it takes a two-day move to dislodge it.
    """
    if P is None or F_d is None or not L2:
        return "C0", None, None, None
    span = day_delta(F_d, P)
    weekly = (L2 - 1) * 7
    if span is None or span < 0:
        return "C0", span, weekly, None
    here = _bucket_of(span, weekly)
    dist = None
    for d in range(1, probe + 1):
        # Only probe spans that a real release could have. A negative span is
        # impossible, so "span - 1 would be C0" is an artifact of the probe,
        # not evidence that a same-day drop sits one day from reclassification.
        alts = [s for s in (span - d, span + d) if s >= 0]
        if any(_bucket_of(s, weekly) != here for s in alts):
            dist = d
            break
    return here, span, weekly, dist


def main():
    diag = pd.read_csv(DIAG, usecols=["show_trakt_id", "title", "show_year", "completers"])
    diag = diag.set_index("show_trakt_id")
    cand_ids = set(diag[diag["completers"] >= 50].index)

    led = {}
    with open(LEDGER) as fh:
        for line in fh:
            r = json.loads(line)
            led[int(r["show_trakt_id"])] = r

    payloads = {}
    with gzip.open(EXTRACT, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            payloads[int(r["show_trakt_id"])] = r["seasons"]

    ledger_steps = []
    remaining = set(cand_ids)
    ledger_steps.append(("Candidate set: shows with >= 50 S1 completers, full-pool diagnostic",
                         0, len(remaining)))

    # ---- Rule 1: the seasons payload must have been fetched successfully
    bad_fetch = {s for s in remaining
                 if led.get(s, {}).get("outcome") != "ok" or s not in payloads}
    remaining -= bad_fetch
    ledger_steps.append(("Seasons payload not retrieved (unavailable / error / not fetched)",
                         len(bad_fetch), len(remaining)))

    rows, undecided = [], []
    n_had_season0 = 0

    for sid in sorted(remaining):
        seasons = payloads[sid]
        by_num = {}
        for s in seasons:
            n = s.get("number")
            if n is None:
                continue
            by_num[int(n)] = s
        if 0 in by_num:
            n_had_season0 += 1
        # Season 0 is filtered from every episode-set and length computation.
        by_num.pop(0, None)

        s1, s2 = by_num.get(1), by_num.get(2)

        def eps_of(s):
            if not s:
                return []
            out = []
            for e in s.get("episodes") or []:
                n = e.get("number")
                if n is None or int(n) < 1:
                    continue
                out.append(e)
            return out

        e1, e2 = eps_of(s1), eps_of(s2)
        E1 = sorted({int(e["number"]) for e in e1})
        E2 = sorted({int(e["number"]) for e in e2})

        base = {
            "show_trakt_id": sid,
            "title": diag.at[sid, "title"] if sid in diag.index else None,
            "show_year": diag.at[sid, "show_year"] if sid in diag.index else None,
            "pool_completers": int(diag.at[sid, "completers"]) if sid in diag.index else None,
        }

        # ---- season 1 must be present to record S1 fields at all
        if s1 is None or not E1:
            undecided.append({**base, "reason": "no season 1 in the seasons payload, "
                                                "or season 1 lists no episodes"})
            continue

        first1 = {e["number"]: e for e in e1}
        L1, F1 = len(E1), max(E1)
        s1_prem = parse_dt(first1[min(E1)].get("first_aired"))
        s1_fin = parse_dt(first1[F1].get("first_aired"))

        rec = {
            **base,
            "s1_L": L1,
            "s1_F": F1,
            "s1_E": ",".join(str(n) for n in E1),
            "s1_episode_count_reported": s1.get("episode_count"),
            "s1_aired_episodes_reported": s1.get("aired_episodes"),
            "s1_premiere_date": s1_prem.date().isoformat() if s1_prem else None,
            "s1_finale_date": s1_fin.date().isoformat() if s1_fin else None,
            "s1_season_first_aired": (parse_dt(s1.get("first_aired")).date().isoformat()
                                      if parse_dt(s1.get("first_aired")) else None),
            # Per-season `network` is DROPPED as a field (Human Lead, 2026-08-12):
            # 0.71% populated across 6,645 season objects is not measurable, and
            # decisions/0014's resolution rule says drop it and state the limit.
            # It is still counted in the field inventory below as evidence.
            "s1_total_runtime": s1.get("total_runtime"),
            "s1_count_disagreement": not (s1.get("episode_count") == s1.get("aired_episodes") == L1),
            "s1_aired_lt_listed": (s1.get("aired_episodes") is not None
                                   and s1.get("aired_episodes") < L1),
            "seasons_returned": len(seasons),
            "season_numbers": ",".join(str(n) for n in sorted(by_num)),
            "max_season_number": max(by_num) if by_num else None,
        }

        # ---- Rule 2: a real season 2 must exist
        if s2 is None or not E2:
            rec["exclusion"] = "no_real_season_2"
            rows.append(rec)
            continue

        first2 = {e["number"]: e for e in e2}
        L2, F2 = len(E2), max(E2)
        s2_prem = parse_dt(first2[min(E2)].get("first_aired"))
        s2_fin = parse_dt(first2[F2].get("first_aired"))

        bucket, span, weekly, dist = cadence_bucket(s2_prem, s2_fin, L2)
        rec.update({
            "s2_L": L2,
            "s2_F": F2,
            "s2_E": ",".join(str(n) for n in E2),
            "s2_episode_count_reported": s2.get("episode_count"),
            "s2_aired_episodes_reported": s2.get("aired_episodes"),
            "s2_premiere_date": s2_prem.date().isoformat() if s2_prem else None,
            "s2_finale_date": s2_fin.date().isoformat() if s2_fin else None,
            "s2_season_first_aired": (parse_dt(s2.get("first_aired")).date().isoformat()
                                      if parse_dt(s2.get("first_aired")) else None),
            "s2_total_runtime": s2.get("total_runtime"),
            "s2_count_disagreement": not (s2.get("episode_count") == s2.get("aired_episodes") == L2),
            "s2_aired_lt_listed": (s2.get("aired_episodes") is not None
                                   and s2.get("aired_episodes") < L2),
            "s2_finale_year": s2_fin.year if s2_fin else None,
            "air_period": air_period(s2_fin.year if s2_fin else None),
            "gap_days": day_delta(s2_prem, s1_fin),
            "s2_span_days": span,
            "s2_weekly_span_days": weekly,
            "cadence_bucket": bucket,
            "cadence_boundary_distance_days": dist,
            # Two distinct properties, kept apart on purpose. A season numbered
            # 33..53 has no internal gap but does not start at 1 (absolute
            # numbering across seasons); a season numbered 1,2,4 does. Only the
            # first is the Step 1 Sec 3.3 gap hypothesis; the second breaks the
            # assumption that E2 begins at episode 1.
            "e1_starts_at_1": min(E1) == 1,
            "e2_starts_at_1": min(E2) == 1,
            "e1_internal_gap": E1 != list(range(min(E1), max(E1) + 1)),
            "e2_internal_gap": E2 != list(range(min(E2), max(E2) + 1)),
        })

        # ---- Rule 3: S2 finale aired on or before 31 Dec 2025
        if s2_fin is None:
            # Human Lead, 2026-08-12: excluded. All 12 report aired_episodes = 0,
            # so the season has not aired and cannot have a finale on or before
            # the cutoff. Held in the previous build; now a decided rule.
            rec["exclusion"] = "s2_listed_but_unaired"
            undecided.append({**base, "reason": "season 2 listed with episodes but its finale "
                                                "(max(E2)) carries no first_aired",
                              "s2_L": L2, "s2_F": F2,
                              "s2_premiere_date": rec["s2_premiere_date"],
                              "s2_aired_episodes_reported": s2.get("aired_episodes")})
            rows.append(rec)
            continue

        if s2_fin >= CUTOFF:
            rec["exclusion"] = "s2_finale_after_2025_12_31"
            rows.append(rec)
            continue

        # ---- Structural thresholds (Human Lead, 2026-08-12, decision 0020).
        # No minimum season size: Step 1 Sec 4's ceil(0.90 * L1) already scales
        # to the real per-show length, so a short season needs no floor.
        if L1 > MAX_SEASON_EPISODES or L2 > MAX_SEASON_EPISODES:
            rec["exclusion"] = "season_over_26_episodes"
            rows.append(rec)
            continue

        gap = rec["gap_days"]
        if gap is None:
            rec["exclusion"] = "UNDECIDED_gap_not_computable"
            rows.append(rec)
            continue
        if gap > MAX_GAP_DAYS:
            rec["exclusion"] = "gap_over_1095_days"
            rows.append(rec)
            continue

        rec["exclusion"] = None
        rows.append(rec)

    df = pd.DataFrame(rows)

    n_no_s1 = sum(1 for u in undecided if "no season 1" in u["reason"])
    remaining -= {u["show_trakt_id"] for u in undecided
                  if "no season 1" in u.get("reason", "")}
    ledger_steps.append(("No season 1 in the payload", n_no_s1, len(remaining)))

    n_no_s2 = int((df["exclusion"] == "no_real_season_2").sum())
    remaining -= set(df.loc[df["exclusion"] == "no_real_season_2", "show_trakt_id"])
    ledger_steps.append(("No real season 2", n_no_s2, len(remaining)))

    n_undated = int((df["exclusion"] == "s2_listed_but_unaired").sum())
    remaining -= set(df.loc[df["exclusion"] == "s2_listed_but_unaired", "show_trakt_id"])
    ledger_steps.append(("S2 listed but unaired (no finale air date, aired_episodes = 0)",
                         n_undated, len(remaining)))

    n_late = int((df["exclusion"] == "s2_finale_after_2025_12_31").sum())
    remaining -= set(df.loc[df["exclusion"] == "s2_finale_after_2025_12_31", "show_trakt_id"])
    ledger_steps.append(("S2 finale aired after 2025-12-31", n_late, len(remaining)))

    for label, tag in (
        ("Season over 26 episodes (S1 or S2)", "season_over_26_episodes"),
        ("Gap over 1095 days (S1 finale to S2 premiere)", "gap_over_1095_days"),
        ("Gap not computable (rules do not decide) -> UNDECIDED",
         "UNDECIDED_gap_not_computable"),
    ):
        n = int((df["exclusion"] == tag).sum())
        remaining -= set(df.loc[df["exclusion"] == tag, "show_trakt_id"])
        ledger_steps.append((label, n, len(remaining)))

    frame = df[df["exclusion"].isna()].copy()
    assert len(frame) == len(remaining), (len(frame), len(remaining))

    # ---- pool completers, recomputed on the REAL season lengths in the frame.
    # Human Lead, 2026-08-12: the max-observed proxy is superseded and no result
    # may use it. Step 1 Sec 4: F1 in D1 AND |D1| >= ceil(0.90 * L1), with D1 the
    # distinct S1 episodes whose number is a MEMBER of the real E1.
    z = np.load(SCAN)
    scan = pd.DataFrame({"user": z["user"], "show": z["show"],
                         "season": z["season"], "number": z["number"]})
    in_frame = set(frame["show_trakt_id"])
    scan = scan[(scan["season"] == 1) & (scan["show"].isin(in_frame))]
    scan = scan.drop_duplicates(["user", "show", "number"])  # Sec 2.1 distinct episodes

    valid = pd.DataFrame(
        [(sid, n) for sid, e in zip(frame["show_trakt_id"], frame["s1_E"])
         for n in (int(x) for x in str(e).split(","))],
        columns=["show", "number"])
    d1 = scan.merge(valid, on=["show", "number"], how="inner")  # D1 subset of E1
    agg = d1.groupby(["show", "user"]).agg(n_d1=("number", "size"),
                                           max_d1=("number", "max")).reset_index()
    real = frame.set_index("show_trakt_id")[["s1_L", "s1_F"]]
    agg = agg.join(real, on="show")
    need = np.ceil(0.90 * agg["s1_L"].to_numpy()).astype(np.int64)
    # F1 in D1 <=> max(D1) == F1, because D1 is a subset of E1 and F1 = max(E1).
    agg["completer"] = (agg["max_d1"].to_numpy() == agg["s1_F"].to_numpy()) & \
                       (agg["n_d1"].to_numpy() >= need)
    real_counts = agg[agg["completer"]].groupby("show").size()

    frame["pool_completers_proxy"] = frame["pool_completers"]
    frame["pool_completers"] = [int(real_counts.get(s, 0)) for s in frame["show_trakt_id"]]

    # ---- title size quintile, cut over the FRAME only (Human Lead, 2026-08-12):
    # the quintile exists to cut results, and results exist only for in-frame shows.
    #
    # `pool_completers` counts users who completed S1 EVER, so a 2012 title has had
    # fourteen years to accumulate them and a 2025 title one. Cut raw, the quintile
    # is a size-AND-AGE composite, not a size field. Two effects partly cancel --
    # recent titles must be larger to clear the >=50 floor at all, older titles
    # accumulate for longer -- which is why it is invisible. Separated here
    # (Human Lead, 2026-08-12, decision 0030).
    LBL = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    exposure_yrs = ((TAU_PULL - pd.to_datetime(frame["s1_premiere_date"], utc=True))
                    .dt.total_seconds() / (86400 * 365.25))
    frame["s1_exposure_years"] = exposure_yrs.round(3)
    frame["completers_per_year"] = (frame["pool_completers"] / exposure_yrs).round(3)
    # PRIMARY: rank within air-period cohort. This is what "size quintile" means.
    # Measured against the frame's own 14.8% share of 2023-2025 titles, the three
    # candidates give 12.3% (raw count), 32.9% (per-year) and 14.9% (within
    # cohort) of Q5. Within-cohort is the only neutral one, and it is neutral by
    # construction rather than by luck.
    #
    # Per-year OVER-corrects, and worse than raw count under-corrects. Completions
    # are front-loaded after release, so dividing by total elapsed years penalises
    # an old title whose accumulation tapered a decade ago: median completers_per_
    # year runs 8.5 (pre-2020), 16.3 (2020-2022), 28.7 (2023-2025) -- a monotone
    # gradient that is pure age, not size. Ranking within cohort compares like
    # with like and assumes nothing about the shape of accumulation.
    frame["size_quintile"] = (
        frame.groupby("air_period")["pool_completers"]
        .transform(lambda s: pd.qcut(s, 5, labels=LBL, duplicates="drop")))
    # Both alternatives retained and explicitly named, so none can be confused.
    frame["size_quintile_raw_count"] = pd.qcut(frame["pool_completers"], 5,
                                               labels=LBL, duplicates="drop")
    frame["size_quintile_per_year"] = pd.qcut(frame["completers_per_year"], 5,
                                              labels=LBL, duplicates="drop")

    # ---- show-level metadata (second endpoint, /shows/:id?extended=full)
    meta_fields = {}
    if SHOWS.exists():
        with gzip.open(SHOWS, "rt") as fh:
            for line in fh:
                r = json.loads(line)
                meta_fields[int(r["show_trakt_id"])] = r["show"]
    keys = sorted({k for m in meta_fields.values() for k in m})
    # `network` is DROPPED (Human Lead, 2026-08-12, decision 0030). It is neither
    # present-day nor release-time and errs in BOTH directions -- Arrested
    # Development (S2 2005) reads Netflix, Brooklyn Nine-Nine reads FOX having
    # ended on NBC -- so it has no stable semantics. A present-day field at least
    # has a known direction of error you could bound; this one does not. A field
    # that cannot be used is safer absent than present.
    #
    # `rating`, `votes`, `comment_count`, `subgenres` and `airs.day` are ADDED
    # from the same cached bodies, at zero API calls. The frame previously had no
    # reception axis at all, so "long gaps abandon more" could not be separated
    # from "long gaps happen to troubled shows".
    for k in ("country", "language", "languages", "genres", "subgenres", "status",
              "runtime", "certification", "aired_episodes", "first_aired", "year",
              "rating", "votes", "comment_count"):
        if k in keys:
            frame["show_" + k] = [
                (", ".join(meta_fields.get(s, {}).get(k) or [])
                 if isinstance(meta_fields.get(s, {}).get(k), list)
                 else meta_fields.get(s, {}).get(k))
                for s in frame["show_trakt_id"]]
    # `airs` is nested {day, time, timezone}; day-of-week is a release-plan lever
    frame["show_airs_day"] = [
        ((meta_fields.get(s, {}).get("airs") or {}) or {}).get("day")
        for s in frame["show_trakt_id"]]

    frame.to_csv(OUT_FRAME, index=False)
    pd.DataFrame(undecided).to_csv(OUT_UNDEC, index=False)
    # Every candidate that reached the rule pass, in-frame or not, so the
    # ledger in the artifact is auditable per show rather than only in total.
    df.to_csv(STEP2 / "all_candidates_scored.csv", index=False)

    # ------------------------------------------------------------ aggregates
    def dist(series, name):
        a = pd.to_numeric(series, errors="coerce").dropna().to_numpy(dtype=float)
        if a.size == 0:
            return {"n": 0}
        return {
            "n": int(a.size), "missing": int(len(series) - a.size),
            "min": float(a.min()), "p05": float(np.percentile(a, 5)),
            "p25": float(np.percentile(a, 25)), "median": float(np.percentile(a, 50)),
            "p75": float(np.percentile(a, 75)), "p90": float(np.percentile(a, 90)),
            "p95": float(np.percentile(a, 95)), "max": float(a.max()),
            "mean": round(float(a.mean()), 2),
        }

    def hist(series, bins, labels):
        a = pd.to_numeric(series, errors="coerce")
        b = pd.cut(a, bins=bins, labels=labels, right=False)
        out = b.value_counts().reindex(labels).fillna(0).astype(int).to_dict()
        out["missing"] = int(a.isna().sum())
        return out

    gap_bins = [-10**9, 0, 90, 180, 270, 365, 547, 730, 1095, 1825, 10**9]
    gap_labels = ["negative", "0-89d", "90-179d", "180-269d", "270-364d", "1-1.5y",
                  "1.5-2y", "2-3y", "3-5y", "5y+"]
    ep_bins = [0, 4, 7, 9, 11, 14, 23, 27, 10**9]
    ep_labels = ["1-3", "4-6", "7-8", "9-10", "11-13", "14-22", "23-26", "27+"]

    cad = frame["cadence_bucket"].value_counts().reindex(
        ["C0", "C1", "C2", "C3", "C4"]).fillna(0).astype(int).to_dict()
    near = pd.to_numeric(frame["cadence_boundary_distance_days"], errors="coerce")

    # field inventory over the frame AND over every fetched payload
    def populated(series):
        s = pd.Series(series)
        nonnull = int(s.notna().sum())
        return {"present_rows": int(len(s)), "non_null": nonnull,
                "non_null_pct": round(100 * nonnull / len(s), 2) if len(s) else None,
                "distinct_non_null": int(s.dropna().nunique())}

    show_meta_inventory = {}
    for k in keys:
        vals = [meta_fields.get(s, {}).get(k) for s in frame["show_trakt_id"]]
        nonnull = sum(1 for v in vals if v not in (None, "", [], {}))
        show_meta_inventory[k] = {
            "non_null": nonnull,
            "non_null_pct": round(100 * nonnull / len(frame), 2) if len(frame) else None,
            "distinct": len({json.dumps(v, sort_keys=True) for v in vals
                             if v not in (None, "", [], {})}),
        }

    all_season_networks, per_show_network_sets = [], []
    for sid, seasons in payloads.items():
        nets = set()
        for s in seasons:
            if s.get("number") == 0:
                continue
            all_season_networks.append(s.get("network"))
            if s.get("network"):
                nets.add(s.get("network"))
        per_show_network_sets.append(len(nets))

    prox = pd.to_numeric(frame["pool_completers_proxy"], errors="coerce")
    realc = pd.to_numeric(frame["pool_completers"], errors="coerce")
    recompute = {
        "rule": "Step 1 Sec 4 on the real E1/L1/F1 now in the frame; the "
                "max-observed proxy is superseded",
        "total_completer_pairs_proxy": int(prox.sum()),
        "total_completer_pairs_real": int(realc.sum()),
        "shows_where_count_rose": int((realc > prox).sum()),
        "shows_where_count_fell": int((realc < prox).sum()),
        "shows_unchanged": int((realc == prox).sum()),
        "shows_now_below_50": int((realc < 50).sum()),
        "shows_now_zero": int((realc == 0).sum()),
        "real": dist(frame["pool_completers"], "real"),
        "proxy": dist(frame["pool_completers_proxy"], "proxy"),
        "note": "The >=50 candidate rule was applied on the proxy counts and has "
                "NOT been re-applied on these. Whether it should be is a Human "
                "Lead call; no show was added or removed here.",
    }

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api_calls_this_pass": 0,
        "pool_completers_recompute": recompute,
        "candidate_set": {"rule": ">= 50 S1 completers on the full-pool diagnostic",
                          "shows": len(cand_ids)},
        "exclusion_ledger": [
            {"step": i, "rule": r, "removed": rm, "remaining": rem}
            for i, (r, rm, rem) in enumerate(ledger_steps)
        ],
        "frame_size": int(len(frame)),
        "undecided_total": int(len(undecided)),
        "shows_with_a_season_0_filtered": n_had_season0,
        "distributions": {
            "gap_days": dist(frame["gap_days"], "gap"),
            "gap_days_hist": hist(frame["gap_days"], gap_bins, gap_labels),
            "s1_L": dist(frame["s1_L"], "s1"),
            "s1_L_hist": hist(frame["s1_L"], ep_bins, ep_labels),
            "s2_L": dist(frame["s2_L"], "s2"),
            "s2_L_hist": hist(frame["s2_L"], ep_bins, ep_labels),
            "s2_span_days": dist(frame["s2_span_days"], "span"),
            "cadence_bucket": cad,
            "cadence_boundary_within_1_day": int((near <= 1).sum()),
            "cadence_boundary_within_3_days": int((near <= 3).sum()),
            "pool_completers": dist(frame["pool_completers"], "completers"),
        },
        "step1_sec_3_4_checks": {
            "s1_count_disagreement": int(frame["s1_count_disagreement"].sum()),
            "s2_count_disagreement": int(frame["s2_count_disagreement"].sum()),
            "s2_aired_lt_listed": int(frame["s2_aired_lt_listed"].sum()),
            "s1_aired_lt_listed": int(frame["s1_aired_lt_listed"].sum()),
            # astype(bool) first: the column is object dtype, and `~` on object
            # bools is integer bitwise negation (~True == -2), which silently
            # produced a negative count.
            "e1_does_not_start_at_1": int((~frame["e1_starts_at_1"].astype(bool)).sum()),
            "e2_does_not_start_at_1": int((~frame["e2_starts_at_1"].astype(bool)).sum()),
            "e1_internal_gap": int(frame["e1_internal_gap"].astype(bool).sum()),
            "e2_internal_gap": int(frame["e2_internal_gap"].astype(bool).sum()),
        },
        "air_period": frame["air_period"].value_counts().to_dict(),
        "field_inventory": {
            "note": "Populated over the frame unless stated. No fragmentation is inferred.",
            "show_level_fields_from_shows_endpoint": show_meta_inventory,
            "s1_premiere_date": populated(frame["s1_premiere_date"]),
            "s1_finale_date": populated(frame["s1_finale_date"]),
            "s2_premiere_date": populated(frame["s2_premiere_date"]),
            "s2_finale_date": populated(frame["s2_finale_date"]),
            "s1_season_first_aired": populated(frame["s1_season_first_aired"]),
            "s2_season_first_aired": populated(frame["s2_season_first_aired"]),
            "per_season_network_DROPPED_AS_A_FIELD": {
                "decided_by": "Human Lead, 2026-08-12",
                "reason": "0.71% populated is not measurable; decisions/0014's "
                          "resolution rule is drop it and state the limitation",
                "evidence_retained_below": True,
            },
            "season_level_network_all_fetched_shows": {
                "season_objects_seen_excluding_s0": len(all_season_networks),
                "non_null": int(sum(1 for x in all_season_networks if x)),
                "non_null_pct": round(
                    100 * sum(1 for x in all_season_networks if x) / len(all_season_networks), 2)
                if all_season_networks else None,
            },
            "distinct_non_null_networks_per_show": {
                "shows": len(per_show_network_sets),
                "zero": int(sum(1 for n in per_show_network_sets if n == 0)),
                "exactly_one": int(sum(1 for n in per_show_network_sets if n == 1)),
                "two_or_more": int(sum(1 for n in per_show_network_sets if n >= 2)),
            },
            "all_keys_returned_by_shows_endpoint": keys,
        },
        "size_quintile_frame_base": frame["size_quintile"].value_counts().sort_index().to_dict(),
        "size_quintile_raw_count": frame["size_quintile_raw_count"].value_counts().sort_index().to_dict(),
        "size_quintile_definition": "quintile of pool_completers ranked WITHIN air_period cohort; "
                                    "exposure-neutral by construction, per 0030",
    }

    with open(OUT_JSON, "w") as fh:
        json.dump(summary, fh, indent=2, default=str)
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
