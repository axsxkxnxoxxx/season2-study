"""Step 5 revision 3: the ADOPTED rule, and the record-level reading of adoption 3.

READ ONLY. Zero network calls.

The Human Lead adopted a far narrower exclusion than Layer 2. Governing principle:

    Timestamp accuracy is not a concern for this study. The outcome is whether
    someone watched season 2, not when.

    Pairs are removed only where they cannot be evaluated against the
    never-started definition, not because their timestamps are untidy.

This file computes:

  1. The adopted exclusion under BOTH readings of adoption 3.

     PAIR-LEVEL reading   - a pair whose S1 completion record is post-dated is
                            deleted outright.
     RECORD-LEVEL reading - the post-dated RECORD is set aside, S1 completion is
                            recomputed without it, and the pair survives with a
                            recomputed T0 unless it can no longer satisfy the
                            Step 1 Sec 4 rule at all.

     The Human Lead wrote "future-dated records", not pairs. The two readings
     disagree on 3,016 pairs that have S2 evidence and are therefore protected by
     adoption 1. The conflict is REPORTED, not resolved.

  2. The C5 mechanism: how often an S1 record was inserted AFTER the observed
     completion instant, which is the direct evidence that first-pass completion
     dates can be too early.

  3. The W estimation sample under Ruling 1, recomputed on the adopted
     analysis population. Estimation sample and analysis population are
     different populations and are kept visibly distinct.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"

BACKFILL_D = 180.0
POSTDATE_D = -30.0
DAY = 86400.0


def parse_set(s):
    return {int(x) for x in str(s).split(",") if x.strip().isdigit()}


def main():
    frame = pd.read_csv(ROOT / "processed" / "step2" / "frame.csv")
    e1 = {int(r.show_trakt_id): parse_set(r.s1_E) for r in frame.itertuples()}
    thr_map = {k: int(np.ceil(0.90 * len(v))) for k, v in e1.items()}
    fin_map = {k: (max(v) if v else -1) for k, v in e1.items()}
    fin_air = {int(r.show_trakt_id): r.s2_finale_date for r in frame.itertuples()}
    frame_ids = np.array(sorted(e1.keys()), dtype=np.int64)

    d = np.load(P5 / "record_lag.npz")
    user, ts, kind = d["user"], d["ts"], d["kind"]
    show, season, number = d["show"], d["season"], d["number"]
    lag, corrupt, undated, tau = d["lag_days"], d["corrupt"], d["undated"], d["tau"]

    m = (kind == 1) & np.isin(show, frame_ids) & (season == 1)
    u, sh, nu = user[m], show[m], number[m]
    t, lg, co, un, ta = ts[m], lag[m], corrupt[m], undated[m], tau[m]
    tsort = np.where(un, np.iinfo(np.int64).max, t)
    order = np.lexsort((tsort, sh, u))
    u, sh, nu, t, lg, co, un, ta = (u[order], sh[order], nu[order], t[order],
                                    lg[order], co[order], un[order], ta[order])
    grp = np.flatnonzero(np.r_[True, (u[1:] != u[:-1]) | (sh[1:] != sh[:-1]), True])

    rows = []
    for i in range(len(grp) - 1):
        a, b = grp[i], grp[i + 1]
        sid = int(sh[a])
        E1 = e1[sid]
        inE = np.array([int(x) in E1 for x in nu[a:b]])
        if not inE.any():
            continue
        n1 = nu[a:b][inE]; t1 = t[a:b][inE]; lg1 = lg[a:b][inE]; ta1 = ta[a:b][inE]
        need = thr_map[sid]; fin = fin_map[sid]

        def walk(mask):
            seen = set()
            for j in range(len(n1)):
                if not mask[j]:
                    continue
                seen.add(int(n1[j]))
                if len(seen) >= need and fin in seen:
                    return j
            return -1

        full = np.ones(len(n1), dtype=bool)
        k_all = walk(full)
        if k_all < 0:
            continue  # not an S1 completer under the adopted definition

        post = lg1 < POSTDATE_D
        comp_postdated = bool(post[k_all])
        # record-level reading: set aside every post-dated S1 record, recompute
        k_rec = walk(~post) if post.any() else k_all

        # C5 mechanism: was any S1 record in the completion prefix inserted AFTER
        # the observed completion instant?
        pref_tau = ta1[: k_all + 1]
        comp_instant = float(t1[k_all])
        later = pref_tau > comp_instant
        shift = float(pref_tau.max() - comp_instant) / DAY if later.any() else 0.0

        rows.append((
            int(u[a]), sid, int(k_all), comp_postdated,
            int(t1[k_all]), int(k_rec),
            int(t1[k_rec]) if k_rec >= 0 else 0,
            bool(later.any()), shift, int(post.sum()),
        ))

    cols = ["user_idx", "show_trakt_id", "k_all", "comp_postdated", "comp_ts",
            "k_rec", "comp_ts_rec", "any_s1_inserted_after_completion",
            "max_shift_days", "n_postdated_s1_records"]
    r = pd.DataFrame(rows, columns=cols)
    print(f"S1-completer pairs (post-dated retained): {len(r):,}")

    base = pd.read_csv(P5 / "pair_t0.csv")
    r = r.merge(base[["user_idx", "show_trakt_id", "s2_ev_n", "t0_contaminated",
                      "binds", "s2_finale_date", "first_s2_lag_days",
                      "first_s2_corrupt", "first_s2_airdate",
                      "s1_ev_backfilled", "s1_ev_corrupt", "s1_ev_airdate",
                      "comp_corrupt", "comp_airdate", "comp_backfill"]],
                on=["user_idx", "show_trakt_id"], how="left", validate="1:1")
    r["has_s2"] = r.s2_ev_n > 0

    out = {"pairs_total": int(len(r))}

    # ---- adoption 2: contaminated T0, no S2 evidence -------------------------
    a2 = (r.t0_contaminated == True) & (~r.has_s2)
    out["adoption2_contaminated_no_s2"] = int(a2.sum())
    out["adoption1_kept_contaminated_with_s2"] = int(((r.t0_contaminated == True) & r.has_s2).sum())

    # ---- adoption 3, two readings -------------------------------------------
    pd_pair = r.comp_postdated.values
    out["postdated_completing_record"] = int(pd_pair.sum())
    out["postdated_with_s2"] = int((pd_pair & r.has_s2.values).sum())
    out["postdated_overlap_with_adoption2"] = int((pd_pair & a2.values).sum())

    # record-level: does the pair still complete once post-dated records are set aside?
    collapses = pd_pair & (r.k_rec.values < 0)
    survives = pd_pair & (r.k_rec.values >= 0)
    out["record_level"] = {
        "postdated_pairs": int(pd_pair.sum()),
        "still_complete_with_recomputed_T0": int(survives.sum()),
        "collapse_cannot_complete": int(collapses.sum()),
        "of_the_3016_with_s2_still_complete": int((survives & r.has_s2.values).sum()),
        "of_the_3016_with_s2_collapse": int((collapses & r.has_s2.values).sum()),
    }
    # how far does T0 move for the survivors?
    mv = survives & (r.comp_ts_rec.values != r.comp_ts.values)
    shift_days = (r.comp_ts_rec.values[mv] - r.comp_ts.values[mv]) / DAY
    out["record_level"]["completion_date_moved"] = int(mv.sum())
    if mv.sum():
        out["record_level"]["completion_shift_days"] = {
            "median": round(float(np.median(shift_days)), 1),
            "p90": round(float(np.percentile(shift_days, 90)), 1),
            "min": round(float(shift_days.min()), 1),
            "max": round(float(shift_days.max()), 1),
        }
    # does the recomputed T0 change the binding term?
    fin_dt = pd.to_datetime(r.s2_finale_date)
    new_s1 = pd.to_datetime(r.comp_ts_rec, unit="s", utc=True).dt.normalize().dt.tz_localize(None)
    old_s1 = pd.to_datetime(r.comp_ts, unit="s", utc=True).dt.normalize().dt.tz_localize(None)
    t0_old = np.maximum(old_s1.values, fin_dt.values)
    t0_new = np.maximum(new_s1.values, fin_dt.values)
    out["record_level"]["T0_unchanged_because_finale_binds"] = int(
        (survives & (t0_old == t0_new)).sum())

    # ---- final retained counts ----------------------------------------------
    removed_pairlevel = a2.values | pd_pair
    removed_recordlevel = a2.values | collapses
    out["FINAL"] = {
        "pair_level_reading": {
            "removed": int(removed_pairlevel.sum()),
            "retained": int((~removed_pairlevel).sum()),
            "retained_pct": round(100 * float((~removed_pairlevel).mean()), 2),
        },
        "record_level_reading": {
            "removed": int(removed_recordlevel.sum()),
            "retained": int((~removed_recordlevel).sum()),
            "retained_pct": round(100 * float((~removed_recordlevel).mean()), 2),
        },
    }

    # ---- C5 mechanism --------------------------------------------------------
    e_bf = (r.s1_ev_backfilled.values - r.comp_backfill.values.astype(int)) > 0
    e_co = (r.s1_ev_corrupt.values - r.comp_corrupt.values.astype(int)) > 0
    e_a3 = (r.s1_ev_airdate.values - r.comp_airdate.values.astype(int)) > 0
    comp_bad = (r.comp_backfill.values | r.comp_corrupt.values | r.comp_airdate.values)
    c5_two = (e_bf | e_co) & ~comp_bad
    c5_three = (e_bf | e_co | e_a3) & ~comp_bad
    lat = r.any_s1_inserted_after_completion.values
    sh_ = r.max_shift_days.values
    c5 = {}
    for lab, mask in (("two_class_backfill_corrupt", c5_two), ("three_class_incl_airdate", c5_three)):
        sel = mask & lat
        c5[lab] = {
            "pairs": int(mask.sum()),
            "with_s2_evidence": int((mask & r.has_s2.values).sum()),
            "with_s2_pct": round(100 * float(r.has_s2.values[mask].mean()), 1),
            "s1_record_inserted_after_completion": int(sel.sum()),
            "pct": round(100 * float(sel.sum() / max(1, mask.sum())), 1),
            "shift_days_median": round(float(np.median(sh_[sel])), 1) if sel.sum() else None,
            "shift_days_max": round(float(sh_[sel].max()), 1) if sel.sum() else None,
        }
    out["C5"] = c5

    # ---- W estimation sample under Ruling 1 ---------------------------------
    clean_t0 = (~r.t0_contaminated.values.astype(bool)) & (~pd_pair)
    fs2_bad = ((r.first_s2_lag_days.values > BACKFILL_D)
               | (r.first_s2_airdate.values == 1) | (r.first_s2_corrupt.values == 1))
    for lab, removed in (("pair_level", removed_pairlevel), ("record_level", removed_recordlevel)):
        keep = ~removed
        est = keep & r.has_s2.values & clean_t0 & (~fs2_bad)
        out.setdefault("W_estimation_sample", {})[lab] = {
            "analysis_population": int(keep.sum()),
            "of_which_have_s2_evidence": int((keep & r.has_s2.values).sum()),
            "W_estimation_sample": int(est.sum()),
            "pct_of_analysis_population": round(100 * float(est.sum() / keep.sum()), 2),
        }

    r.to_csv(P5 / "pair_adopted.csv", index=False)
    (P5 / "adopted_rule.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
