"""Step 7 RERUN on ALT-MATCHED (decisions/0052), namespace `a`. STAGE 5 — CHECKS.

  1. the waterfall, with line 6 OUTCOME-CONDITIONAL and split by state;
  2. monotone decrease at position 6, strict or non-strict, PER POPULATION, at every arm;
  3. commutation: outcome assignment and liveness are row-local predicates on the position-5
     output; checked by computing the surviving state counts BOTH ways, not asserted;
  4. tie sensitivity at BOTH instants -- the rule now reads two thresholds, so a tie can occur at
     tau1 or at tau2;
  5. NEW UNDER ALT-MATCHED: the post-tau2 observation window. D10 admits pairs with
     tau2 == tau_pull, so the tau2 silence test can have a ZERO-LENGTH window in which to observe
     the insertion that would prove liveness. The tau1 test always has at least H days. Measured,
     because it is an asymmetry the rule change introduces;
  6. the calibration clamp. Under ALT-BROAD it was inert (0 of 703 exclusions on clamped
     accounts) because the clamp time exceeds every tau1. It is NOT automatically inert against
     tau2, which can be later than the clamp time. Re-measured rather than carried over.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/mm_a")

DAY = 86400.0
H = 91
W_ADOPTED = 108
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)
CLAMP_TIME = np.datetime64("2026-08-10T20:48:00", "s").astype("int64").astype(float)
STATES = ["never_started", "continued", "started_and_left"]


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    pop = np.load(os.path.join(OUT, "population.npz"))
    never, cont, left = m["never"], m["cont"], m["left"]
    ex, ex_ns, ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    tau1, tau2, last = m["tau1"], m["tau2"], m["last_inst"]
    arms = json.load(open(os.path.join(OUT, "arms.json")))["arms"]
    line4 = pop["line4"][pop["line1"]]
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    out = {"step": 7, "instance": "mm_a", "stage": 5, "api_calls": 0, "W": W_ADOPTED, "H": H}

    # ---- 1. waterfall, line 6 outcome-conditional ---------------------------------------
    wf = {}
    for nm, p in pops.items():
        k = int((ex & p).sum())
        wf[nm] = {
            "position_4_contamination_exclusion": 152126 if nm == "DERIV" else 201900,
            "position_5_right_censoring_D10": int(p.sum()),
            "position_6_liveness_OUTCOME_CONDITIONAL": int(p.sum()) - k,
            "position_6_removed": k,
            "position_6_removed_never_started": int((ex_ns & p).sum()),
            "position_6_removed_started_and_left": int((ex_sl & p).sum()),
            "position_6_removed_continued": int((ex & p & cont).sum()),
            "why_outcome_conditional": "both disjuncts of the rule contain a position-7 outcome "
                                       "predicate (|A| = 0 in one, NOT Continued in the other), so "
                                       "the removed count cannot be stated without reference to "
                                       "outcome assignment, and it removes rows from TWO outcome "
                                       "states",
        }
    out["waterfall"] = wf

    # ---- 2. monotone decrease at position 6, per population, per arm --------------------
    mono = {}
    for nm in ("DERIV", "APPLY"):
        rows = []
        for W, r in arms.items():
            d = r["D10_per_arm"][nm]
            rows.append({"W": int(W), "before": d["population_pairs"],
                         "after": d["population_pairs"] - d["excluded_pairs"],
                         "removed": d["excluded_pairs"],
                         "strict": d["excluded_pairs"] > 0})
        mono[nm] = {
            "per_arm": sorted(rows, key=lambda x: x["W"]),
            "strict_at_every_arm": all(x["strict"] for x in rows),
            "non_strict_holds_everywhere": all(x["after"] <= x["before"] for x in rows),
        }
    out["monotone_decrease_at_position_6"] = mono
    out["monotone_note"] = ("STRICT on BOTH populations at every arm tested. The `>=` coding is "
                            "KEPT: strictness is a fact about this pull date, not a theorem, and "
                            "the invariant must not encode a property of one rule. Under the "
                            "SUPERSEDED ALT the DERIV set was empty at every arm and decrease was "
                            "non-strict there; under ALT-BROAD it was 99; under ALT-MATCHED it is "
                            "188 at W = 108.")

    # ---- 3. commutation -----------------------------------------------------------------
    comm = {}
    for nm, p in pops.items():
        # order A: assign outcomes on position-5 output, then drop the excluded rows
        a = [int((never & p & ~ex).sum()), int((cont & p & ~ex).sum()), int((left & p & ~ex).sum())]
        # order B: drop the excluded rows first, then assign outcomes on the survivors
        surv = p & ~ex
        b = [int((never & surv).sum()), int((cont & surv).sum()), int((left & surv).sum())]
        comm[nm] = {"assign_then_filter": dict(zip(STATES, a)),
                    "filter_then_assign": dict(zip(STATES, b)),
                    "identical": a == b}
    out["commutation_check"] = comm
    out["commutation_note"] = ("0029's ordering rationale concerns per-filter SAMPLE SIZE, which "
                               "cannot reach position 7 because outcome assignment removes no "
                               "rows: positions 1-6 are filters, position 7 is an annotation.")

    # ---- 4. tie sensitivity at BOTH instants --------------------------------------------
    ties = {}
    for nm, p in pops.items():
        d1 = np.abs(last - tau1)[p]
        d2 = np.abs(last - tau2)[p]
        ties[nm] = {
            "pairs_with_last_instant_exactly_at_tau1": int((d1 == 0).sum()),
            "pairs_with_last_instant_within_1s_of_tau1": int((d1 <= 1).sum()),
            "pairs_with_last_instant_exactly_at_tau2": int((d2 == 0).sum()),
            "pairs_with_last_instant_within_1s_of_tau2": int((d2 <= 1).sum()),
            "pairs_with_last_instant_within_60s_of_tau2": int((d2 <= 60).sum()),
        }
    out["tie_convention"] = {
        "convention": "'after tau' is read STRICTLY, so silence is max(instant) <= tau. A tie does "
                      "not prove liveness. Judgement call; the spec is silent.",
        "by_population": ties,
    }

    # ---- 5. the post-tau2 observation window -- NEW under ALT-MATCHED -------------------
    win = {}
    for nm, p in pops.items():
        w1 = (TAU_PULL - tau1)[p] / DAY
        w2 = (TAU_PULL - tau2)[p] / DAY
        esl = ex_sl & p
        w2e = (TAU_PULL - tau2)[esl] / DAY
        win[nm] = {
            "post_tau1_window_days": {"min": round(float(w1.min()), 4),
                                      "p25": round(float(np.percentile(w1, 25)), 1),
                                      "median": round(float(np.median(w1)), 1),
                                      "max": round(float(w1.max()), 1)},
            "post_tau2_window_days": {"min": round(float(w2.min()), 4),
                                      "p25": round(float(np.percentile(w2, 25)), 1),
                                      "median": round(float(np.median(w2)), 1),
                                      "max": round(float(w2.max()), 1)},
            "pairs_with_ZERO_post_tau2_window": int((w2 <= 0).sum()),
            "pairs_with_post_tau2_window_under_7d": int((w2 < 7).sum()),
            "pairs_with_post_tau2_window_under_30d": int((w2 < 30).sum()),
            "excluded_started_and_left_post_tau2_window_days": {
                "min": round(float(w2e.min()), 4) if esl.any() else None,
                "median": round(float(np.median(w2e)), 1) if esl.any() else None,
                "max": round(float(w2e.max()), 1) if esl.any() else None,
                "count_with_zero_window": int((w2e <= 0).sum()) if esl.any() else None,
                "count_with_window_under_7d": int((w2e < 7).sum()) if esl.any() else None,
                "count_with_window_under_30d": int((w2e < 30).sum()) if esl.any() else None,
            },
        }
    out["post_tau2_observation_window"] = win
    out["post_tau2_note"] = (
        "D10 is [[T0]] + (max(W,91)+H)*24h <= tau_pull. At W = 108 that is exactly "
        "T0 + 199d <= tau_pull, and tau2 = T0 + 199d, so tau2 <= tau_pull with EQUALITY attainable: "
        "a pair at the censoring boundary has a zero-length window in which the insertion that "
        "would prove its liveness could be observed. The tau1 test never has this problem -- "
        "tau_pull - tau1 >= H days at every arm with W <= max(W,91). This asymmetry is introduced "
        "BY the rule change and is reported as a limitation, not repaired here.")

    # ---- 6. the calibration clamp, re-measured against tau2 -----------------------------
    clamp = {}
    for nm, p in pops.items():
        cl = p & (last >= CLAMP_TIME)
        clamp[nm] = {
            "clamp_time_utc": str(np.datetime64(int(CLAMP_TIME), "s")),
            "pairs_on_clamped_accounts": int(cl.sum()),
            "clamped_pairs_excluded_total": int((cl & ex).sum()),
            "clamped_pairs_excluded_never_started": int((cl & ex_ns).sum()),
            "clamped_pairs_excluded_started_and_left": int((cl & ex_sl).sum()),
            "clamped_pairs_whose_tau2_exceeds_the_clamp_time": int((cl & (tau2 > CLAMP_TIME)).sum()),
            "clamped_pairs_whose_tau1_exceeds_the_clamp_time": int((cl & (tau1 > CLAMP_TIME)).sum()),
        }
    out["calibration_clamp"] = clamp
    out["calibration_clamp_note"] = (
        "Under ALT-BROAD the clamp was INERT: the clamp time 2026-08-10T20:48Z exceeds every tau1 "
        "the rule can read, so a clamped account was live everywhere and 0 of 703 exclusions sat "
        "on one. That argument does NOT transfer to tau2, because tau2 can run to tau_pull, which "
        "is LATER than the clamp time. Re-measured above.")

    with open(os.path.join(OUT, "checks.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
