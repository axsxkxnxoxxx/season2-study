"""Step 7 RERUN on ALT-BROAD (decisions/0048), namespace `a`. STAGE 6b of 8 —
IS THE EXCLUSION SET STABLE UNDER PLAUSIBLE CALIBRATION RESIDUAL?

Conjunct 1 fires when max(instant) <= tau1. Three tests, in increasing order of strength:

  A. MARGINS. The distribution of tau1 - max(instant) for every EXCLUDED pair (how much later
     the instant must read before the pair flips to live) and of max(instant) - tau1 for the
     LIVE pairs that are near misses (how much earlier it must read before they flip to
     excluded). Both in days, both populations, both exclusion components.

  B. UNIFORM SHIFT. Re-run the rule with every instant moved by +delta, for delta drawn from
     the stage-6a residual quantiles and from the tail the "claims later" diagnostic exposes.
     A positive delta corrects a curve that reads EARLY, so it can only REMOVE exclusions.

  C. NON-PARAMETRIC CORRECTION, and the strongest of the three. A genuine record cannot be
     inserted before it was watched, so for every dated record the true insertion instant is
     at least max(interp(rid), watched_at). Taking the account-wide maximum of that lower
     bound gives a residual-corrected last instant that needs NO assumption about the size of
     the error, only its direction, and it absorbs the whole 22.68% finding at once:
        last_inst' = max( interp(max rid), max dated watched_at <= tau_pull )
     Re-running the rule on last_inst' gives the exclusion count that survives the correction.

  D. THE CLAMP. Records clamped above the curve get the last knot time, 2026-08-10T20:48Z.
     D10 forces tau1 <= tau_pull - H*24h = 2026-05-12 at EVERY arm, so a clamped account's
     instant is later than any tau1 in either population and the account is live everywhere.
     Checked directly against the exclusion set rather than argued.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/bb_a")

SEC_PER_DAY = 86400.0
W, H = 108, 91
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)
QS = [0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100]
DELTAS_D = [0.0195, 0.0422, 0.1072, 1.0, 7.0, 30.0, 77.483, 124.6412, 365.0, 470.6171]
NEAR = [0.0195, 0.1072, 1.0, 7.0, 30.0, 90.0, 180.0, 365.0]


def qd(x):
    if x.size == 0:
        return None
    return {f"p{q}": round(float(np.percentile(x, q)), 4) for q in QS}


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    ra = np.load(os.path.join(OUT, "residual_accounts.npz"))
    user = m["user"]
    never, cont, left = m["never"], m["cont"], m["left"]
    ex, ex_ns, ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    t0f, last_inst = m["t0f"], m["last_inst"]
    tau1 = t0f + W * SEC_PER_DAY
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    uids = ra["uids"]
    slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    slot[uids] = np.arange(uids.size)
    us = slot[user]
    assert np.array_equal(ra["last_inst"][us], last_inst), "instant arrays disagree"
    max_ts = ra["max_ts"][us]
    clamped = ra["clamped"][us]
    act_at_max = ra["act_at_max"][us]
    res_at_max = ra["res_at_max"][us]

    out = {"step": 7, "instance": "bb_a", "stage": "6b", "api_calls": 0, "W": W, "H": H,
           "by_population": {}}

    # ---- D. the clamp, settled before anything else ---------------------------------
    out["clamp_check"] = {
        "clamp_value_utc": "2026-08-10T20:48:00",
        "max_tau1_possible_at_any_arm_utc": str(
            np.datetime64(int(TAU_PULL - H * SEC_PER_DAY), "s")),
        "max_tau1_observed_at_W108_on_APPLY_utc": str(
            np.datetime64(int(tau1[pops["APPLY"]].max()), "s")),
        "note_on_that_figure": "the maximum is taken over the APPLY population, i.e. AFTER "
                               "D10; the line-1 table before D10 reaches 2026-11-27, which is "
                               "not a tau1 the rule ever reads",
        "pairs_on_APPLY_whose_account_max_rid_is_clamped_above": int(
            (clamped & pops["APPLY"]).sum()),
        "of_those_excluded": int((clamped & pops["APPLY"] & ex).sum()),
        "verdict": "clamping ABOVE cannot cause a false exclusion at any arm: the clamp value "
                   "is later than the largest tau1 D10 permits, so every clamped account is "
                   "LIVE for every pair. Instance B's stated direction is correct in "
                   "principle and INERT here.",
    }

    for nm, p in pops.items():
        e, ens, esl = ex & p, ex_ns & p, ex_sl & p
        live = p & ~ex
        # A. margins
        slack = (tau1[e] - last_inst[e]) / SEC_PER_DAY            # >= 0 on exclusions
        over = (last_inst[live] - tau1[live]) / SEC_PER_DAY       # > 0 on live pairs
        # live pairs that are near misses only matter where the pair is NOT Continued: a
        # Continued pair fails conjunct 2 and can never be excluded however the instant moves
        nearable = live & ~cont
        over_nearable = (last_inst[nearable] - tau1[nearable]) / SEC_PER_DAY

        rec = {
            "population_pairs": int(p.sum()),
            "excluded_pairs": int(e.sum()),
            "A_margin_tau1_minus_max_instant_days_EXCLUDED": {
                "all": qd(slack),
                "never_started_component": qd((tau1[ens] - last_inst[ens]) / SEC_PER_DAY),
                "started_and_left_component": qd((tau1[esl] - last_inst[esl]) / SEC_PER_DAY),
                "count_within_0.0195d_residual_median": int((slack <= 0.0195).sum()),
                "count_within_0.1072d_residual_p90": int((slack <= 0.1072).sum()),
                "count_within_1d": int((slack <= 1).sum()),
                "count_within_7d": int((slack <= 7).sum()),
                "count_within_30d": int((slack <= 30).sum()),
                "count_within_90d": int((slack <= 90).sum()),
                "count_within_365d": int((slack <= 365).sum()),
                "reading": "an excluded pair survives any residual correction smaller than "
                           "its own margin; the count within a given residual is the number "
                           "of exclusions that correction could reverse",
            },
            "A_margin_max_instant_minus_tau1_days_LIVE_NEAR_MISSES": {
                "all_live": qd(over),
                "live_and_not_continued_the_only_flippable_ones": qd(over_nearable),
                "counts_within": {str(t): int((over_nearable <= t).sum()) for t in NEAR},
                "reading": "a live pair can only flip to excluded if it is NOT Continued and "
                           "the curve reads LATE by more than this margin; the residual's "
                           "sign here is the opposite of the one that worries 0048 SS9",
            },
            "B_uniform_shift_plus_delta_days": {},
            "C_nonparametric_correction": {},
            "excluded_set_provenance": {
                "excluded_accounts": int(np.unique(user[e]).size),
                "max_rid_record_is_watch_import_family": int(
                    (act_at_max[e] == 0).sum()),
                "max_rid_record_is_checkin_or_scrobble": int((act_at_max[e] > 0).sum()),
                "residual_at_that_record_days_where_measurable": qd(
                    res_at_max[e][~np.isnan(res_at_max[e])]),
                "reading": "where the account's own last record is a checkin or scrobble the "
                           "residual at exactly the point the rule reads is directly "
                           "measurable; where it is a watch it is not, and the uniform-shift "
                           "and non-parametric tests are what cover it",
            },
        }

        for dlt in DELTAS_D:
            shifted = last_inst + dlt * SEC_PER_DAY
            ex_d = (shifted <= tau1) & ~cont
            rec["B_uniform_shift_plus_delta_days"][str(dlt)] = {
                "excluded_pairs": int((ex_d & p).sum()),
                "never_started_component": int((ex_d & p & never).sum()),
                "started_and_left_component": int((ex_d & p & left).sum()),
                "exclusions_lost_vs_delta_0": int(e.sum()) - int((ex_d & p).sum()),
                "pct_of_exclusion_set_retained": round(
                    100.0 * (ex_d & p).sum() / max(int(e.sum()), 1), 2),
            }

        corrected = np.maximum(last_inst, max_ts)
        ex_c = (corrected <= tau1) & ~cont
        moved = (corrected > last_inst)
        rec["C_nonparametric_correction"] = {
            "definition": "last_inst' = max(interp(max rid), max dated watched_at <= tau_pull)",
            "assumption": "direction only: a genuine record is not inserted before it is "
                          "watched, so watched_at is a lower bound on its insertion instant",
            "pairs_whose_account_instant_moved_later": int((moved & p).sum()),
            "median_move_days_where_moved": round(float(np.median(
                (corrected[moved & p] - last_inst[moved & p]) / SEC_PER_DAY)), 4)
                if (moved & p).any() else None,
            "excluded_pairs_after_correction": int((ex_c & p).sum()),
            "never_started_component_after": int((ex_c & p & never).sum()),
            "started_and_left_component_after": int((ex_c & p & left).sum()),
            "exclusions_lost": int(e.sum()) - int((ex_c & p).sum()),
            "pct_of_exclusion_set_retained": round(
                100.0 * (ex_c & p).sum() / max(int(e.sum()), 1), 2),
            "new_exclusions_created": int((ex_c & p & ~ex).sum()),
        }
        out["by_population"][nm] = rec

    with open(os.path.join(OUT, "stability.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
