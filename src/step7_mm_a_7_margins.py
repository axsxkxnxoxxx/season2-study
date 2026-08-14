"""Step 7 RERUN on ALT-MATCHED (decisions/0052), namespace `a`. STAGE 7 — MARGINS AND RESIDUAL.

The rule compares an INTERPOLATED insertion instant against a threshold. If the curve reads EARLY,
a live account is scored silent and the pair is FALSELY EXCLUDED. This stage re-measures how far
each exclusion sits from ITS OWN threshold -- tau1 for the never-started branch, tau2 for the
started-and-left branch -- and re-runs the two robustness tests on the NEW exclusion set.

The per-account residual arrays are REUSED from the prior namespace-`a` run
(processed/step7/bb_a/residual_accounts.npz) and CROSS-CHECKED against this run's own instants
before use. The stored calibration is READ, never refitted (0029). The residual DISTRIBUTION is a
property of the curve and the records, so it does not change with the rule; what changes is the
exclusion set it is applied to, which is why this stage is re-run rather than carried over.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/mm_a")
PRIOR = os.path.join(ROOT, "processed/step7/bb_a")
DAY = 86400.0
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)
SHIFTS = [0.0, 0.0195, 0.107, 1.0, 7.0, 30.0, 77.5, 124.6, 365.0]


def q(x, qs=(0, 25, 50, 75, 90, 100)):
    return {f"p{p}": round(float(np.percentile(x, p)), 4) for p in qs} if x.size else None


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    li = np.load(os.path.join(OUT, "instants.npz"))
    ra = np.load(os.path.join(PRIOR, "residual_accounts.npz"))

    assert np.array_equal(ra["uids"], li["uids"]), "residual account set differs"
    assert float(np.max(np.abs(ra["last_inst"] - li["last_inst"]))) == 0.0, \
        "residual last_inst differs from this run's"

    never, cont, left = m["never"], m["cont"], m["left"]
    ex, ex_ns, ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    tau1, tau2, last, user = m["tau1"], m["tau2"], m["last_inst"], m["user"]
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    # per-pair own threshold: tau1 for the never-started branch, tau2 for started-and-left
    own_tau = np.where(never, tau1, tau2)

    # non-parametric corrected last instant: a genuine record cannot be inserted before it was
    # watched, so the true instant is at least max(interp(max rid), max dated watched_at)
    uids = li["uids"]
    slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    slot[uids] = np.arange(uids.size)
    corr_acc = np.maximum(ra["last_inst"], np.where(np.isfinite(ra["max_ts"]), ra["max_ts"],
                                                    -np.inf))
    corr = corr_acc[slot[user]]
    clamped_pair = ra["clamped"][slot[user]]
    act_at_max = ra["act_at_max"][slot[user]]

    out = {"step": 7, "instance": "mm_a", "stage": 7, "api_calls": 0,
           "reused": "processed/step7/bb_a/residual_accounts.npz (namespace a), cross-checked",
           "by_population": {}}

    for nm, p in pops.items():
        e, ens, esl = ex & p, ex_ns & p, ex_sl & p
        marg = (own_tau - last)[e] / DAY
        rec = {
            "population_pairs": int(p.sum()),
            "exclusions": int(e.sum()),
            "margin_days_to_OWN_threshold": {
                "all_exclusions": q(marg),
                "never_started_component_vs_tau1": q((tau1 - last)[ens] / DAY),
                "started_and_left_component_vs_tau2": q((tau2 - last)[esl] / DAY),
                "within_0.0195d_residual_median": int((marg <= 0.0195).sum()),
                "within_1d": int((marg <= 1).sum()),
                "within_7d": int((marg <= 7).sum()),
                "within_30d": int((marg <= 30).sum()),
                "within_90d": int((marg <= 90).sum()),
            },
            "margin_of_the_LIVE_pairs_that_could_flip": {
                "note": "live and NOT Continued; a Continued pair cannot be excluded whatever the "
                        "instant does. Distance from the pair's own threshold, in days.",
                "distribution": q((last - own_tau)[p & ~cont & ~ex] / DAY),
                "within_1d": int(((last - own_tau)[p & ~cont & ~ex] / DAY < 1).sum()),
                "within_7d": int(((last - own_tau)[p & ~cont & ~ex] / DAY < 7).sum()),
            },
            "uniform_shift_delta_days": {},
            "non_parametric_correction": {},
            "where_the_residual_is_directly_measurable": {
                "note": "the residual can be measured AT the point the rule reads only where the "
                        "account's own last record is checkin or scrobble (action != 0), the "
                        "family on which watched_at IS the insertion time. For the import family "
                        "(action == 0) watched_at carries no information about insertion time and "
                        "only the two tests above are evidence.",
                "excluded_on_fit_family_accounts": int((e & (act_at_max != 0)).sum()),
                "excluded_on_import_family_accounts": int((e & (act_at_max == 0)).sum()),
            },
            "clamped_accounts": {
                "excluded_pairs_on_clamped_accounts": int((e & clamped_pair).sum()),
                "note": "under ALT-BROAD this was 0, because the clamp time exceeds every tau1. "
                        "It is not automatically 0 against tau2.",
            },
        }
        for d in SHIFTS:
            shifted = last + d * DAY
            nx_ns = never & (shifted <= tau1) & p
            nx_sl = left & (shifted <= tau2) & p
            tot = int((nx_ns | nx_sl).sum())
            rec["uniform_shift_delta_days"][str(d)] = {
                "excluded": tot,
                "retained_pct": round(100.0 * tot / int(e.sum()), 2) if e.any() else None,
                "never_started": int(nx_ns.sum()), "started_and_left": int(nx_sl.sum()),
            }
        cx_ns = never & (corr <= tau1) & p
        cx_sl = left & (corr <= tau2) & p
        cx = cx_ns | cx_sl
        rec["non_parametric_correction"] = {
            "rule": "last_inst' = max(interp(max rid), max dated watched_at <= tau_pull); assumes "
                    "only that a record is not inserted before it is watched -- no magnitude "
                    "assumption at all",
            "pairs_whose_account_instant_moved_later": int((p & (corr > last)).sum()),
            "median_move_days_where_moved": round(
                float(np.median(((corr - last)[p & (corr > last)]) / DAY)), 4)
            if (p & (corr > last)).any() else None,
            "exclusions_after_correction": int(cx.sum()),
            "of_the_original_exclusions_surviving": int((cx & e).sum()),
            "survival_pct": round(100.0 * (cx & e).sum() / e.sum(), 2) if e.any() else None,
            "lost_never_started": int((e & ex_ns & ~cx).sum()),
            "lost_started_and_left": int((e & ex_sl & ~cx).sum()),
            "NEW_exclusions_created": int((cx & ~e & p).sum()),
        }
        out["by_population"][nm] = rec

    with open(os.path.join(OUT, "margins.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
