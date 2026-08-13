"""Step 7 gate-closing sensitivity test (decisions/0041 SS4), instance namespace `a`.

STAGE 3 of 4 — apply the liveness filter at each setting and assign outcomes.

Settings (decisions/0041 SS4):
  T = 787    clustered-interval lower endpoint
  T = 1293   the point value
  T = 2200   clustered-interval upper endpoint
  parameter-free, no threshold at all

THE PARAMETER-FREE RULE HAS TWO READINGS AND THEY ARE NOT THE SAME RULE. Both are computed
and both are reported; this instance reconciles neither.
  PF-BRACKET (the literal text of 0041 SS4: "a distinct insertion instant at or before tau1
      AND one after it"): not live iff no instant after tau1 OR no instant at or before it.
      This REINSTATES 0036 SS2.3's second edge case, which decisions/0040 SS1 WITHDREW as
      contradicting approved gate 0021.
  PF-LIMIT (the T -> infinity limit of the threshold rule as 0040 leaves it): not live iff
      no instant after tau1. Pairs with no instant at or before tau1 are LIVE per 0021.

Threshold rule, per decisions/0036 SS2 as amended by 0040 SS1:
  not live iff (no insertion instant after tau1)                        [edge case (i)]
            or (the measured gap bracketing tau1 is >= T)
  a pair with no instant at or before tau1 is LIVE (0021, approved gate 2 of 5)

Outcome assignment, per Step 1 SS7 as amended by decisions/0034:
  Never started    |A| = 0                                    tested at tau1
  Continued        |A| >= 1 and F2 in A_H and |A_H| >= ceil(0.90*L2)   tested at tau2
  Started and left |A| >= 1 and not Continued

This is NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved gate.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/sens_a")
A4 = os.path.join(ROOT, "processed/step7/a4")

THRESHOLDS = [787, 1293, 2200]


def main():
    pop = np.load(os.path.join(OUT, "population.npz"))
    oi = np.load(os.path.join(OUT, "outcome_inputs.npz"))
    br = np.load(os.path.join(A4, "pair_bracketing_W108.npz"))

    # the a4 bracketing arrays are in pair_revision5 row order, as is population.npz
    assert np.array_equal(br["user_idx"], pop["user_idx"])
    assert np.array_equal(br["show"], pop["show"])
    assert np.array_equal(br["ref"], pop["ref"])

    rows = np.flatnonzero(pop["ref"])
    assert np.array_equal(rows, oi["pair_row_index"])
    n = rows.size

    no_before = br["no_before"][rows]
    no_after = br["no_after"][rows]
    gap = br["gap_days"][rows]
    measured = ~no_before & ~no_after
    assert np.isfinite(gap[measured]).all()
    assert np.isnan(gap[~measured]).all()

    user = pop["user_idx"][rows]
    nA, nAH = oi["nA"], oi["nAH"]
    f2_in_AH, need = oi["f2_in_AH"], oi["need"]

    started = nA >= 1
    continued = started & f2_in_AH & (nAH >= need)
    never = ~started
    left = started & ~continued
    assert int((never | continued | left).sum()) == n
    assert int((never & continued).sum()) == 0
    assert int((never & left).sum()) == 0
    assert int((continued & left).sum()) == 0

    def block(live, label, detail):
        k = int(live.sum())
        nv = int((never & live).sum())
        co = int((continued & live).sum())
        le = int((left & live).sum())
        assert nv + co + le == k
        return {
            "setting": label,
            **detail,
            "pairs_live": k,
            "pairs_excluded": n - k,
            "excluded_share_of_post_D10_pct": round(100.0 * (n - k) / n, 4),
            "accounts_touched_by_exclusion": int(np.unique(user[~live]).size),
            "counts": {"never_started": nv, "continued": co, "started_and_left": le},
            "shares_pct": {
                "never_started": round(100.0 * nv / k, 4),
                "continued": round(100.0 * co / k, 4),
                "started_and_left": round(100.0 * le / k, 4),
            },
        }

    settings = {}

    settings["no_liveness_filter"] = block(
        np.ones(n, dtype=bool), "no liveness filter at all (context row, not a candidate rule)",
        {"excluded_open_ended": 0, "excluded_measured_gap": 0, "excluded_no_instant_before": 0})

    for T in THRESHOLDS:
        dead_gap = measured & (gap >= T)
        dead = no_after | dead_gap
        settings[f"threshold_{T}d"] = block(
            ~dead, f"threshold rule at T = {T} d",
            {"threshold_days": T,
             "excluded_open_ended": int(no_after.sum()),
             "excluded_measured_gap": int(dead_gap.sum()),
             "excluded_no_instant_before": 0,
             "realised_rate_vs_measured_gap_pairs_pct":
                 round(100.0 * int(dead_gap.sum()) / int(measured.sum()), 4),
             "realised_rate_vs_extended_set_pct":
                 round(100.0 * int(dead.sum()) / int((measured | no_after).sum()), 4)})

    settings["parameter_free_LIMIT"] = block(
        ~no_after,
        "parameter-free, T -> infinity limit of the threshold rule as decisions/0040 leaves "
        "it: not live iff no insertion instant after tau1; the no-instant-before bucket is "
        "LIVE per 0021",
        {"threshold_days": None,
         "excluded_open_ended": int(no_after.sum()),
         "excluded_measured_gap": 0,
         "excluded_no_instant_before": 0})

    settings["parameter_free_BRACKET"] = block(
        measured,
        "parameter-free, the literal text of 0041 SS4: live iff a distinct insertion instant "
        "at or before tau1 AND one after it. THIS REINSTATES 0036 SS2.3(ii), WITHDRAWN BY 0040 SS1.",
        {"threshold_days": None,
         "excluded_open_ended": int(no_after.sum()),
         "excluded_measured_gap": 0,
         "excluded_no_instant_before": int(no_before.sum())})

    # ------------------------------------------------------------------ deltas
    order = ["threshold_787d", "threshold_1293d", "threshold_2200d",
             "parameter_free_LIMIT", "parameter_free_BRACKET", "no_liveness_filter"]
    states = ["never_started", "continued", "started_and_left"]

    def d(a, b, s):
        return round(settings[b]["shares_pct"][s] - settings[a]["shares_pct"][s], 4)

    named = {
        "787_to_1293": {s: d("threshold_787d", "threshold_1293d", s) for s in states},
        "1293_to_2200": {s: d("threshold_1293d", "threshold_2200d", s) for s in states},
        "787_to_2200_FULL_CLUSTERED_INTERVAL": {
            s: d("threshold_787d", "threshold_2200d", s) for s in states},
        "1293_to_parameter_free_LIMIT": {
            s: d("threshold_1293d", "parameter_free_LIMIT", s) for s in states},
        "1293_to_parameter_free_BRACKET": {
            s: d("threshold_1293d", "parameter_free_BRACKET", s) for s in states},
        "no_filter_to_1293": {s: d("no_liveness_filter", "threshold_1293d", s) for s in states},
    }
    matrix = {a: {b: {s: d(a, b, s) for s in states} for b in order} for a in order}

    span = {s: round(max(settings[k]["shares_pct"][s] for k in
                         ("threshold_787d", "threshold_1293d", "threshold_2200d",
                          "parameter_free_LIMIT"))
                     - min(settings[k]["shares_pct"][s] for k in
                           ("threshold_787d", "threshold_1293d", "threshold_2200d",
                            "parameter_free_LIMIT")), 4)
            for s in states}

    out = {
        "step": 7,
        "what": "GATE-CLOSING SENSITIVITY DIAGNOSTIC for Step 7 (decisions/0041 SS4). "
                "NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved "
                "gate, so these shares are provisional in POPULATION as well as in status.",
        "instance": "sens_a",
        "api_calls": 0,
        "population_post_D10": n,
        "population_line": "Step 5 waterfall line 4 (152,126) less D10 right-censoring at "
                           "W=108, H=91 -> 147,370",
        "W_days": 108, "H_days": 91,
        "tau1": "[[T0]] + 108*24h", "tau2": "[[T0]] + 199*24h",
        "classes_at_tau1": {
            "measured_bracketing_gap": int(measured.sum()),
            "open_ended_no_instant_after_tau1": int(no_after.sum()),
            "no_instant_at_or_before_tau1": int(no_before.sum()),
        },
        "pre_liveness_outcomes": {
            "never_started": int(never.sum()),
            "continued": int(continued.sum()),
            "started_and_left": int(left.sum()),
        },
        "settings": settings,
        "deltas_pp": named,
        "delta_matrix_pp": matrix,
        "max_minus_min_share_pp_across_the_four_candidate_settings": span,
    }
    with open(os.path.join(OUT, "sensitivity.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    np.savez_compressed(
        os.path.join(OUT, "pair_states.npz"),
        user=user, never=never, continued=continued, left=left,
        no_before=no_before, no_after=no_after, gap=gap, measured=measured,
    )
    print(json.dumps({"settings": {k: {"pairs_live": v["pairs_live"],
                                       "shares_pct": v["shares_pct"]}
                                   for k, v in settings.items()},
                      "deltas_pp": named,
                      "span_pp": span}, indent=2))


if __name__ == "__main__":
    main()
