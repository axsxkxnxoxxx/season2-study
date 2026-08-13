"""Step 7 RERUN ON THE ADOPTED RULE ALT-BROAD (instance b, namespace bb_b) -- stage 1.

GATE. NOTHING IS ADOPTED HERE. The Human Lead approves and diffs the two arms.

THE ADOPTED RULE (decisions/0048 Sec 1, task-sheet.md Step 7 as rewritten):

    A user-show pair is NOT LIVE iff BOTH
      (a) the account shows no insertion instant after that pair's
          tau1 = [T0] + W x 24h, AND
      (b) the pair is NOT Continued.

"Continued" is Step 1 Sec 7 as amended by 0034:
    |A| >= 1  AND  F2 in A_H  AND  |A_H| >= ceil(0.90 x L2),  read at
    tau2 = [T0] + (W + H) x 24h.

So conjunct (b) is satisfied by BOTH Never started (|A| = 0) and Started and
left (|A| >= 1 AND NOT Continued). That is the change from the superseded ALT,
whose conjunct (b) was |A| = 0 alone.

POPULATIONS -- every figure carries one (0046 Sec 0):
  DERIV  Step 5 waterfall line 4 (152,126) less D10 -> 147,370 at W = 108.
  APPLY  Step 5 waterfall line 1 (201,900) less D10 -> 196,654 at W = 108.

REUSE. Conjunct (a), D10 per arm, and the outcome assignment at every arm were
built by THIS instance at processed/step7/alt2_b/{pairs,outcomes}.npz under the
ALT rerun. They are inputs to the rule, not the rule, and neither changed at
0048. They are reused rather than recomputed, and their construction provenance
is re-asserted here: the Step 5 waterfall is recomputed from pair_revision5.csv
and checked line by line, and both populations are checked against it.

ZERO network calls. Reads only. The calibration is READ, NEVER REFITTED.

Out: processed/step7/bb_b/rule.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
SRC = ROOT / "processed" / "step7" / "alt2_b"       # this instance's own prior stage
OUT = ROOT / "processed" / "step7" / "bb_b"

BACKFILL_D, POSTDATE_D = 180.0, -30.0
WATERFALL = [201_900, 178_165, 155_131, 152_126, 128_099]   # Step 5 lines 1-5
W_ADOPTED, H = 108, 91
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]


def reassert_step5_waterfall() -> dict:
    """Recompute the Step 5 waterfall and both population bases from source."""
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
    got = [int(x.sum()) for x in w]
    assert got == WATERFALL, (got, WATERFALL)
    return {
        "source": "processed/step5/pair_revision5.csv, recomputed here",
        "pair_table_rows": int(len(p)),
        "measured": got,
        "expected": WATERFALL,
        "asserted": True,
        "line1_APPLY_base_before_D10": got[0],
        "line4_DERIV_base_before_D10": got[3],
        # the ordered (user, show) keys of line 1 and of line 4, for the population check
        "_keys": (p.loc[w[0], ["user_idx", "show_trakt_id"]].values,
                  w[3][w[0]]),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()

    res: dict = {
        "instance": "data-scientist-b", "namespace": "bb_b", "stage": 1,
        "api_calls": 0, "adopts": "nothing",
        "gate": "Step 7 is a GATE. This artifact is a proposal. Nothing here is adopted.",
        "rule": ("NOT LIVE iff (no insertion instant after tau1) AND (NOT Continued). "
                 "Continued = |A| >= 1 AND F2 in A_H AND |A_H| >= ceil(0.90 x L2), read at tau2."),
        "rule_source": "decisions/0048 Sec 1; task-sheet.md Step 7",
        "W_adopted": W_ADOPTED, "H": H, "W_arms": W_ARMS,
        "populations": {
            "DERIV": "Step 5 line 4 (152,126) less D10 = 147,370 at W = 108. Requires S2 evidence.",
            "APPLY": "Step 5 line 1 (201,900) less D10 = 196,654 at W = 108. Step 8 position 6.",
        },
    }

    wf = reassert_step5_waterfall()
    keys_line1, line4_of_line1 = wf.pop("_keys")
    res["step5_waterfall_reasserted"] = wf
    print(f"step 5 waterfall re-asserted {wf['measured']}  ({time.time() - t:.1f}s)", flush=True)

    pz = np.load(SRC / "pairs.npz")
    oz = np.load(SRC / "outcomes.npz")

    # --- the reused inputs are checked against the freshly recomputed waterfall ---
    assert len(pz["user_idx"]) == 201_900
    assert np.array_equal(pz["user_idx"], keys_line1[:, 0])
    assert np.array_equal(pz["show_trakt_id"], keys_line1[:, 1])
    assert np.array_equal(pz["in_line4"], line4_of_line1)
    assert int(pz["in_line4"].sum()) == 152_126
    res["reused_inputs"] = {
        "from": "processed/step7/alt2_b/{pairs,outcomes}.npz -- this instance's ALT rerun",
        "what": ("conjunct (a) per arm (no_after_W*), D10 per arm (d10_W*), the line-4 flag, "
                 "and the outcome assignment per arm (started_/cont_/sal_W*)"),
        "why_valid": ("none of these is the rule; 0048 changed conjunct (b) only, and the "
                      "outcome assignment it now reads was already computed at every arm"),
        "checked": ("row order and identity of all 201,900 line-1 pairs, and the line-4 flag, "
                    "re-derived from pair_revision5.csv and compared element-wise"),
        "calibration": "READ, NEVER REFITTED -- processed/step5/calibration.npz, 10,918 knots",
    }
    print(f"reused inputs verified against source  ({time.time() - t:.1f}s)", flush=True)

    in_line4_all = pz["in_line4"]
    uidx_all = pz["user_idx"]
    any_rec = oz["has_any_s2_record_anywhere"]

    by_pop: dict = {}
    for popname in ("DERIV", "APPLY"):
        per_arm = {}
        for W in W_ARMS:
            d10 = pz[f"d10_W{W}"]
            base = (d10 & in_line4_all) if popname == "DERIV" else d10
            n = int(base.sum())
            started = oz[f"started_W{W}"][base]
            cont = oz[f"cont_W{W}"][base].astype(bool)
            sal = oz[f"sal_W{W}"][base].astype(bool)
            ns = ~started
            noaft = pz[f"no_after_W{W}"][base]
            uidx = uidx_all[base]
            assert int(ns.sum() + cont.sum() + sal.sum()) == n, "states do not partition"

            notlive = noaft & ~cont            # THE ADOPTED RULE
            live = ~notlive
            ex = int(notlive.sum())
            ex_ns = int((notlive & ns).sum())
            ex_sl = int((notlive & sal).sum())
            ex_c = int((notlive & cont).sum())
            assert ex_c == 0, "a Continued pair was excluded -- conjunct (b) is misread"
            assert ex_ns + ex_sl == ex

            n_live = int(live.sum())
            ns_live = int((ns & live).sum())
            c_live = int((cont & live).sum())
            sl_live = int((sal & live).sum())
            assert ns_live + c_live + sl_live == n_live
            ns_tot, c_tot, sl_tot = int(ns.sum()), int(cont.sum()), int(sal.sum())
            assert c_live == c_tot                      # no Continued pair is ever excluded

            # ---------------- bounds, ONE denominator, n = n (position-5 population) ----
            # The excluded pairs' true state is unknown, subject to what is OBSERVED:
            #   the ex_ns pairs have |A| = 0 observed-as-null  -> true state in {NS, SL, C}
            #   the ex_sl pairs have |A| >= 1 DIRECTLY OBSERVED -> true state in {SL, C} only
            ns_floor = 100.0 * (ns_tot - ex_ns) / n     # every NS-excluded pair really started
            ns_ceil = 100.0 * ns_tot / n                # every NS-excluded pair really never started
            sl_floor = 100.0 * (sl_tot - ex_sl) / n     # every excluded pair really continued
            sl_ceil_over_sl_ex = 100.0 * sl_tot / n     # the ex_sl really left; ex_ns not SL
            sl_ceil_joint = 100.0 * (sl_tot + ex_ns) / n  # ex_sl really left AND every ex_ns is SL
            c_floor = 100.0 * c_tot / n
            c_ceil = 100.0 * (c_tot + ex) / n

            per_arm[str(W)] = {
                "W": W, "population": popname,
                "n_before_liveness": n,
                "accounts_before_liveness": int(len(np.unique(uidx))),
                # ---- exclusions
                "excluded_pairs": ex,
                "excluded_never_started": ex_ns,
                "excluded_started_and_left": ex_sl,
                "excluded_continued": ex_c,
                "excluded_share_of_population_pct": 100.0 * ex / n,
                "accounts_supplying_exclusions": int(len(np.unique(uidx[notlive]))) if ex else 0,
                "accounts_supplying_NS_exclusions":
                    int(len(np.unique(uidx[notlive & ns]))) if ex_ns else 0,
                "accounts_supplying_SL_exclusions":
                    int(len(np.unique(uidx[notlive & sal]))) if ex_sl else 0,
                "conjunct_a_alone_would_exclude": int(noaft.sum()),
                "conjunct_b_alone_would_exclude": int((~cont).sum()),
                "excluded_with_no_S2_record_anywhere": int((notlive & ~any_rec[base]).sum()),
                "excluded_with_an_S2_record_somewhere": int((notlive & any_rec[base]).sum()),
                # ---- shares
                "no_filter": {
                    "n": n, "never_started": ns_tot, "continued": c_tot,
                    "started_and_left": sl_tot,
                    "never_started_pct": 100.0 * ns_tot / n,
                    "continued_pct": 100.0 * c_tot / n,
                    "started_and_left_pct": 100.0 * sl_tot / n},
                "under_rule": {
                    "n": n_live, "never_started": ns_live, "continued": c_live,
                    "started_and_left": sl_live,
                    "never_started_pct": 100.0 * ns_live / n_live,
                    "continued_pct": 100.0 * c_live / n_live,
                    "started_and_left_pct": 100.0 * sl_live / n_live},
                "delta_vs_no_filter_pp": {
                    "never_started": 100.0 * ns_live / n_live - 100.0 * ns_tot / n,
                    "continued": 100.0 * c_live / n_live - 100.0 * c_tot / n,
                    "started_and_left": 100.0 * sl_live / n_live - 100.0 * sl_tot / n},
                # ---- bounds
                "never_started_bound": {
                    "estimand": "never-started share of the position-5 population",
                    "denominator": n,
                    "floor_pct": ns_floor, "ceiling_pct": ns_ceil,
                    "width_pp": ns_ceil - ns_floor,
                    "floor_numerator": ns_tot - ex_ns, "ceiling_numerator": ns_tot,
                    "ceiling_equals_unfiltered_share_identity":
                        bool(ns_ceil == 100.0 * ns_tot / n),
                    "spanned_by": "the NS liveness exclusions only",
                    "complete": ("yes -- the started-and-left exclusions have |A| >= 1 DIRECTLY "
                                 "OBSERVED, so they cannot be never-started under any reading "
                                 "and move neither endpoint"),
                },
                "started_and_left_bound": {
                    "estimand": "started-and-left share of the position-5 population",
                    "denominator": n,
                    "floor_pct": sl_floor,
                    "ceiling_over_SL_exclusions_pct": sl_ceil_over_sl_ex,
                    "width_over_SL_exclusions_pp": sl_ceil_over_sl_ex - sl_floor,
                    "ceiling_joint_pct": sl_ceil_joint,
                    "width_joint_pp": sl_ceil_joint - sl_floor,
                    "floor_numerator": sl_tot - ex_sl,
                    "ceiling_over_SL_exclusions_numerator": sl_tot,
                    "ceiling_joint_numerator": sl_tot + ex_ns,
                    "ceiling_over_SL_exclusions_equals_unfiltered_share_identity":
                        bool(sl_ceil_over_sl_ex == 100.0 * sl_tot / n),
                },
                "continued_bound": {
                    "estimand": "continued share of the position-5 population",
                    "denominator": n,
                    "floor_pct": c_floor, "ceiling_pct": c_ceil,
                    "width_pp": c_ceil - c_floor,
                    "floor_equals_unfiltered_share_identity":
                        bool(c_floor == 100.0 * c_tot / n),
                },
            }
        by_pop[popname] = per_arm
    res["by_population"] = by_pop

    # ---------------- population assertions at the adopted W ----------------
    assert by_pop["APPLY"]["108"]["n_before_liveness"] == 196_654
    assert by_pop["DERIV"]["108"]["n_before_liveness"] == 147_370
    res["populations_asserted_at_W108"] = {"APPLY": 196_654, "DERIV": 147_370}

    # ---------------- claims from 0048 / task sheet, confirmed or refuted --------------
    a108, d108 = by_pop["APPLY"]["108"], by_pop["DERIV"]["108"]
    res["claims_tested"] = {
        "prior_measurement_DERIV_99_from_73_accounts": {
            "claimed": {"excluded": 99, "accounts": 73},
            "measured": {"excluded": d108["excluded_pairs"],
                         "accounts": d108["accounts_supplying_exclusions"]},
            "verdict": "CONFIRMED" if (d108["excluded_pairs"] == 99 and
                                       d108["accounts_supplying_exclusions"] == 73) else "REFUTED",
        },
        "prior_measurement_APPLY_703_from_216_accounts": {
            "claimed": {"excluded": 703, "accounts": 216, "split": [604, 99]},
            "measured": {"excluded": a108["excluded_pairs"],
                         "accounts": a108["accounts_supplying_exclusions"],
                         "split": [a108["excluded_never_started"],
                                   a108["excluded_started_and_left"]]},
            "verdict": "CONFIRMED" if (a108["excluded_pairs"] == 703 and
                                       a108["accounts_supplying_exclusions"] == 216 and
                                       a108["excluded_never_started"] == 604 and
                                       a108["excluded_started_and_left"] == 99) else "REFUTED",
        },
        "0048_per_arm_APPLY": {
            "claimed": [537, 550, 633, 664, 701, 703, 789, 864],
            "measured": [by_pop["APPLY"][str(W)]["excluded_pairs"] for W in W_ARMS],
        },
        "0048_per_arm_SL_component": {
            "claimed": [52, 56, 79, 89, 98, 99, 125, 148],
            "claimed_population_stated_in_0048": "not stated at the point of use (0046 Sec 0)",
            "measured_APPLY": [by_pop["APPLY"][str(W)]["excluded_started_and_left"]
                               for W in W_ARMS],
            "measured_DERIV": [by_pop["DERIV"][str(W)]["excluded_started_and_left"]
                               for W in W_ARMS],
        },
        "never_started_bound_unchanged_from_ALT": {
            "ALT_published_0047": [16.6633, 16.9704],
            "ALT_BROAD_measured_APPLY_W108": [a108["never_started_bound"]["floor_pct"],
                                              a108["never_started_bound"]["ceiling_pct"]],
            "ALT_BROAD_denominator": a108["never_started_bound"]["denominator"],
        },
        "DERIV_NS_exclusion_component_is_zero_at_every_arm": {
            W: by_pop["DERIV"][str(W)]["excluded_never_started"] for W in W_ARMS},
        "APPLY_W_coupling_factor": {
            "total": by_pop["APPLY"]["213"]["excluded_pairs"] /
                     by_pop["APPLY"]["38"]["excluded_pairs"],
            "NS_component": by_pop["APPLY"]["213"]["excluded_never_started"] /
                            by_pop["APPLY"]["38"]["excluded_never_started"],
            "SL_component": by_pop["APPLY"]["213"]["excluded_started_and_left"] /
                            by_pop["APPLY"]["38"]["excluded_started_and_left"],
        },
    }

    res["elapsed_s"] = time.time() - t
    (OUT / "rule.json").write_text(json.dumps(res, indent=2))

    for pop in ("DERIV", "APPLY"):
        a = by_pop[pop]["108"]
        print(f"\n=== {pop}  W=108  n={a['n_before_liveness']:,}")
        print(f"  excluded {a['excluded_pairs']:,} from {a['accounts_supplying_exclusions']} "
              f"accounts = {a['excluded_never_started']} NS + "
              f"{a['excluded_started_and_left']} SL")
        print(f"  no filter : NS {a['no_filter']['never_started_pct']:.4f}  "
              f"C {a['no_filter']['continued_pct']:.4f}  "
              f"SL {a['no_filter']['started_and_left_pct']:.4f}")
        print(f"  under rule: NS {a['under_rule']['never_started_pct']:.4f}  "
              f"C {a['under_rule']['continued_pct']:.4f}  "
              f"SL {a['under_rule']['started_and_left_pct']:.4f}")
        print(f"  NS bound [{a['never_started_bound']['floor_pct']:.4f}, "
              f"{a['never_started_bound']['ceiling_pct']:.4f}] on "
              f"{a['never_started_bound']['denominator']:,}")
        print(f"  SL bound [{a['started_and_left_bound']['floor_pct']:.4f}, "
              f"{a['started_and_left_bound']['ceiling_over_SL_exclusions_pct']:.4f}] "
              f"(joint ceiling {a['started_and_left_bound']['ceiling_joint_pct']:.4f})")
    print(f"\n({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
