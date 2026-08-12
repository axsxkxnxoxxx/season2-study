"""Outcome-neutrality check on the 287 users discarded by decision 0012.

Question: does the sweep-completeness tolerance select on the outcome? If the
discarded users' S1-completer rate and has-any-S2 rate match the retained
2,549, the discard is outcome-neutral. If they differ, the tolerance is
selecting on the thing the study measures.

READ ONLY on the pull. ZERO API calls: the discarded users' pages were never
written to processed/step4/parsed/ under 0012, but the raw bodies are still
cached under raw/users/<slug>/history/.

Both populations go through the SAME metric function, so a difference in the
output cannot be a difference in method. The two extractors differ only in
their source — raw page JSON for the discarded, the committed S1/S2 scan for
the retained — and §1 validates them against each other on shared users.

Detail  -> processed/step5/discard_neutrality/*
Aggregates -> caller writes the artifact; this prints and stores JSON.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
RAW = ROOT / "raw" / "users"
P5 = ROOT / "processed" / "step5" / "discard_neutrality"
FRAME = ROOT / "processed" / "step2" / "frame.csv"
SCAN = ROOT / "processed" / "s1s2_scan.npz"
LEDGER = ROOT / "processed" / "step4" / "pull_ledger.jsonl"
PARSED = ROOT / "processed" / "step4" / "parsed"


# ---------------------------------------------------------------- frame
def load_frame():
    f = pd.read_csv(FRAME, usecols=["show_trakt_id", "s1_E", "s1_L", "s1_F"])
    e1, need, fin = {}, {}, {}
    for r in f.itertuples():
        s = set(int(x) for x in str(r.s1_E).split(","))
        e1[int(r.show_trakt_id)] = s
        need[int(r.show_trakt_id)] = math.ceil(0.90 * int(r.s1_L))
        fin[int(r.show_trakt_id)] = int(r.s1_F)
    return e1, need, fin


# ---------------------------------------------------------------- extractors
def extract_raw(slug: str):
    """(show, season, number) triples from a user's cached raw history pages.

    Dedup is by record `id` within the user, mirroring the parsed store, which
    is written from the same pages. Distinct-episode collapse happens later, in
    the metric function, for both populations alike.
    """
    d = RAW / slug / "history"
    if not d.exists():
        return []
    out, seen = [], set()
    for p in sorted(d.glob("*.json")):
        if p.name.endswith(".meta.json"):
            continue
        try:
            body = json.loads(p.read_text())
        except Exception:
            continue
        if not isinstance(body, list):
            continue
        for rec in body:
            if rec.get("type") != "episode":
                continue
            rid = rec.get("id")
            if rid in seen:
                continue
            seen.add(rid)
            ep = rec.get("episode") or {}
            sh = (rec.get("show") or {}).get("ids") or {}
            season, number, show = ep.get("season"), ep.get("number"), sh.get("trakt")
            if season not in (1, 2) or number is None or show is None:
                continue
            out.append((int(show), int(season), int(number)))
    return out


def extract_parsed(slug: str):
    """Same triples from the parsed store, for the §1 cross-validation only."""
    import gzip
    p = PARSED / f"{slug}.jsonl.gz"
    if not p.exists():
        return []
    out, seen = [], set()
    with gzip.open(p, "rt") as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("type") != "episode":
                continue
            rid = r.get("id")
            if rid in seen:
                continue
            seen.add(rid)
            s, n, sh = r.get("season"), r.get("number"), r.get("show_trakt")
            if s not in (1, 2) or n is None or sh is None:
                continue
            out.append((int(sh), int(s), int(n)))
    return out


# ---------------------------------------------------------------- metric
def metrics(user_records, e1, need, fin):
    """Step 1 Sec 4 on the real E1 from the Step 2 frame.

    user_records: {user_key: [(show, season, number), ...]}
    Returns per-user completer counts and per-pair has-S2 flags.
    """
    per_user, pairs = {}, []
    for u, recs in user_records.items():
        s1 = defaultdict(set)
        s2 = defaultdict(set)
        for show, season, number in recs:
            if show not in e1:
                continue                      # in-frame shows only
            (s1 if season == 1 else s2)[show].add(number)
        n_comp = 0
        for show, nums in s1.items():
            d1 = nums & e1[show]              # membership by SET, Sec 3.2
            if not d1:
                continue
            if max(d1) == fin[show] and len(d1) >= need[show]:
                n_comp += 1
                pairs.append((u, show, 1 if s2.get(show) else 0))
        per_user[u] = n_comp
    return per_user, pairs


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * (c - h), 2), round(100 * (c + h), 2))


def describe(per_user, pairs, label):
    counts = np.array(sorted(per_user.values()), dtype=float)
    k = sum(x[2] for x in pairs)
    n = len(pairs)
    lo, hi = wilson(k, n)
    return {
        "population": label,
        "users": len(per_user),
        "users_with_at_least_one_completer": int((counts > 0).sum()),
        "completer_pairs": n,
        "completers_per_user": {
            "mean": round(float(counts.mean()), 3) if counts.size else None,
            "p10": float(np.percentile(counts, 10)) if counts.size else None,
            "p25": float(np.percentile(counts, 25)) if counts.size else None,
            "median": float(np.percentile(counts, 50)) if counts.size else None,
            "p75": float(np.percentile(counts, 75)) if counts.size else None,
            "p90": float(np.percentile(counts, 90)) if counts.size else None,
            "max": float(counts.max()) if counts.size else None,
        },
        "completers_with_any_s2": k,
        "has_any_s2_rate_pct": round(100 * k / n, 2) if n else None,
        "has_any_s2_rate_ci95_pct": [lo, hi],
    }


def main():
    P5.mkdir(parents=True, exist_ok=True)
    e1, need, fin = load_frame()

    disc = sorted({json.loads(l)["slug"] for l in open(LEDGER)
                   if json.loads(l).get("outcome") == "discarded_over_tolerance"})
    comp = sorted({json.loads(l)["slug"] for l in open(LEDGER)
                   if json.loads(l).get("outcome") == "complete"})
    print(f"discarded {len(disc)} | complete {len(comp)}", flush=True)

    # ---- 1. cross-validate the two extractors on shared users
    val = []
    for slug in comp[:25]:
        a = set(extract_raw(slug))
        b = set(extract_parsed(slug))
        if not b:
            continue
        val.append({"raw_only": len(a - b), "parsed_only": len(b - a), "shared": len(a & b)})
    agree = sum(1 for v in val if v["raw_only"] == 0 and v["parsed_only"] == 0)
    print(f"extractor validation on {len(val)} complete users: {agree} exact matches", flush=True)

    # ---- 2. discarded population, from raw
    disc_rec = {}
    for i, slug in enumerate(disc, 1):
        disc_rec[slug] = extract_raw(slug)
        if i % 50 == 0:
            print(f"  raw {i}/{len(disc)}", flush=True)
    d_user, d_pairs = metrics(disc_rec, e1, need, fin)

    # ---- 3. retained population, from the committed S1/S2 scan
    z = np.load(SCAN)
    df = pd.DataFrame({"user": z["user"], "show": z["show"],
                       "season": z["season"], "number": z["number"]})
    df = df[df["show"].isin(e1.keys())]
    ret_rec = defaultdict(list)
    for u, sh, se, nu in df.itertuples(index=False):
        ret_rec[int(u)].append((int(sh), int(se), int(nu)))
    r_user, r_pairs = metrics(ret_rec, e1, need, fin)

    a = describe(d_user, d_pairs, "discarded_over_tolerance (287)")
    b = describe(r_user, r_pairs, "complete / retained (2,549)")

    # ---- 4. difference in the has-any-S2 rate
    k1, n1 = a["completers_with_any_s2"], a["completer_pairs"]
    k2, n2 = b["completers_with_any_s2"], b["completer_pairs"]
    p1, p2 = k1 / n1, k2 / n2
    pool = (k1 + k2) / (n1 + n2)
    se = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
    zstat = (p1 - p2) / se
    se_d = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    diff = {
        "difference_pct_points": round(100 * (p1 - p2), 3),
        "ci95_pct_points": [round(100 * (p1 - p2 - 1.96 * se_d), 3),
                            round(100 * (p1 - p2 + 1.96 * se_d), 3)],
        "z": round(zstat, 3),
        "two_sided_p": round(2 * (1 - 0.5 * (1 + math.erf(abs(zstat) / math.sqrt(2)))), 5),
    }

    out = {"generated_at": "2026-08-12", "api_calls": 0,
           "rule": "Step 1 Sec 4 on the real E1/L1/F1 from the 1,138-show Step 2 frame; "
                   "identical metric function applied to both populations",
           "extractor_validation": {"users_checked": len(val), "exact_matches": agree,
                                    "detail": val[:5]},
           "discarded": a, "retained": b, "difference_has_any_s2": diff}
    (P5 / "summary.json").write_text(json.dumps(out, indent=2))
    pd.DataFrame(sorted(d_user.items()), columns=["slug", "completers"]).to_csv(
        P5 / "discarded_per_user.csv", index=False)
    pd.DataFrame(d_pairs, columns=["slug", "show_trakt_id", "has_any_s2"]).to_csv(
        P5 / "discarded_pairs.csv", index=False)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
