"""Step 7 rerun on ALT-MATCHED (instance b, namespace mm_b) -- stage 6.

How fragile is the exclusion set under the stored calibration's residual?

This matters more under ALT-MATCHED than it did under ALT-BROAD. 0050 Sec 2
routed into Step 14 the finding that the started-and-left component is the
fragile one -- median margin 81.3 days against the never-started component's
202.5. ALT-MATCHED nearly doubles that component, and the 90 pairs it adds are
by definition pairs whose last insertion falls inside (tau1, tau2), i.e. within
91 days of tau2. Their margin is SMALL BY CONSTRUCTION. That has to be measured
and stated, not inferred.

Margin is measured against each pair's OWN silence instant: tau1 for branch (i),
tau2 for branch (ii). Under ALT-BROAD there was one instant; under ALT-MATCHED
there are two, and mixing them would misdescribe both components.

The calibration is READ, NEVER REFITTED. The residual ladder is applied as a
sensitivity shift to the per-account maximum, not as a refit.

ZERO network calls. Out: processed/step7/mm_b/margins.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "mm_b"
MISSING = np.iinfo(np.int64).min
W, H, DAY = 108, 91, 86400.0
QS = (0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100)
LADDER = [0.02, 0.107, 1.0, 7.0, 30.0, 124.6, 287.5]


def pct(a):
    return {f"p{q}": float(np.percentile(a, q)) for q in QS} if len(a) else None


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    in4 = pz["in_line4"]
    t0 = pz["t0_midnight_epoch"].astype(np.float64)
    mx_pair = pz["max_inst_pair"]
    uidx_all = pz["user_idx"]

    # per-account max CLAIMED watched_at, for the calibration-independent cross-check
    z = np.load(P5 / "full_scan.npz")
    user, ts = z["user"], z["ts"]
    dated = ts != MISSING
    n_users = int(user.max()) + 1
    max_claim = np.full(n_users, -np.inf)
    np.maximum.at(max_claim, user[dated], ts[dated].astype(np.float64))
    del z, user, ts, dated
    print(f"max claimed watched_at  ({time.time() - t:.1f}s)", flush=True)

    res: dict = {
        "instance": "data-scientist-b", "namespace": "mm_b", "stage": 6,
        "api_calls": 0, "adopts": "nothing", "rule_name": "ALT-MATCHED", "W": W, "H": H,
        "calibration": "READ, NEVER REFITTED. The ladder is a sensitivity shift, not a refit.",
        "margin_definition": ("distance below each pair's OWN silence instant: tau1 for the "
                              "never-started branch, tau2 for the started-and-left branch"),
        "residual_ladder_days": LADDER,
        "ladder_provenance": "the fit-family |residual| percentiles measured at bb_b stage 3a "
                             "(p50 0.0195 d, p90 0.107 d, p95 124.6 d, p97.5 287.5 d) plus "
                             "three round anchors; no ladder is specified by the spec",
        "by_population": {},
    }

    for pop in ("DERIV", "APPLY"):
        d10 = pz[f"d10_W{W}"]
        base = (d10 & in4) if pop == "DERIV" else d10
        ns = ~oz[f"started_W{W}"][base]
        sal = oz[f"sal_W{W}"][base].astype(bool)
        sil1, sil2 = pz[f"no_after_tau1_W{W}"][base], pz[f"no_after_tau2_W{W}"][base]
        tau1, tau2, m = t0[base] + W * DAY, t0[base] + (W + H) * DAY, mx_pair[base]
        u = uidx_all[base]

        bi, bii = ns & sil1, sal & sil2
        notlive = bi | bii
        new90 = bii & ~(sal & sil1)          # the pairs ALT-MATCHED adds
        old99 = bii & (sal & sil1)

        own = np.where(bi, tau1, tau2)
        marg_all = (own[notlive] - m[notlive]) / DAY
        d: dict = {
            "excluded_total": int(notlive.sum()),
            "margin_days_all": pct(marg_all),
            "margin_days_never_started_branch": pct((tau1[bi] - m[bi]) / DAY),
            "margin_days_started_and_left_branch": pct((tau2[bii] - m[bii]) / DAY),
            "margin_days_the_pairs_ALT_MATCHED_ADDS": pct((tau2[new90] - m[new90]) / DAY),
            "margin_days_the_pairs_ALT_BROAD_already_had": pct((tau2[old99] - m[old99]) / DAY),
            "n_added": int(new90.sum()), "n_already_had": int(old99.sum()),
            "added_margin_is_bounded_by_H_by_construction": bool(
                ((tau2[new90] - m[new90]) / DAY <= H).all()) if int(new90.sum()) else None,
        }

        # near-miss live pairs: live only by the silence conjunct, per branch
        lo_i, lo_ii = ns & ~sil1, sal & ~sil2
        d["near_miss_live"] = {
            "never_started_branch_n": int(lo_i.sum()),
            "never_started_branch_days_past_tau1": pct((m[lo_i] - tau1[lo_i]) / DAY),
            "started_and_left_branch_n": int(lo_ii.sum()),
            "started_and_left_branch_days_past_tau2": pct((m[lo_ii] - tau2[lo_ii]) / DAY),
        }

        # calibration-independent cross-check: any CLAIMED watched_at after the silence instant
        mc = max_claim[u]
        d["claimed_watched_at_cross_check"] = {
            "excluded_pairs_whose_account_claims_a_record_after_its_own_silence_instant":
                int((notlive & (mc > own)).sum()),
            "of_which_never_started_branch": int((bi & (mc > tau1)).sum()),
            "of_which_started_and_left_branch": int((bii & (mc > tau2)).sum()),
            "reading": ("an UPPER BOUND on the exclusions the residual could overturn, not an "
                        "estimate: a claim after the instant is either a backdated-forward claim, "
                        "which 0021 requires be ignored, or calibration error, and this cannot "
                        "separate them. It does NOT reintroduce a claimed-watched_at test."),
        }

        # stability ladder: shift every account's max instant by +/- delta, re-apply
        lad = {}
        for dd in LADDER:
            row = {}
            for sign, name in ((+1, "later_more_live"), (-1, "earlier_more_excluded")):
                mm = m + sign * dd * DAY
                s1, s2 = mm <= tau1, mm <= tau2
                nl = (ns & s1) | (sal & s2)
                row[name] = {"total": int(nl.sum()),
                             "never_started": int((ns & s1).sum()),
                             "started_and_left": int((sal & s2).sum())}
            lad[str(dd)] = row
        d["stability_ladder"] = lad
        d["ladder_direction_note"] = (
            "+delta = the true insertion was LATER than the curve says, which is the direction "
            "src/step5_calibrate.py states the curve errs in; it makes accounts more live and the "
            "exclusion set smaller.")
        res["by_population"][pop] = d
        print(f"{pop} done  ({time.time() - t:.1f}s)", flush=True)

    res["elapsed_s"] = time.time() - t
    (OUT / "margins.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res["by_population"]["APPLY"], indent=2)[:5000])


if __name__ == "__main__":
    main()
