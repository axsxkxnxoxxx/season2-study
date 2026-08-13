"""EVALUATION ONLY. Zero API calls. Adopts nothing, changes no rule.

Evaluates the proposed change to the Continued / Started-and-left boundary:
replace "evaluate the Continued condition at tau1 = [T0] + W*24h" with
"decide continued vs dropped by whether the account showed activity after the
pair's last S2 episode."

Nothing here is a Step 7 derivation. No gap percentile is computed. The delta
values used below are ROUND ILLUSTRATIVE CONSTANTS for a sensitivity band, not
candidate thresholds.

Populations
  - The Step 5 clean-record estimation sample (128,099 pairs), rebuilt by the
    identical mask used by src/step6_completion_lag.py and asserted against the
    published waterfall. This is the sample the disputed boundary is argued on.
  - For the censoring arithmetic only: all 220,107 in-frame pairs.

Clocks
  - Outcome states run on canonical watched_at (Step 1 sec 2.2, sec 7).
  - Liveness runs on INSERTION time (decisions/0021, 0029), read from the
    stored isotonic play-id curve at processed/step5/calibration.npz. Not
    refitted.

Output: processed/step7_eval/continued_boundary_eval.json  (counts only)
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
OUT = ROOT / "processed" / "step7_eval" / "continued_boundary_eval.json"

BACKFILL_D, POSTDATE_D = 180.0, -30.0
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
MISSING = np.iinfo(np.int64).min
W = 108            # decisions/0026
H = 91             # D10
DAY = 86400.0
TAU_PULL = pd.Timestamp("2026-08-11", tz="UTC").timestamp()
USER_STRIDE = 4_000_000_000   # > any epoch second, for the composite sort key
DELTAS = [0, 30, 60, 90, 180]  # illustrative only; see module docstring


def share(a, b):
    return None if b == 0 else round(100.0 * a / b, 2)


def main():
    # ---------------------------------------------------------------- sample
    p = pd.read_csv(P5 / "pair_revision5.csv")
    has_s2 = p.s2_ev_n.values > 0
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    keep = ~(all_air | (t0c & ~has_s2))
    fs2_bad = has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                        | (p.first_s2_airdate.values == 1)
                        | (p.first_s2_corrupt.values == 1))
    w = [keep]
    for m in (has_s2, ~t0c, ~postd, ~fs2_bad):
        w.append(w[-1] & m)
    waterfall = [int(x.sum()) for x in w]
    assert waterfall == PUBLISHED_WATERFALL, f"waterfall drift: {waterfall}"
    est = p.loc[w[-1], ["user_idx", "show_trakt_id", "t0", "s2_distinct"]].copy()
    est["t0_ts"] = ((pd.to_datetime(est.t0, utc=True)
                     - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds())

    # ---------------------------------------------------------------- frame
    f = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_E", "s2_L",
                                               "s2_F", "cadence_bucket", "air_period"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}
    need = {int(r.show_trakt_id): math.ceil(0.90 * int(r.s2_L)) for r in f.itertuples()}
    fin = {int(r.show_trakt_id): int(r.s2_F) for r in f.itertuples()}
    bucket = dict(zip(f.show_trakt_id.astype(int), f.cadence_bucket))
    period = dict(zip(f.show_trakt_id.astype(int), f.air_period))

    # ------------------------------------------- account-wide insertion times
    z = np.load(P5 / "full_scan.npz")
    user_all, rid_all = z["user"], z["rid"]
    cal = np.load(P5 / "calibration.npz")
    ins_all = np.interp(rid_all.astype(np.float64), cal["knot_rid"], cal["knot_time"])
    # per-user sorted insertion instants, as one composite-key array
    key_all = user_all.astype(np.int64) * USER_STRIDE + ins_all.astype(np.int64)
    key_all.sort()
    ins_sorted = key_all % USER_STRIDE
    usr_sorted = key_all // USER_STRIDE

    # ------------------------------------------------- S2 records, in-E2 only
    s2m = (z["season"] == 2) & (z["ts"] != MISSING)
    s2 = pd.DataFrame({"user_idx": user_all[s2m], "show_trakt_id": z["show"][s2m],
                       "number": z["number"][s2m], "ts": z["ts"][s2m],
                       "ins": ins_all[s2m]})
    del z, rid_all, ins_all, user_all
    s2 = s2[[n in e2.get(sh, ()) for sh, n in
             zip(s2.show_trakt_id.values, s2.number.values)]]

    # anchor: last insertion instant of any S2 evidence for the pair
    anchor = s2.groupby(["user_idx", "show_trakt_id"], as_index=False)["ins"].max() \
               .rename(columns={"ins": "anchor_ins"})
    # canonical (Step 1 sec 2.2) distinct-episode timestamps
    ep = s2.groupby(["user_idx", "show_trakt_id", "number"], as_index=False)["ts"].min()
    del s2

    d = est.merge(anchor, on=["user_idx", "show_trakt_id"], how="left")
    d["k"] = [need.get(int(s), 10**9) for s in d.show_trakt_id]
    d["f2"] = [fin.get(int(s), -1) for s in d.show_trakt_id]
    d["bucket"] = [bucket.get(int(s)) for s in d.show_trakt_id]
    d["period"] = [period.get(int(s)) for s in d.show_trakt_id]
    d["tau1"] = d.t0_ts + W * DAY
    d["tau1H"] = d.tau1 + H * DAY

    # ------------------------------------------ Continued condition at 3 bounds
    idx = {(u, s): i for i, (u, s) in
           enumerate(zip(d.user_idx.values, d.show_trakt_id.values))}
    n = len(d)
    row = np.array([idx.get((u, s), -1) for u, s in
                    zip(ep.user_idx.values, ep.show_trakt_id.values)])
    m = row >= 0
    row, ets, enum = row[m], ep.ts.values[m], ep.number.values[m]
    del ep

    bounds = {"tau1": d.tau1.values, "tau1H": d.tau1H.values,
              "pull": np.full(n, TAU_PULL)}
    state, n_epi = {}, {}
    for name, b in bounds.items():
        sel = ets < b[row]
        cnt = np.bincount(row[sel], minlength=n)
        f2hit = np.bincount(row[sel & (enum == d.f2.values[row])], minlength=n) > 0
        n_epi[name] = cnt
        state[name] = f2hit & (cnt >= d.k.values)
    d["nA_tau1"] = n_epi["tau1"]
    for name in bounds:
        d["cont_" + name] = state[name]

    # ------------------------------------------------- liveness after anchor
    ak = (d.user_idx.values.astype(np.int64) * USER_STRIDE
          + d.anchor_ins.values.astype(np.int64))
    pos = np.searchsorted(key_all, ak, side="right")
    same = (pos < len(key_all)) & (usr_sorted[np.clip(pos, 0, len(key_all) - 1)]
                                   == d.user_idx.values)
    nxt = np.where(same, ins_sorted[np.clip(pos, 0, len(key_all) - 1)], np.inf)
    d["gap_after_days"] = (nxt - d.anchor_ins.values) / DAY   # inf = nothing after
    d["days_to_last_activity"] = (
        pd.Series(ins_sorted).groupby(usr_sorted).max()
        .reindex(d.user_idx.values).values - d.anchor_ins.values) / DAY

    # ---------------------------------------------------------------- report
    def block(sub):
        st_tau1 = sub.nA_tau1.values > 0
        cont = sub.cont_tau1.values
        sal = st_tau1 & ~cont                       # started and left at tau1
        ever = sub.cont_pull.values
        byH = sub.cont_tau1H.values
        slow_H = sal & byH                          # completes inside D3's horizon
        slow_ever = sal & ever
        slow_beyond = slow_ever & ~byH
        out = {
            "pairs": int(len(sub)),
            "never_started_at_tau1": int((~st_tau1).sum()),
            "continued_at_tau1": int(cont.sum()),
            "started_and_left_at_tau1": int(sal.sum()),
            "of_started_and_left": {
                "n": int(sal.sum()),
                "completes_ever_before_pull_pct": share(slow_ever.sum(), sal.sum()),
                "completes_within_H91_of_tau1_pct": share(slow_H.sum(), sal.sum()),
                "completes_only_beyond_tau1_plus_H_pct": share(slow_beyond.sum(), sal.sum()),
            },
            "reclassified_if_continued_evaluated_at_tau1_plus_H": int(slow_H.sum()),
            "reclassified_if_continued_evaluated_ever": int(slow_ever.sum()),
        }
        # the proposal's classifier, on the group the Human Lead names as false
        for label, msk in (("all_started_pairs", st_tau1),
                           ("continued_at_tau1", cont),
                           ("started_and_left_at_tau1", sal),
                           ("started_and_left_but_completes_later", slow_ever)):
            g = sub.gap_after_days.values[msk]
            out.setdefault("quiet_after_last_S2_pct", {})[label] = {
                "n": int(msk.sum()),
                **{f"delta_{x}d": share((g > x).sum(), msk.sum()) for x in DELTAS},
                "no_activity_after_at_all": int(np.isinf(g).sum()),
            }
        return out

    res = {
        "what": "evaluation of the proposed Continued / Started-and-left boundary change",
        "api_calls": 0,
        "adopts": "nothing",
        "W": W, "H": H, "step5_waterfall_reproduced": waterfall,
        "distinct_count_exceeds_step5_s2_distinct": int(
            (d.nA_tau1.values > d.s2_distinct.values).sum()),
        "note_on_deltas": "illustrative sensitivity band, NOT Step 7 threshold candidates",
        "all_shows": block(d),
        "C1": block(d[d.bucket == "C1"]),
    }

    # exposure dependence of an unbounded Continued test, by air period
    per = {}
    for a, sub in d.groupby("period"):
        st = sub.nA_tau1.values > 0
        per[a] = {"started_pairs": int(st.sum()),
                  "continued_at_tau1_pct": share(sub.cont_tau1.sum(), st.sum()),
                  "continued_at_tau1_plus_H_pct": share(sub.cont_tau1H.sum(), st.sum()),
                  "continued_ever_pct": share(sub.cont_pull.sum(), st.sum()),
                  "median_years_T0_to_pull": round(
                      float(np.median(TAU_PULL - sub.t0_ts.values)) / 365.25 / DAY, 2)}
    res["exposure_dependence_by_air_period"] = per

    # degeneracy ceiling of the literal proposal
    # ---- discriminating power of the proposal's classifier, absolute volumes
    st = d.nA_tau1.values > 0
    cont, sal = d.cont_tau1.values, st & ~d.cont_tau1.values
    slow = sal & d.cont_pull.values
    g = d.gap_after_days.values
    disc = {}
    for x in DELTAS[1:]:
        q = g > x
        a, na = int((q & sal).sum()), int(sal.sum())
        b, nb = int((q & cont).sum()), int(cont.sum())
        pa, pb = a / na, b / nb
        pp = (a + b) / (na + nb)
        se = math.sqrt(pp * (1 - pp) * (1 / na + 1 / nb))
        disc[f"delta_{x}d"] = {
            "quiet_among_started_and_left": a,
            "quiet_among_continued_PLACEBO": b,
            "rate_started_and_left_pct": round(100 * pa, 2),
            "rate_continued_pct": round(100 * pb, 2),
            "relative_risk": round(pa / pb, 3) if pb else None,
            "z": round((pa - pb) / se, 2) if se else None,
            "pairs_the_proposal_moves": a,
            "quiet_among_the_named_false_cases": int((q & slow).sum()),
            "named_false_cases_left_where_they_are_pct":
                share(int((~q & slow).sum()), int(slow.sum())),
        }
    res["proposal_discriminating_power"] = disc

    # ---- is an unbounded Continued test exposure-driven? by exposure quartile
    exy = (TAU_PULL - d.t0_ts.values) / DAY / 365.25
    qs = np.quantile(exy, [0.25, 0.5, 0.75])
    lab = np.digitize(exy, qs)
    eq = {}
    for i in range(4):
        m2 = lab == i
        s2m_, sl = m2 & sal, m2 & slow
        eq[f"Q{i+1}"] = {
            "median_exposure_years": round(float(np.median(exy[m2])), 2),
            "started_and_left_at_tau1": int(s2m_.sum()),
            "of_which_complete_ever_pct": share(int(sl.sum()), int(s2m_.sum())),
            "of_which_complete_within_H91_pct":
                share(int((m2 & sal & d.cont_tau1H.values).sum()), int(s2m_.sum())),
        }
    res["exposure_quartiles_of_unbounded_vs_fixed_horizon"] = eq

    # ---- what excluding the quiet pairs does to the headline denominator
    nev = int((~st).sum())
    hl = {"never_started_at_tau1": nev, "denominator": int(len(d)),
          "never_started_pct": share(nev, len(d)),
          "anchor_undefined_for_never_started": True,
          "why": "a never-started pair has no S2 record, so 'activity after its "
                 "last S2 episode' has no anchor; the classifier cannot be "
                 "applied to the state the study is named after"}
    for x in DELTAS[1:]:
        drop = int(((g > x) & st).sum())
        hl[f"if_quiet_started_pairs_excluded_delta_{x}d"] = {
            "pairs_dropped": drop,
            "never_started_pct": share(nev, len(d) - drop)}
    res["headline_denominator_effect"] = hl

    # ---- do the two candidate fixes move the same pairs?
    fixH = sal & d.cont_tau1H.values
    prop30 = sal & (g > 30)
    res["overlap_of_candidate_fixes"] = {
        "moved_by_evaluating_Continued_at_tau1_plus_H": int(fixH.sum()),
        "moved_by_the_proposal_at_delta_30d": int(prop30.sum()),
        "moved_by_both": int((fixH & prop30).sum()),
        "moved_by_neither": int((sal & ~fixH & ~prop30).sum()),
    }

    res["degeneracy_ceiling"] = {
        "distinct_accounts_in_frame": int(p.user_idx.nunique()),
        "in_frame_pairs": int(len(p)),
        "why": ("at delta=0 the 'went quiet' set is exactly the pairs holding the "
                "account's last-ever inserted record, so it cannot exceed one pair "
                "per account"),
        "max_possible_pct_of_in_frame_pairs": share(p.user_idx.nunique(), len(p)),
    }

    # censoring cost of moving the Continued deadline out
    t0all = ((pd.to_datetime(p.t0, utc=True)
              - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds()).values
    shows = p.show_trakt_id.values
    cens = {}
    for label, horizon in (("current: max(W,91)+H = 199", max(W, 91) + H),
                           ("Continued at tau1+H, same 199", max(W, 91) + H),
                           ("second window W_c=167: max(167,91)+H = 258", 167 + H),
                           ("W_c=127 (all-shows p90): max(127,91)+H = 218", 127 + H)):
        ok = t0all + horizon * DAY <= TAU_PULL
        cens[label] = {"horizon_days": int(horizon),
                       "pairs_retained": int(ok.sum()),
                       "pairs_retained_pct": share(ok.sum(), len(p)),
                       "shows_lost": int(len(set(shows)) - len(set(shows[ok])))}
    res["right_censoring_cost"] = cens

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
