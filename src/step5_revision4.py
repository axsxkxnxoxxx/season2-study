"""Step 5 revision 4: every figure in the artifact, derivable from this file.

READ ONLY. Zero network calls.

Red Team B3 was "the artifact rests on code not in the repository". It recurred as
D3 inside the section written to answer B3. This file exists so it cannot recur:
every number quoted in revision 4 of the artifact is computed here and written to
processed/step5/revision4.json.

WHAT CHANGED IN THE RULING

D1 ruled: approved Step 1 Sec 7 stands. Never started is |A| = 0 under
watched_at < tau1. The revision-3 governing principle - "the outcome is whether
someone watched season 2, not when" - described an ever-started study and is
WITHDRAWN.

Consequences computed here:
  adoption 1  narrowed: exclude pairs whose S2 evidence is ENTIRELY air-date
              stamped, because that stamp is <= S2 finale <= T0 < tau1 by
              construction and so classifies the pair by itself
  adoption 2  re-ruled: the 1,542 go for a CENSORING defect (Step 1 D10), not an
              evaluability defect. A pair with zero S2 records has |A| = 0 for
              every tau1 and is perfectly evaluable; what a fabricated-early T0
              breaks is the right-censoring test
  adoption 3  reconsidered, not assumed

THE INSERT-TIME BOUND (Red Team's endorsed test, and the basis for D2)

A viewer cannot log an episode before watching it, so a record's insert instant
is an UPPER bound on when that episode was truly watched. The latest defensible
S1 completion instant for a pair is therefore the maximum insert instant over the
records that establish completion, and the latest defensible clock start is

    T0_latest = max(S2_finale_air_date, date(max tau_ins over completion evidence))

If even that latest clock leaves too little elapsed time before tau_pull, the pair
should have failed right-censoring and its retention is an artifact of the
fabricated-early date.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"

DAY = 86400.0
TAU_PULL = int(dt.datetime(2026, 8, 11, tzinfo=dt.timezone.utc).timestamp())
BACKFILL_D = 180.0
POSTDATE_D = -30.0
W_PROBE = 60  # illustrative W for the open-window share; W is not set until Step 6


def parse_set(s):
    return {int(x) for x in str(s).split(",") if x.strip().isdigit()}


def main():
    out = {}
    frame = pd.read_csv(ROOT / "processed" / "step2" / "frame.csv")
    e1 = {int(r.show_trakt_id): parse_set(r.s1_E) for r in frame.itertuples()}
    need = {k: int(np.ceil(0.90 * len(v))) for k, v in e1.items()}
    finale_ep = {k: max(v) for k, v in e1.items()}
    fin_air = {int(r.show_trakt_id): r.s2_finale_date for r in frame.itertuples()}
    ids = np.array(sorted(e1), dtype=np.int64)

    d = np.load(P5 / "record_lag.npz")
    m = (d["kind"] == 1) & np.isin(d["show"], ids) & (d["season"] == 1)
    u, sh, nu = d["user"][m], d["show"][m], d["number"][m]
    t, un, ta = d["ts"][m], d["undated"][m], d["tau"][m]
    tsort = np.where(un, np.iinfo(np.int64).max, t)
    o = np.lexsort((tsort, sh, u))
    u, sh, nu, t, ta = u[o], sh[o], nu[o], t[o], ta[o]
    g = np.flatnonzero(np.r_[True, (u[1:] != u[:-1]) | (sh[1:] != sh[:-1]), True])

    rows = []
    for i in range(len(g) - 1):
        a, b = g[i], g[i + 1]
        sid = int(sh[a])
        E = e1[sid]
        inE = np.array([int(x) in E for x in nu[a:b]])
        if not inE.any():
            continue
        n1, t1, ta1 = nu[a:b][inE], t[a:b][inE], ta[a:b][inE]
        seen, k = set(), -1
        for j in range(len(n1)):
            seen.add(int(n1[j]))
            if len(seen) >= need[sid] and finale_ep[sid] in seen:
                k = j
                break
        if k < 0:
            continue
        rows.append((int(u[a]), sid, float(ta1[: k + 1].max())))
    bound = pd.DataFrame(rows, columns=["user_idx", "show_trakt_id", "latest_completion_tau"])

    p = pd.read_csv(P5 / "pair_t0.csv").merge(
        bound, on=["user_idx", "show_trakt_id"], validate="1:1")
    p["has_s2"] = p.s2_ev_n > 0

    # latest-defensible clock start, both terms as UTC calendar dates
    lat_s1 = pd.to_datetime(p.latest_completion_tau, unit="s", utc=True).dt.normalize().dt.tz_localize(None)
    fin_dt = pd.to_datetime(p.s2_finale_date)
    t0_latest = np.maximum(lat_s1.values, fin_dt.values)
    tau_pull_dt = np.datetime64("2026-08-11")
    p["elapsed_days_latest"] = (tau_pull_dt - t0_latest) / np.timedelta64(1, "D")

    # ---- the populations -----------------------------------------------------
    t0c = p.t0_contaminated.values.astype(bool)
    s2 = p.has_s2.values
    the1542 = t0c & ~s2
    postd = (p.complete_rec_lag_days < POSTDATE_D).values

    all_air = s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    any_air = s2 & (p.s2_ev_airdate.values > 0)
    part_air = any_air & ~all_air

    cb = p.comp_contaminated.values.astype(bool)
    e_bf = (p.s1_ev_backfilled.values - p.comp_backfill.values.astype(int)) > 0
    e_co = (p.s1_ev_corrupt.values - p.comp_corrupt.values.astype(int)) > 0
    e_a3 = (p.s1_ev_airdate.values - p.comp_airdate.values.astype(int)) > 0
    c5_two = (e_bf | e_co) & ~cb
    c5_three = (e_bf | e_co | e_a3) & ~cb
    the720 = c5_three & ~s2
    the425 = c5_two & ~s2

    out["populations"] = {
        "pairs_total": int(len(p)),
        "the_1542_contaminated_T0_no_s2": int(the1542.sum()),
        "all_airdate_s2": int(all_air.sum()),
        "any_airdate_s2": int(any_air.sum()),
        "partly_airdate_s2": int(part_air.sum()),
        "postdated_completing": int(postd.sum()),
        "c5_three_class": int(c5_three.sum()),
        "c5_two_class": int(c5_two.sum()),
        "c5_no_s2_three_class_the_720": int(the720.sum()),
        "c5_no_s2_two_class_the_425": int(the425.sum()),
        "c5_no_s2_gap_295": int(the720.sum() - the425.sum()),
    }

    # ---- insert-time bound, the D2 evidence ---------------------------------
    def bnd(mask, label):
        e = p.elapsed_days_latest.values[mask]
        return {
            "label": label,
            "pairs": int(mask.sum()),
            "median_elapsed_days": round(float(np.median(e)), 1),
            "p25": round(float(np.percentile(e, 25)), 1),
            "p75": round(float(np.percentile(e, 75)), 1),
            f"share_window_still_open_at_W{W_PROBE}": round(float(np.mean(e < W_PROBE)), 4),
            "share_negative_elapsed": round(float(np.mean(e < 0)), 4),
        }

    out["insert_time_bound"] = {
        "definition": "elapsed = tau_pull - max(S2 finale date, date(max tau_ins over S1 completion evidence))",
        "the_1542": bnd(the1542, "contaminated T0, no S2 evidence"),
        "the_720": bnd(the720, "C5 three-class, no S2 evidence"),
        "the_425": bnd(the425, "C5 two-class, no S2 evidence"),
        "the_295": bnd(the720 & ~the425, "C5 air-date-only class, no S2 evidence"),
        "all_no_s2_pairs": bnd(~s2, "every pair with no S2 evidence"),
    }

    # ---- adopted rule arithmetic --------------------------------------------
    ad1 = all_air                     # adoption 1, narrowed to option (b)
    ad2 = the1542                     # adoption 2
    ad3 = postd                       # adoption 3, if taken at pair level
    out["overlaps"] = {
        "ad1_and_ad2": int((ad1 & ad2).sum()),
        "ad3_and_ad2": int((ad3 & ad2).sum()),
        "ad3_and_ad1": int((ad3 & ad1).sum()),
    }
    without3 = ad1 | ad2
    with3 = ad1 | ad2 | ad3
    out["adopted_rule"] = {
        "without_adoption3": {
            "removed": int(without3.sum()),
            "retained": int((~without3).sum()),
            "retained_pct": round(100 * float((~without3).mean()), 2),
        },
        "with_adoption3_pair_level": {
            "removed": int(with3.sum()),
            "retained": int((~with3).sum()),
            "retained_pct": round(100 * float((~with3).mean()), 2),
            "marginal_cost_of_adoption3": int(with3.sum() - without3.sum()),
        },
    }

    # adoption 3 under the record-level readings
    pr = pd.read_csv(P5 / "pair_postdate_readings.csv")
    p2 = p.merge(pr[["user_idx", "show_trakt_id", "ok_r1b", "ok_r1n", "ok_r3"]],
                 on=["user_idx", "show_trakt_id"], validate="1:1")
    for lab, col in (("R1b", "ok_r1b"), ("R1n", "ok_r1n"), ("R3", "ok_r3")):
        rem = ad1 | ad2 | (postd & ~p2[col].values)
        out["adopted_rule"][f"with_adoption3_{lab}"] = {
            "removed": int(rem.sum()), "retained": int((~rem).sum()),
            "retained_pct": round(100 * float((~rem).mean()), 2),
        }

    # ---- E2: rejected candidates recosted on the ADOPTED population ---------
    keep0 = ~without3
    all_bf = s2 & (p.s2_ev_backfilled.values == p.s2_ev_n.values)
    out["rejected_recost_on_adopted_population"] = {
        "P2_all_airdate_s2_NOW_ADOPTED": int(all_air.sum()),
        "P3_all_backfilled_s2_full_scope": int(all_bf.sum()),
        "P3_share_of_population": round(100 * float(all_bf.mean()), 1),
        "P3_marginal_beyond_adopted_rule": int((all_bf & keep0).sum()),
        "layer2_full_scope": int(t0c.sum()),
        "layer2_marginal_beyond_adopted_rule": int((t0c & keep0).sum()),
    }

    # ---- E1: retention bias vs exclusion bias -------------------------------
    fs2_bad = ((p.first_s2_lag_days.values > BACKFILL_D)
               | (p.first_s2_airdate.values == 1) | (p.first_s2_corrupt.values == 1))
    out["bias"] = {
        "exclusion_pairs_all_never_started": int(ad2.sum()),
        "retention_first_s2_contaminated_total": int((fs2_bad & s2).sum()),
        "retention_first_s2_contaminated_retained": int((fs2_bad & s2 & keep0).sum()),
        "ratio_retention_to_exclusion": round(
            float((fs2_bad & s2 & keep0).sum() / max(1, ad2.sum())), 1),
        "denominator_pairs_with_s2_evidence": int(s2.sum()),
        "E6_share_of_pairs_with_s2": round(100 * float((fs2_bad & s2).sum() / s2.sum()), 1),
    }

    # ---- E3: W estimation sample under every reading, R3 handled properly ---
    clean_t0_base = (~t0c) & (~postd)
    est_base = clean_t0_base & s2 & (~fs2_bad)
    ws = {}
    for lab, rem, restore in (
        ("no_adoption3", without3, np.zeros(len(p), bool)),
        ("P_pair_delete", with3, np.zeros(len(p), bool)),
        ("R1b", ad1 | ad2 | (postd & ~p2.ok_r1b.values), np.zeros(len(p), bool)),
        ("R1n", ad1 | ad2 | (postd & ~p2.ok_r1n.values), np.zeros(len(p), bool)),
        # R3 re-dates the post-dated record, so it is no longer post-dated and
        # the pair becomes ELIGIBLE for the estimation sample. E3.
        ("R3", ad1 | ad2 | (postd & ~p2.ok_r3.values), postd & (~t0c)),
    ):
        keep = ~rem
        est = keep & (est_base | (restore & s2 & (~fs2_bad)))
        ws[lab] = {"analysis_population": int(keep.sum()),
                   "W_estimation_sample": int(est.sum())}
    out["W_estimation_sample"] = ws

    p.to_csv(P5 / "pair_revision4.csv", index=False)
    (P5 / "revision4.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
