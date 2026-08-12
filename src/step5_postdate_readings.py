"""Step 5: every defensible reading of adoption 3, "exclude the future-dated records".

READ ONLY. Zero network calls. NOTHING ADOPTED - this bounds a question for the
Human Lead.

Adoption 1 keeps all pairs with S2 evidence. Adoption 3 excludes future-dated
records. 3,016 pairs sit in both, so the two point opposite ways.

The coordinator offered two readings. Running them showed the record-level one is
itself ambiguous: "set aside a record" can mean at least three different
operations, and they give materially different answers because a post-dated
completing record is almost never alone - affected pairs hold a MEDIAN OF 12
post-dated S1 records. Post-dating is a block property, like every other
contamination class in this store, so dropping "the" record drops a dozen and
takes the pair below the 90% completion threshold.

  P    pair-level: delete the pair outright
  R1b  record-level, broad drop: remove EVERY post-dated S1 record, recompute
  R1n  record-level, narrow drop: remove only the post-dated COMPLETING record
  R3   record-level, re-date: the claimed date is bogus, so substitute the
       record's insertion time, re-sort, recompute

R3 is the only reading under which the episode stays in D1. Step 1 Sec 2.3
conditions on whether the episode was viewed, not on whether its date is usable,
and the S1-completer diagnostic already applied that logic to undated records -
which is an argument for R3 that the Human Lead should see, not one this file
acts on.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
POSTDATE_D = -30.0
DAY = 86400.0


def parse_set(s):
    return {int(x) for x in str(s).split(",") if x.strip().isdigit()}


def main():
    frame = pd.read_csv(ROOT / "processed" / "step2" / "frame.csv")
    e1 = {int(r.show_trakt_id): parse_set(r.s1_E) for r in frame.itertuples()}
    need_map = {k: int(np.ceil(0.90 * len(v))) for k, v in e1.items()}
    fin_map = {k: (max(v) if v else -1) for k, v in e1.items()}
    ids = np.array(sorted(e1.keys()), dtype=np.int64)

    d = np.load(P5 / "record_lag.npz")
    m = (d["kind"] == 1) & np.isin(d["show"], ids) & (d["season"] == 1)
    u, sh, nu = d["user"][m], d["show"][m], d["number"][m]
    t, lg, un, ta = d["ts"][m], d["lag_days"][m], d["undated"][m], d["tau"][m]
    tsort = np.where(un, np.iinfo(np.int64).max, t)
    o = np.lexsort((tsort, sh, u))
    u, sh, nu, t, lg, un, ta = u[o], sh[o], nu[o], t[o], lg[o], un[o], ta[o]
    grp = np.flatnonzero(np.r_[True, (u[1:] != u[:-1]) | (sh[1:] != sh[:-1]), True])

    rows = []
    for i in range(len(grp) - 1):
        a, b = grp[i], grp[i + 1]
        sid = int(sh[a])
        E1 = e1[sid]
        inE = np.array([int(x) in E1 for x in nu[a:b]])
        if not inE.any():
            continue
        n1, t1, lg1, ta1 = nu[a:b][inE], t[a:b][inE], lg[a:b][inE], ta[a:b][inE]
        need, fin = need_map[sid], fin_map[sid]

        def walk(nums, dates):
            ordr = np.argsort(dates, kind="stable")
            seen = set()
            for j in ordr:
                seen.add(int(nums[j]))
                if len(seen) >= need and fin in seen:
                    return float(dates[j])
            return None

        c_all = walk(n1, t1.astype(float))
        if c_all is None:
            continue
        post = lg1 < POSTDATE_D
        comp_post = bool(post[np.argsort(t1.astype(float), kind="stable")][
            [k for k, jj in enumerate(np.argsort(t1.astype(float), kind="stable"))
             if float(t1[jj]) == c_all][0]]) if post.any() else False
        # simpler and exact: the completing record is the first, in date order,
        # at which the condition holds; recover its index
        ordr = np.argsort(t1.astype(float), kind="stable")
        seen = set(); comp_idx = -1
        for j in ordr:
            seen.add(int(n1[j]))
            if len(seen) >= need and fin in seen:
                comp_idx = int(j); break
        comp_post = bool(post[comp_idx])

        keep_b = ~post
        c_r1b = walk(n1[keep_b], t1[keep_b].astype(float)) if keep_b.any() else None
        keep_n = np.ones(len(n1), bool); keep_n[comp_idx] = not comp_post
        c_r1n = walk(n1[keep_n], t1[keep_n].astype(float)) if keep_n.any() else None
        dates_r3 = np.where(post, ta1, t1.astype(float))
        c_r3 = walk(n1, dates_r3)

        rows.append((int(u[a]), sid, comp_post, c_all,
                     c_r1b is not None, c_r1n is not None, c_r3 is not None,
                     c_r1b if c_r1b is not None else np.nan,
                     c_r3 if c_r3 is not None else np.nan,
                     int(post.sum())))

    r = pd.DataFrame(rows, columns=[
        "user_idx", "show_trakt_id", "comp_postdated", "comp_ts",
        "ok_r1b", "ok_r1n", "ok_r3", "comp_ts_r1b", "comp_ts_r3", "n_post"])
    base = pd.read_csv(P5 / "pair_t0.csv")
    r = r.merge(base[["user_idx", "show_trakt_id", "s2_ev_n", "t0_contaminated"]],
                on=["user_idx", "show_trakt_id"], validate="1:1")
    r["has_s2"] = r.s2_ev_n > 0
    a2 = (r.t0_contaminated == True) & (~r.has_s2)
    pdp = r.comp_postdated.values

    out = {"pairs_total": int(len(r)),
           "adoption2": int(a2.sum()),
           "postdated_completing": int(pdp.sum())}

    readings = {
        "P   pair-level delete": a2.values | pdp,
        "R1b record drop, broad": a2.values | (pdp & ~r.ok_r1b.values),
        "R1n record drop, narrow": a2.values | (pdp & ~r.ok_r1n.values),
        "R3  re-date to insert time": a2.values | (pdp & ~r.ok_r3.values),
    }
    tbl = {}
    for lab, rem in readings.items():
        tbl[lab] = {"removed": int(rem.sum()), "retained": int((~rem).sum()),
                    "retained_pct": round(100 * float((~rem).mean()), 2),
                    "postdated_pairs_rescued": int((pdp & ~rem).sum())}
    out["readings"] = tbl

    # collateral: a BROAD record rule also touches pairs adoption 3 never named
    other = (r.n_post.values > 0) & ~pdp
    out["broad_rule_collateral"] = {
        "pairs_with_postdated_noncompleting_records": int(other.sum()),
        "of_which_collapse_under_R1b": int((other & ~r.ok_r1b.values).sum()),
    }

    # how far T0's S1 term moves under R3
    mv = pdp & r.ok_r3.values
    sh_ = (r.comp_ts_r3.values[mv] - r.comp_ts.values[mv]) / DAY
    out["R3_completion_shift_days"] = {
        "pairs": int(mv.sum()),
        "median": round(float(np.median(sh_)), 1),
        "p10": round(float(np.percentile(sh_, 10)), 1),
        "p90": round(float(np.percentile(sh_, 90)), 1),
    }

    r.to_csv(P5 / "pair_postdate_readings.csv", index=False)
    (P5 / "postdate_readings.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
