"""S1-completer diagnostic over the Step 4 snapshot. READ ONLY, zero API calls.

Applies the APPROVED Step 1 Sec 4 rule:  F1 in D1  AND  |D1| >= ceil(0.90 * L1),
with E1 supplied by the max-observed-number proxy (Step 1 Sec 3.3 fallback shape),
because no Step 2 frame exists yet.
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
SCAN = ROOT / "processed" / "s1s2_scan.npz"
OUT_CSV = ROOT / "processed" / "s1-completer-diagnostic-per-show.csv"
OUT_JSON = ROOT / "processed" / "s1-completer-diagnostic-summary.json"

MISSING = np.iinfo(np.int64).min
CUTOFF_2025 = int(datetime(2026, 1, 1, tzinfo=timezone.utc).timestamp())  # < this == on/before 2025-12-31
Y1990 = int(datetime(1990, 1, 1, tzinfo=timezone.utc).timestamp())

z = np.load(SCAN)
df = pd.DataFrame({
    "user": z["user"],
    "show": z["show"],
    "season": z["season"],
    "number": z["number"],
    "ts": z["ts"],
})
raw_rows = len(df)

# ---- Step 1 Sec 2.1 / 2.2: distinct (show, season, number) per user, earliest ts
df = df.groupby(["user", "show", "season", "number"], sort=False, as_index=False)["ts"].min()
distinct_rows = len(df)

s1 = df[df["season"] == 1]
s2 = df[df["season"] == 2]

# ---- season-length proxy: max episode number observed pooled over all cohort users
L1 = s1.groupby("show")["number"].max().rename("L1_hat")
L2 = s2.groupby("show")["number"].max().rename("L2_hat")

# ---- per (user, show)
p1 = s1.groupby(["show", "user"]).agg(n_s1=("number", "size"), max_s1=("number", "max")).reset_index()
p2 = s2.groupby(["show", "user"]).agg(n_s2=("number", "size")).reset_index()

p1 = p1.join(L1, on="show")
# Sec 4: finale watched AND at least ceil(0.90 * L1) distinct S1 episodes
need = np.ceil(0.90 * p1["L1_hat"].to_numpy()).astype(np.int64)
p1["completer"] = (p1["max_s1"].to_numpy() == p1["L1_hat"].to_numpy()) & (p1["n_s1"].to_numpy() >= need)

comp = p1[p1["completer"]].merge(p2, on=["show", "user"], how="left")
comp["n_s2"] = comp["n_s2"].fillna(0).astype(np.int64)

per_show = pd.DataFrame(index=L1.index.union(L2.index, sort=True))
per_show.index.name = "show"
per_show["L1_hat"] = L1
per_show["L2_hat"] = L2
per_show["users_any_s1"] = p1.groupby("show").size()
per_show["users_any_s2"] = p2.groupby("show").size()
per_show["completers"] = comp.groupby("show").size()
per_show["completers_with_any_s2"] = comp[comp["n_s2"] >= 1].groupby("show").size()
per_show = per_show.fillna(0)
for c in ("users_any_s1", "users_any_s2", "completers", "completers_with_any_s2"):
    per_show[c] = per_show[c].astype(np.int64)

# ---- S2 "finished airing" proxy: earliest pooled watch of the S2 finale episode
fin = s2.merge(L2, on="show")
fin = fin[fin["number"] == fin["L2_hat"]]
fin_ok = fin[fin["ts"] != MISSING]
g = fin_ok.groupby("show")["ts"]
per_show["s2_finale_first_watch"] = g.min()
per_show["s2_finale_p10_watch"] = g.quantile(0.10)
per_show["s2_finale_watchers"] = g.size()
fin_1990 = fin_ok[fin_ok["ts"] >= Y1990]
per_show["s2_finale_first_watch_ge1990"] = fin_1990.groupby("show")["ts"].min()

def as_date(col):
    return pd.to_datetime(per_show[col], unit="s", utc=True, errors="coerce").dt.strftime("%Y-%m-%d")

per_show["restricted_min"] = per_show["s2_finale_first_watch"] < CUTOFF_2025
per_show["restricted_p10"] = per_show["s2_finale_p10_watch"] < CUTOFF_2025
per_show["restricted_min_ge1990"] = per_show["s2_finale_first_watch_ge1990"] < CUTOFF_2025

# ---------------------------------------------------------------- reporting
def dist(series):
    a = np.asarray(series, dtype=float)
    if a.size == 0:
        return {}
    return {
        "n_shows": int(a.size),
        "total_completers": int(a.sum()),
        "mean": round(float(a.mean()), 3),
        "p25": float(np.percentile(a, 25)),
        "median": float(np.percentile(a, 50)),
        "p75": float(np.percentile(a, 75)),
        "p90": float(np.percentile(a, 90)),
        "p95": float(np.percentile(a, 95)),
        "p99": float(np.percentile(a, 99)),
        "max": int(a.max()),
    }

def thresholds(series):
    a = np.asarray(series)
    return {f"ge_{t}": int((a >= t).sum()) for t in (1, 10, 25, 50, 100, 250)}

def item3(sub):
    """sub: per_show rows with >= 50 completers."""
    tot_c = int(sub["completers"].sum())
    tot_s2 = int(sub["completers_with_any_s2"].sum())
    share = (sub["completers_with_any_s2"] / sub["completers"]).to_numpy()
    return {
        "shows": int(len(sub)),
        "completers": tot_c,
        "completers_with_any_s2": tot_s2,
        "pooled_share": round(tot_s2 / tot_c, 4) if tot_c else None,
        "per_show_share_p10": round(float(np.percentile(share, 10)), 4) if len(sub) else None,
        "per_show_share_p25": round(float(np.percentile(share, 25)), 4) if len(sub) else None,
        "per_show_share_median": round(float(np.percentile(share, 50)), 4) if len(sub) else None,
        "per_show_share_p75": round(float(np.percentile(share, 75)), 4) if len(sub) else None,
        "per_show_share_p90": round(float(np.percentile(share, 90)), 4) if len(sub) else None,
        "per_show_share_min": round(float(share.min()), 4) if len(sub) else None,
        "per_show_share_max": round(float(share.max()), 4) if len(sub) else None,
        "shows_with_zero_s2_completers": int((sub["completers_with_any_s2"] == 0).sum()),
        "shows_with_no_s2_observed": int((sub["L2_hat"] == 0).sum()),
    }

has_s1 = per_show[per_show["L1_hat"] > 0]
summary = {
    "cohort": {
        "users": int(df["user"].nunique()),
        "raw_s1s2_records": int(raw_rows),
        "distinct_user_show_season_episode": int(distinct_rows),
        "collapse_ratio": round(1 - distinct_rows / raw_rows, 4),
        "shows_with_any_s1_or_s2_record": int(len(per_show)),
        "shows_with_any_s1_record": int(len(has_s1)),
        "shows_with_any_s2_record": int((per_show["L2_hat"] > 0).sum()),
        "user_show_pairs_with_any_s1": int(len(p1)),
        "total_s1_completer_pairs": int(len(comp)),
    },
    "item1_all_shows_with_s1": dist(has_s1["completers"]),
    "item1_all_shows_in_scan": dist(per_show["completers"]),
    "item2_thresholds_shows_with_s1": thresholds(has_s1["completers"]),
    "item3_shows_ge50": item3(per_show[per_show["completers"] >= 50]),
}

for label, mask in (
    ("min", per_show["restricted_min"]),
    ("p10", per_show["restricted_p10"]),
    ("min_ge1990", per_show["restricted_min_ge1990"]),
):
    r = per_show[mask]
    r1 = r[r["L1_hat"] > 0]
    summary[f"item4_{label}"] = {
        "shows_in_restricted_set": int(len(r)),
        "shows_in_restricted_set_with_s1": int(len(r1)),
        "item1": dist(r1["completers"]),
        "item2": thresholds(r1["completers"]),
        "item3": item3(r[r["completers"] >= 50]),
    }

# extra context: how many shows have an S2 finale watch at all
summary["s2_finale_coverage"] = {
    "shows_with_s2_finale_watched_by_someone": int(per_show["s2_finale_watchers"].notna().sum()),
    "shows_with_s2_records_but_no_dated_finale_watch": int(
        ((per_show["L2_hat"] > 0) & per_show["s2_finale_first_watch"].isna()).sum()),
    "shows_whose_min_finale_watch_predates_1990": int(
        (per_show["s2_finale_first_watch"] < Y1990).sum()),
    "shows_whose_min_finale_watch_is_epoch_1970_exact": int(
        (per_show["s2_finale_first_watch"] == 0).sum()),
    "shows_moved_out_of_restricted_set_by_the_1990_guard": int(
        (per_show["restricted_min"] & ~per_show["restricted_min_ge1990"]).sum()),
}

# top shows by completers, for the write-up (titles are public metadata, no user data)
titles = pd.read_csv(ROOT / "processed" / "pool-coverage-per-show.csv",
                     usecols=["show_trakt_id", "title", "show_year"])
titles = titles.drop_duplicates("show_trakt_id").set_index("show_trakt_id")
out = per_show.join(titles, how="left")
out["s2_finale_first_watch_date"] = as_date("s2_finale_first_watch")
out["s2_finale_p10_watch_date"] = as_date("s2_finale_p10_watch")
out["s2_finale_first_watch_ge1990_date"] = as_date("s2_finale_first_watch_ge1990")
cols = ["title", "show_year", "L1_hat", "L2_hat", "users_any_s1", "users_any_s2",
        "completers", "completers_with_any_s2", "s2_finale_watchers",
        "s2_finale_first_watch_date", "s2_finale_p10_watch_date",
        "s2_finale_first_watch_ge1990_date",
        "restricted_min", "restricted_p10", "restricted_min_ge1990"]
out[cols].sort_values("completers", ascending=False).to_csv(OUT_CSV, index_label="show_trakt_id")

top = out.sort_values("completers", ascending=False).head(25)
summary["top25_shows_by_completers"] = [
    {"title": str(r.title), "year": (int(r.show_year) if pd.notna(r.show_year) else None),
     "L1_hat": int(r.L1_hat), "L2_hat": int(r.L2_hat),
     "users_any_s1": int(r.users_any_s1), "completers": int(r.completers),
     "completers_with_any_s2": int(r.completers_with_any_s2),
     "s2_finale_first_watch": r.s2_finale_first_watch_date,
     "restricted_min": bool(r.restricted_min)}
    for r in top.itertuples()
]

# L1 proxy sanity: distribution of L1_hat on shows with >=50 completers
big = per_show[per_show["completers"] >= 50]
summary["L1_hat_on_shows_ge50"] = {
    "min": int(big["L1_hat"].min()), "p25": float(np.percentile(big["L1_hat"], 25)),
    "median": float(np.percentile(big["L1_hat"], 50)), "p75": float(np.percentile(big["L1_hat"], 75)),
    "max": int(big["L1_hat"].max()),
    "shows_with_L1_hat_1": int((big["L1_hat"] == 1).sum()),
    "shows_with_L1_hat_le_3": int((big["L1_hat"] <= 3).sum()),
    "shows_with_L1_hat_gt_30": int((big["L1_hat"] > 30).sum()),
}

with open(OUT_JSON, "w") as fh:
    json.dump(summary, fh, indent=2)
print(json.dumps(summary, indent=2))

# ------------------------------------------------------------------ supplements
sup = {}

# (a) item 3 unrestricted, split by whether the show has any S2 observed at all
big = per_show[per_show["completers"] >= 50]
sup["item3_ge50_split_by_s2_existence"] = {
    "shows_with_no_s2_observed": {
        "shows": int((big["L2_hat"] == 0).sum()),
        "completers": int(big.loc[big["L2_hat"] == 0, "completers"].sum()),
    },
    "shows_with_s2_observed": item3(big[big["L2_hat"] > 0]),
}

# (b) how the two date proxies disagree, over shows with any S2
s2shows = per_show[per_show["L2_hat"] > 0]
sup["date_proxy_agreement_over_shows_with_s2"] = {
    "shows_with_s2": int(len(s2shows)),
    "in_both": int((s2shows["restricted_min"] & s2shows["restricted_p10"]).sum()),
    "min_only": int((s2shows["restricted_min"] & ~s2shows["restricted_p10"]).sum()),
    "p10_only": int((~s2shows["restricted_min"] & s2shows["restricted_p10"]).sum()),
    "in_neither": int((~s2shows["restricted_min"] & ~s2shows["restricted_p10"]).sum()),
    "min_pre1990_but_p10_in_2026": int(
        ((s2shows["s2_finale_first_watch"] < Y1990)
         & (s2shows["s2_finale_p10_watch"] >= CUTOFF_2025)).sum()),
    "shows_with_s2_excluded_by_min": int((~s2shows["restricted_min"]).sum()),
}

# (c) still-airing risk: when was the S1 finale-proxy episode first watched pool-wide
s1fin = s1.merge(L1, on="show")
s1fin = s1fin[(s1fin["number"] == s1fin["L1_hat"]) & (s1fin["ts"] != MISSING)]
s1_first = s1fin.groupby("show")["ts"].min()
s1_p10 = s1fin.groupby("show")["ts"].quantile(0.10)
per_show["s1_finale_first_watch"] = s1_first
per_show["s1_finale_p10_watch"] = s1_p10
big = per_show[per_show["completers"] >= 50]
Y2026 = int(datetime(2026, 1, 1, tzinfo=timezone.utc).timestamp())
Y2025 = int(datetime(2025, 1, 1, tzinfo=timezone.utc).timestamp())
sup["s1_finale_proxy_recency_shows_ge50"] = {
    "shows": int(len(big)),
    "s1_finale_proxy_p10_watch_in_2026": int((big["s1_finale_p10_watch"] >= Y2026).sum()),
    "s1_finale_proxy_p10_watch_in_2025_or_later": int((big["s1_finale_p10_watch"] >= Y2025).sum()),
    "note": "p10 of the pooled first-watch dates of the max-observed S1 episode. A recent p10 "
            "means the proxy finale only became watchable recently, so the true S1 may still be airing "
            "and the proxy may be short.",
}
big2 = big[big["L2_hat"] > 0]
sup["s2_finale_proxy_recency_shows_ge50_with_s2"] = {
    "shows": int(len(big2)),
    "s2_finale_proxy_p10_watch_in_2026": int((big2["s2_finale_p10_watch"] >= Y2026).sum()),
    "s2_finale_proxy_p10_watch_in_2025_or_later": int((big2["s2_finale_p10_watch"] >= Y2025).sum()),
}

# (d) how much of the pool's S1/S2 record mass carries an implausible timestamp
ts_all = df["ts"].to_numpy()
sup["timestamp_anomalies_in_s1s2_scope"] = {
    "distinct_episode_rows": int(len(df)),
    "rows_missing_watched_at": int((ts_all == MISSING).sum()),
    "rows_exactly_epoch_1970_01_01": int((ts_all == 0).sum()),
    "rows_before_1990": int(((ts_all != MISSING) & (ts_all < Y1990)).sum()),
    "share_before_1990": round(float(((ts_all != MISSING) & (ts_all < Y1990)).sum()) / len(df), 5),
}

# (e) proxy season lengths on the shows that carry the headline
sup["L2_hat_on_shows_ge50_with_s2"] = {
    "min": int(big2["L2_hat"].min()), "median": float(np.percentile(big2["L2_hat"], 50)),
    "max": int(big2["L2_hat"].max()),
}

summary["supplements"] = sup
with open(OUT_JSON, "w") as fh:
    json.dump(summary, fh, indent=2)

cols2 = cols + ["s1_finale_first_watch", "s1_finale_p10_watch"]
out2 = per_show.join(titles, how="left")
out2["s2_finale_first_watch_date"] = as_date("s2_finale_first_watch")
out2["s2_finale_p10_watch_date"] = as_date("s2_finale_p10_watch")
out2["s2_finale_first_watch_ge1990_date"] = as_date("s2_finale_first_watch_ge1990")
out2["s1_finale_first_watch_date"] = as_date("s1_finale_first_watch")
out2["s1_finale_p10_watch_date"] = as_date("s1_finale_p10_watch")
out2[cols + ["s1_finale_first_watch_date", "s1_finale_p10_watch_date"]] \
    .sort_values("completers", ascending=False).to_csv(OUT_CSV, index_label="show_trakt_id")

print(json.dumps(sup, indent=2))
