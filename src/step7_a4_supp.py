"""Step 7 rerun (decisions/0040), instance A4 — supplementary numbers for the deliverable.

  - what D10 removed, decomposed by liveness class
  - the inertness split under the measured-gap-only reference, across percentiles
  - the tie multiplicity at the selected order statistic, which is why every percentile
    convention returns the same value
  - the edge-case-(i) redundancy check under both candidate references

Zero API calls.
"""
import json
import math
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/a4")
PCTL = 99.0


def main():
    d = np.load(os.path.join(OUT, "pair_bracketing_W108.npz"))
    ref152, keep10 = d["ref152"], d["keep_d10"]
    gap, no_after, no_before = d["gap_days"], d["no_after"], d["no_before"]
    ref = ref152 & keep10
    meas = ~no_after & ~no_before

    def cls(mask):
        return {
            "measured": int((mask & meas).sum()),
            "open_ended": int((mask & no_after).sum()),
            "no_pre_tau1": int((mask & no_before).sum()),
            "total": int(mask.sum()),
        }

    before = cls(ref152)
    after = cls(ref)
    removed = {k: before[k] - after[k] for k in before}

    g = gap[ref & meas]
    n_meas, n_open = int(g.size), int((ref & no_after).sum())
    n_pairs = int(ref.sum())

    # inertness under the measured-gap-only reference
    inert_meas = {}
    for q in (90.0, 95.0, 97.5, 99.0, 99.5, 99.9):
        tq = int(math.ceil(float(np.percentile(g, q))))
        dq = int((g >= tq).sum())
        tot = dq + n_open
        inert_meas[str(q)] = {
            "threshold_days": tq,
            "not_live_measured_gap": dq,
            "not_live_open_ended": n_open,
            "not_live_total": tot,
            "measured_gap_share_of_exclusions": round(dq / tot, 6),
            "evidence_absence_share_of_exclusions": round(n_open / tot, 6),
            "realised_rate_vs_measured_gap_pairs": round(dq / n_meas, 6),
            "realised_rate_vs_post_D10_population": round(tot / n_pairs, 6),
        }

    # tie multiplicity at the two selected order statistics
    def tie_at(v):
        return int((g == v).sum())

    raw_m = float(np.percentile(g, PCTL))
    ext = np.concatenate([g, np.full(n_open, np.inf)])
    raw_e = float(np.percentile(ext, PCTL))

    # the percentile above which the extended reference goes infinite
    crit = 100.0 * (1.0 - n_open / (n_meas + n_open))

    supp = {
        "instance": "a4",
        "api_calls": 0,
        "d10_effect_by_class": {
            "before_152126": before,
            "after_D10": after,
            "removed_by_D10": removed,
            "note": (
                "decisions/0040 SS2 anticipated 894 open-ended out of a 130,524 extended set "
                "(0.685%). Measured here: 751 out of 129,218 (0.581%). The anticipated figure "
                "is the pre-D10 extended set (133,876) less the 3,352 pairs whose tau1 is past "
                "the pull instant, i.e. it assumes D10 acts only on the open-ended bucket. D10 "
                "is a cut on [[T0]] + (max(W,91)+H)*24h, which is 91 days stricter than tau1 > "
                "tau_pull, so it removes pairs from every class: "
                f"{removed['open_ended']} open-ended, {removed['measured']} measured, "
                f"{removed['no_pre_tau1']} no-pre-tau1. The conclusion 0040 draws from the "
                "figure is unaffected: the open-ended share is well under 1%, so the extended "
                "99th is finite."
            ),
        },
        "inertness_measured_only_reference": inert_meas,
        "order_statistic_ties": {
            "measured_only_p99_value_days": raw_m,
            "pairs_at_exactly_that_value": tie_at(raw_m),
            "extended_p99_value_days": raw_e,
            "pairs_at_exactly_that_value_extended": tie_at(raw_e),
            "why_it_matters": (
                "every numpy percentile convention and the nearest-rank ceiling return the "
                "same value because the selected order statistic sits inside a tie plateau. "
                "It is also why the measured-only p99 is bit-identical before and after D10."
            ),
        },
        "edge_case_i_redundancy": {
            "question": "is 0036 SS2.3(i) still needed as a separate ruling?",
            "open_ended_pairs": n_open,
            "extended_reference": {
                "threshold_days": int(math.ceil(raw_e)),
                "an_infinite_gap_fails_it": True,
                "separate_ruling_needed": False,
            },
            "measured_only_reference": {
                "threshold_days": int(math.ceil(raw_m)),
                "an_infinite_gap_fails_it": True,
                "separate_ruling_needed": False,
            },
            "what_IS_still_needed": (
                "the CONVENTION that an absent successor instant is scored as an infinite gap "
                "rather than as undefined. That is a definition, not a liveness ruling. Once it "
                "is stated, the branch is arithmetic: inf >= any finite threshold."
            ),
            "extended_reference_finiteness_margin": {
                "open_ended_share": round(n_open / (n_meas + n_open), 6),
                "percentile_above_which_the_extended_p_is_infinite": round(crit, 4),
                "headroom_from_the_99th_in_percentile_points": round(crit - 99.0, 4),
            },
        },
    }
    with open(os.path.join(OUT, "supplementary.json"), "w") as f:
        json.dump(supp, f, indent=2)
    print(json.dumps(supp, indent=2))


if __name__ == "__main__":
    main()
