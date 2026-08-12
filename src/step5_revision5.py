"""Step 5 revision 5: every figure quoted in the artifact, from committed code.

READ ONLY. Zero network calls.

WHY THIS FILE EXISTS

Red Team B3 was "the artifact rests on code not in the repository". It recurred as
D3, and revision 4 answered D3 with a §16 sentence certifying that every figure
was written by committed code - which was itself false for nine figures, including
the two C5 rows D3 had been raised about. F3 is that defect's third occurrence.

So this file computes EVERY number the artifact quotes, including the ones that
were previously produced in throwaway shells, and writes them to
processed/step5/revision5.json. The certification in the artifact points here and
is checkable by grep.

NEW WORK IN THIS REVISION

F1  The retention bias was quoted as a 30:1 ratio computed as 46,642 / 1,542,
    which ignores the 16,665 - a population change running the other way and
    itself 10.8x the 1,542. Two incommensurable things had been put in one
    column. Here they are separated:
      - population change: exact counts, net direction
      - estimator bias:    a BOUND on how many pairs could flip, not a count
    The bound uses the instrument this step already built. A contaminated
    record's true watch time is <= its insert instant. So a pair whose first S2
    watch has tau_ins < tau1 was inside the window whatever its claimed date
    says, and CANNOT flip. Only tau_ins >= tau1 pairs can. Tabulated at candidate
    W exactly as the censoring bound is tabulated.

F2  The 2,352 closure. For a pair whose FIRST S2 watch is clean, that record's
    canonical timestamp c satisfies c <= s <= S2 finale <= T0 < tau1 for any
    stamped record s, so the clean record lands in A at every W and the stamp is
    redundant. Those pairs are provably rescued with no W. The open set is the
    4,988 whose first S2 watch is itself the stamped record.

RECONCILIATION
The 720's censoring-bound figure is published in two places as 2,150 d / 8.1%.
Six bases are computed here. max(finale, .) is monotone, so including it can only
push T0_latest later and elapsed SMALLER; 2,150 > 1,738 is therefore impossible
with the max() included on the same set, and the table shows exactly which two
departures produce it.
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
TAU_PULL = np.datetime64("2026-08-11")
BACKFILL_D = 180.0
POSTDATE_D = -30.0
W_GRID = (30, 60, 91, 120, 180)


def parse_set(s):
    return {int(x) for x in str(s).split(",") if x.strip().isdigit()}


def main():
    out = {}
    frame = pd.read_csv(ROOT / "processed" / "step2" / "frame.csv")
    e1 = {int(r.show_trakt_id): parse_set(r.s1_E) for r in frame.itertuples()}
    e2 = {int(r.show_trakt_id): parse_set(r.s2_E) for r in frame.itertuples()}
    need = {k: int(np.ceil(0.90 * len(v))) for k, v in e1.items()}
    fin_ep = {k: max(v) for k, v in e1.items()}
    ids = np.array(sorted(e1), dtype=np.int64)

    d = np.load(P5 / "record_lag.npz")
    m3 = np.zeros(len(d["user"]), dtype=bool)
    m3[np.load(P5 / "mode3_flags.npz")["record_index"]] = True

    # ---------- S1 pass: completion instant and insert-time bounds -----------
    m = (d["kind"] == 1) & np.isin(d["show"], ids) & (d["season"] == 1)
    u, sh, nu = d["user"][m], d["show"][m], d["number"][m]
    t, un, ta = d["ts"][m], d["undated"][m], d["tau"][m]
    o = np.lexsort((np.where(un, np.iinfo(np.int64).max, t), sh, u))
    u, sh, nu, t, ta = u[o], sh[o], nu[o], t[o], ta[o]
    g = np.flatnonzero(np.r_[True, (u[1:] != u[:-1]) | (sh[1:] != sh[:-1]), True])

    s1rows = []
    for i in range(len(g) - 1):
        a, b = g[i], g[i + 1]
        sid = int(sh[a])
        inE = np.array([int(x) in e1[sid] for x in nu[a:b]])
        if not inE.any():
            continue
        n1, t1, ta1 = nu[a:b][inE], t[a:b][inE], ta[a:b][inE]
        seen, k = set(), -1
        for j in range(len(n1)):
            seen.add(int(n1[j]))
            if len(seen) >= need[sid] and fin_ep[sid] in seen:
                k = j
                break
        if k < 0:
            continue
        s1rows.append((int(u[a]), sid, float(t1[k]),
                       float(ta1[: k + 1].max()), float(ta1.max())))
    s1 = pd.DataFrame(s1rows, columns=["user_idx", "show_trakt_id", "comp_ts",
                                       "tau_prefix", "tau_allE1"])

    # ---------- S2 pass: the FIRST S2 watch, its insert instant and class ----
    m = (d["kind"] == 1) & np.isin(d["show"], ids) & (d["season"] == 2)
    u, sh, nu = d["user"][m], d["show"][m], d["number"][m]
    t, un, ta = d["ts"][m], d["undated"][m], d["tau"][m]
    lg, co, a3 = d["lag_days"][m], d["corrupt"][m], m3[m]
    o = np.lexsort((np.where(un, np.iinfo(np.int64).max, t), sh, u))
    u, sh, nu, t, ta, lg, co, a3 = (u[o], sh[o], nu[o], t[o], ta[o], lg[o], co[o], a3[o])
    g = np.flatnonzero(np.r_[True, (u[1:] != u[:-1]) | (sh[1:] != sh[:-1]), True])

    s2rows = []
    for i in range(len(g) - 1):
        a, b = g[i], g[i + 1]
        sid = int(sh[a])
        inE = np.array([int(x) in e2[sid] for x in nu[a:b]])
        if not inE.any():
            continue
        k = int(np.flatnonzero(inE)[0])
        # earliest CLEAN S2 record in E2, for the F2 closure
        clean = inE & (~co[a:b]) & (lg[a:b] <= BACKFILL_D) & (~a3[a:b])
        s2rows.append((int(u[a]), sid, float(t[a:b][k]), float(ta[a:b][k]),
                       bool(a3[a:b][k]), bool(co[a:b][k]), float(lg[a:b][k]),
                       int(clean.sum()),
                       float(t[a:b][np.flatnonzero(clean)[0]]) if clean.any() else np.nan))
    s2 = pd.DataFrame(s2rows, columns=[
        "user_idx", "show_trakt_id", "first_s2_ts_r5", "first_s2_tau",
        "first_s2_is_airdate", "first_s2_is_corrupt", "first_s2_lag_r5",
        "n_clean_s2", "first_clean_s2_ts"])

    p = pd.read_csv(P5 / "pair_t0.csv").merge(s1, on=["user_idx", "show_trakt_id"], validate="1:1")
    p = p.merge(s2, on=["user_idx", "show_trakt_id"], how="left", validate="1:1")

    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    any_air = has_s2 & (p.s2_ev_airdate.values > 0)
    part_air = any_air & ~all_air
    the1542 = t0c & ~has_s2
    removed = all_air | the1542
    keep = ~removed

    # ---------- F2: the 2,352 closure ---------------------------------------
    first_is_stamp = part_air & p.first_s2_is_airdate.fillna(False).values.astype(bool)
    first_is_clean = part_air & ~first_is_stamp
    out["F2_partly_airdate"] = {
        "any_airdate_s2": int(any_air.sum()),
        "all_airdate_excluded": int(all_air.sum()),
        "partly_airdate_retained": int(part_air.sum()),
        "closed_first_s2_watch_is_clean": int(first_is_clean.sum()),
        "open_first_s2_watch_is_the_stamp": int(first_is_stamp.sum()),
        "open_pct_of_frame": round(100 * float(first_is_stamp.sum() / len(p)), 2),
        "closure_argument": ("first clean record c <= first stamped record s <= S2 finale "
                             "<= T0 < tau1, so c lands in A at every W"),
    }

    # ---------- F1: population change vs estimator bias ---------------------
    fs2_bad = (has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                         | (p.first_s2_airdate.values == 1)
                         | (p.first_s2_corrupt.values == 1)))
    pop = {
        "removed_1542_direction": "down (all were Never started)",
        "removed_1542": int(the1542.sum()),
        "removed_16665_direction": "up (all were guaranteed Started)",
        "removed_16665": int(all_air.sum()),
        "net_population_change": int(all_air.sum() - the1542.sum()),
        "net_direction": "up",
        "ratio_16665_to_1542": round(float(all_air.sum() / the1542.sum()), 1),
        "naive_ratio_46642_over_1542_WITHDRAWN": round(float((fs2_bad & keep).sum() / the1542.sum()), 1),
        "ratio_against_net_exclusion": round(
            float((fs2_bad & keep).sum() / (all_air.sum() - the1542.sum())), 1),
    }
    out["F1_population_change"] = pop

    # flip bound: only pairs whose first S2 watch has tau_ins >= tau1 can flip
    t0_dt = pd.to_datetime(p.t0).values
    flip = {}
    cand = keep & fs2_bad
    tau_first = pd.to_datetime(p.first_s2_tau, unit="s", utc=True).dt.tz_localize(None).values
    for W in W_GRID:
        tau1 = t0_dt + np.timedelta64(W, "D")
        can = cand & (tau_first >= tau1)
        flip[f"W={W}"] = {
            "candidates_contaminated_first_s2_retained": int(cand.sum()),
            "upper_bound_on_flips": int(can.sum()),
            "pct_of_retained_pairs": round(100 * float(can.sum() / keep.sum()), 2),
            "ruled_out_by_insert_time": int(cand.sum() - can.sum()),
        }
    out["F1_flip_upper_bound"] = flip
    out["F1_statement"] = {
        "population_change": "exact, net UP",
        "estimator_bias": ("contaminated-early first-S2 dates can only pull records INTO the "
                           "window, so the reported never-started share is a FLOOR; direction "
                           "down; magnitude BOUNDED above, not counted"),
    }

    # ---------- F3: the previously uncommitted figures -----------------------
    # section 8 breakdowns, both denominators
    def brk(mask, label):
        n = int(mask.sum())
        return {"label": label, "denominator": n,
                "backfilled": int((mask & (p.first_s2_lag_days.values > BACKFILL_D)).sum()),
                "airdate": int((mask & (p.first_s2_airdate.values == 1)).sum()),
                "corrupt": int((mask & (p.first_s2_corrupt.values == 1)).sum()),
                "any_class": int((mask & fs2_bad).sum()),
                "any_class_pct": round(100 * float((mask & fs2_bad).sum() / n), 1)}
    out["F3_section8"] = {"full_frame": brk(has_s2, "all pairs with S2 evidence"),
                          "retained": brk(has_s2 & keep, "retained pairs with S2 evidence")}

    # C5 mechanism, all four rows
    cb = p.comp_contaminated.values.astype(bool)
    e_bf = (p.s1_ev_backfilled.values - p.comp_backfill.values.astype(int)) > 0
    e_co = (p.s1_ev_corrupt.values - p.comp_corrupt.values.astype(int)) > 0
    e_a3 = (p.s1_ev_airdate.values - p.comp_airdate.values.astype(int)) > 0
    bases = {"two_class": (e_bf | e_co) & ~cb, "three_class": (e_bf | e_co | e_a3) & ~cb}
    c5 = {}
    for bl, bm in bases.items():
        for vl, col in (("completion_prefix", "tau_prefix"), ("any_s1_record", "tau_allE1")):
            shift = (p[col].values - p.comp_ts.values) / DAY
            sel = bm & (shift > 0)
            c5[f"{bl}__{vl}"] = {
                "pairs_in_basis": int(bm.sum()),
                "inserted_after_completion": int(sel.sum()),
                "pct": round(100 * float(sel.sum() / bm.sum()), 1),
                "median_shift_days": round(float(np.median(shift[sel])), 1),
                "max_shift_days": round(float(shift[sel].max()), 1),
            }
    out["F3_C5_mechanism"] = c5

    # ---------- reconciliation: the 720 bound, six bases ---------------------
    the720 = bases["three_class"] & ~has_s2
    fin_dt = pd.to_datetime(p.s2_finale_date).values
    recon = {}
    for vl, col in (("completion_prefix", "tau_prefix"), ("any_s1_record", "tau_allE1")):
        lat = pd.to_datetime(p[col], unit="s", utc=True).dt.normalize().dt.tz_localize(None).values
        for wf in (True, False):
            t0l = np.maximum(lat, fin_dt) if wf else lat
            el = (TAU_PULL - t0l) / np.timedelta64(1, "D")
            recon[f"{vl}__finale_max_{wf}"] = {
                "median_elapsed_days": round(float(np.median(el[the720])), 1),
                "share_open_at_W60": round(float(np.mean(el[the720] < 60)), 4),
            }
    recon["share_of_720_where_finale_binds"] = round(
        float(np.mean(fin_dt[the720] > pd.to_datetime(
            p.tau_prefix, unit="s", utc=True).dt.normalize().dt.tz_localize(None).values[the720])), 4)
    recon["note"] = ("max(finale, .) is monotone, so including it can only make T0_latest later "
                     "and elapsed smaller; 2150 > 1738 is impossible with the max() included")
    out["reconciliation_720_bound"] = recon

    # ---------- record-level figures the artifact quotes ---------------------
    # These were previously produced in throwaway shells. Committed here so the
    # whole artifact greps against one file (F3).
    T_1990 = np.datetime64("1990-01-01").astype("datetime64[s]").astype(np.int64)
    rl_ts, rl_lag = d["ts"], d["lag_days"]
    rl_cor, rl_und, rl_tau = d["corrupt"], d["undated"], d["tau"]
    dated = (~rl_cor) & (~rl_und)
    bf180 = dated & (rl_lag > BACKFILL_D)
    union_bad = rl_cor | rl_und | bf180 | m3
    wave_lo = np.datetime64("2026-06-25").astype("datetime64[s]").astype(np.int64)
    wave_hi = np.datetime64("2026-07-23").astype("datetime64[s]").astype(np.int64)
    wave = (rl_tau >= wave_lo) & (rl_tau < wave_hi)
    rec = {
        "records_total": int(len(rl_ts)),
        "backfill_gt180d": int(bf180.sum()),
        "corrupt_pre1990": int(rl_cor.sum()),
        "undated": int(rl_und.sum()),
        "airdate_stamped": int(m3.sum()),
        "union_unusable_or_backfilled": int(union_bad.sum()),
        "union_share": round(float(union_bad.mean()), 4),
        "tvtime_wave_weeks_2026_06_25_to_07_22": {
            "records_written": int(wave.sum()),
            "of_which_backfilled": int((wave & bf180).sum()),
        },
    }
    fs = np.load(P5 / "full_scan.npz")
    NULL = np.iinfo(np.int64).min
    TAUP = np.datetime64("2026-08-11").astype("datetime64[s]").astype(np.int64)
    rt = (fs["ts"] != NULL) & (fs["ts"] <= TAUP) & (fs["action"] != 0)
    rec["calibration_fit_records_checkin_scrobble"] = int(rt.sum())
    rec["calibration_heldout_test_records_odd_users"] = int((rt & (fs["user"] % 2 == 1)).sum())
    out["F3_record_level"] = rec

    # ---------- FINAL ADOPTED RULE (revision 6) ------------------------------
    # Adoption 3 was DROPPED by the Human Lead: post-dated records are tagged and
    # kept out of the W estimation sample, and no pair is deleted for them. So the
    # analysis population is exactly the two adopted exclusions, and the four
    # readings of adoption 3 are moot - there is no rule left for them to apply.
    final_removed = all_air | the1542
    final_keep = ~final_removed
    fin = {
        "frame_pairs": int(len(p)),
        "excluded_all_airdate_s2": int(all_air.sum()),
        "excluded_contaminated_T0_no_s2": int(the1542.sum()),
        "excluded_overlap": int((all_air & the1542).sum()),
        "excluded_total": int(final_removed.sum()),
        "ANALYSIS_POPULATION": int(final_keep.sum()),
        "analysis_population_pct": round(100 * float(final_keep.mean()), 2),
        "postdated_pairs_deleted": 0,
        "postdated_pairs_retained_in_analysis_population": int((postd & final_keep).sum()),
    }

    # W estimation sample waterfall, Ruling 1, on the final population
    w1 = final_keep
    w2 = w1 & has_s2
    w3 = w2 & ~t0c
    w4 = w3 & ~postd
    w5 = w4 & ~fs2_bad
    fin["W_estimation_waterfall"] = [
        {"step": "analysis population", "n": int(w1.sum())},
        {"step": "has S2 evidence", "n": int(w2.sum()), "dropped": int((w1 & ~w2).sum())},
        {"step": "T0 not contaminated", "n": int(w3.sum()), "dropped": int((w2 & ~w3).sum())},
        {"step": "completing record not postdated", "n": int(w4.sum()), "dropped": int((w3 & ~w4).sum())},
        {"step": "first S2 watch clean", "n": int(w5.sum()), "dropped": int((w4 & ~w5).sum())},
    ]
    fin["W_ESTIMATION_SAMPLE"] = int(w5.sum())
    fin["W_estimation_sample_is_determinate"] = True
    fin["note"] = ("adoption 3 dropped, so no reading of it exists; E3's indeterminacy "
                   "(128,099 vs 131,043 under R3) is closed by the ruling")
    out["FINAL_ADOPTED_RULE"] = fin

    p.to_csv(P5 / "pair_revision5.csv", index=False)
    (P5 / "revision5.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
