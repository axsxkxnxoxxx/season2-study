"""Step 7 VERIFICATION, namespace `a` -- the DERIV started-and-left floor and Continued ceiling.

specs/step7-deriv-floor-verification.md. This REPRODUCES or REFUTES a correction proposed by
the Human Lead (decisions/0055). Nothing proposed is hardcoded and nothing is asserted against
a target: every figure is computed from instance a's own stored W = 108 ALT-BROAD outputs
(processed/step7/bb_a/masks_W108.npz) and the comparison to the proposal is made afterwards,
in data, so a mismatch surfaces as a REFUTATION rather than as an AssertionError.

That distinction is the whole point of the assignment. src/step7_floor_extremes.py -- the
script the proposal was computed with -- reads the same masks but carries
    assert d["floor_extreme_ALL_continued"]["count"] == 16655
so it cannot report a refutation; it can only crash. It is not read here.

THE RULE IS UNCHANGED -- ALT-BROAD (0048, restored by 0054):
    NOT LIVE iff (no insertion instant after tau1) AND (NOT Continued),
silence anchored at tau1 and only at tau1.

Populations, both stated at every point of use:
    APPLY = Step 5 line 1 less D10  = what Step 8 filters
    DERIV = Step 5 line 4 less D10  = requires S2 evidence
Denominators are taken from the masks themselves, not asserted.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
MASKS = os.path.join(ROOT, "processed/step7/bb_a/masks_W108.npz")
OUT = os.path.join(ROOT, "processed/step7/df_a")

SEC_PER_DAY = 86400.0
W = 108
H = 91

PROPOSED = {
    "DERIV": {
        "channel_pairs": 89,
        "floor_ALL_count": 16655, "floor_ALL_pct": 11.3015,
        "floor_NONE_count": 16744, "floor_NONE_pct": 11.3619,
        "ceiling_count": 16843, "ceiling_pct": 11.4291,
        "continued_ceiling_ALL_count": 121570, "continued_ceiling_ALL_pct": 82.4930,
    }
}


def pct(x, n):
    return 100.0 * x / n


def main():
    os.makedirs(OUT, exist_ok=True)
    m = np.load(MASKS)

    user = m["user"]
    never, cont, left = m["never"], m["cont"], m["left"]
    nA = m["nA"]
    t0f, last = m["t0f"], m["last_inst"]
    stored_ex, stored_ex_ns, stored_ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    stored_no_after = m["no_after"]

    tau1 = t0f + W * SEC_PER_DAY
    tau2 = t0f + (W + H) * SEC_PER_DAY

    # ---- primitives rebuilt, not trusted -------------------------------------------------
    integrity = {
        "states_partition_the_rows": bool(
            (never.astype(np.int8) + cont.astype(np.int8) + left.astype(np.int8) == 1).all()),
        "never_is_|A|=0": bool((never == (nA == 0)).all()),
        "left_is_notContinued_and_|A|>=1": bool((left == (~cont & ~never)).all()),
        "no_after_rebuilt_matches_stored": bool((stored_no_after == (last <= tau1)).all()),
        "rule_rebuilt_matches_stored_ex": None,
        "ex_components_partition_ex": bool(((stored_ex_ns | stored_ex_sl) == stored_ex).all()),
        "no_Continued_pair_is_excluded": int((stored_ex & cont).sum()) == 0,
        "tau2_strictly_after_tau1": bool((tau2 > tau1).all()),
    }
    not_live = (~cont) & (last <= tau1)              # THE RULE, rebuilt
    integrity["rule_rebuilt_matches_stored_ex"] = bool((not_live == stored_ex).all())

    ex_ns = not_live & never
    ex_sl = not_live & left
    live = ~not_live

    # ---- the channel ---------------------------------------------------------------------
    # ¬Continued, |A| >= 1 (i.e. not never-started), last insertion inside (tau1, tau2].
    # These pairs are LIVE under ALT-BROAD only because they inserted after tau1, and they
    # could produce no evidence dated after that instant, so they may in truth be Continued.
    base = (~cont) & (~never) & (last > tau1)
    chan_halfopen = base & (last <= tau2)            # (tau1, tau2]  -- the spec's item 1
    chan_open = base & (last < tau2)                 # (tau1, tau2)  -- the spec's background
    # the same construction on the never-started rows, reported but never used in an endpoint
    chan_ns = (~cont) & never & (last > tau1) & (last <= tau2)

    POPS = {
        "APPLY": (m["apply_"], "Step 5 line 1 less D10 -- what Step 8 filters"),
        "DERIV": (m["deriv"], "Step 5 line 4 less D10 -- requires S2 evidence"),
    }

    results = {}
    for name, (msk, defn) in POPS.items():
        n = int(msk.sum())

        unf = {"never_started": int((msk & never).sum()),
               "continued": int((msk & cont).sum()),
               "started_and_left": int((msk & left).sum())}

        e_ns, e_sl = int((msk & ex_ns).sum()), int((msk & ex_sl).sum())
        e_tot = e_ns + e_sl

        ch = int((msk & chan_halfopen).sum())
        ch_open = int((msk & chan_open).sum())
        ch_at_tau2 = ch - ch_open
        ch_nsc = int((msk & chan_ns).sum())

        ret_sl = int((msk & live & left).sum())
        ret_cont = int((msk & live & cont).sum())
        ret_ns = int((msk & live & never).sum())

        # S&L floor. Exclusions contribute nothing to a floor -- they are removed and may in
        # truth be anything. Among the RETAINED S&L, the channel pairs may in truth be
        # Continued, so the covering floor concedes them.
        floor_none = ret_sl
        floor_all = ret_sl - ch

        # S&L ceiling. Every exclusion may in truth be S&L; the channel pairs are ALREADY
        # counted as S&L in it, so the widening cannot reach the ceiling.
        ceiling_none = ret_sl + e_tot
        ceiling_all = ret_sl + e_tot          # computed separately, then compared

        # Continued ceiling. Any EXCLUDED pair may in truth be Continued; under extreme ALL
        # the channel pairs may be too.
        cont_ceiling_none = ret_cont + e_tot
        cont_ceiling_all = ret_cont + e_tot + ch

        results[name] = {
            "population": name,
            "population_definition": defn,
            "n_pairs_denominator": n,
            "n_from_mask_not_asserted": True,
            "unfiltered_counts_on_this_population": unf,
            "exclusions_on_this_population": {
                "total": e_tot, "never_started_component": e_ns,
                "started_and_left_component": e_sl,
                "accounts": int(np.unique(user[msk & not_live]).size),
            },
            "retained_counts_on_this_population": {
                "never_started": ret_ns, "continued": ret_cont, "started_and_left": ret_sl},
            "channel": {
                "definition": "not Continued AND |A| >= 1 AND last insertion in (tau1, tau2]",
                "count_half_open_tau1_tau2_SPEC_ITEM_1": ch,
                "count_open_tau1_tau2_SPEC_BACKGROUND": ch_open,
                "pairs_with_last_insertion_exactly_at_tau2": ch_at_tau2,
                "definitions_agree": ch == ch_open,
                "never_started_analogue_not_used_in_any_endpoint": ch_nsc,
            },
            "started_and_left_floor": {
                "extreme_NONE_continued": {"count": floor_none, "pct": pct(floor_none, n)},
                "extreme_ALL_continued": {"count": floor_all, "pct": pct(floor_all, n)},
                "movement_pp": pct(floor_none, n) - pct(floor_all, n),
                "movement_pp_exact_as_channel_share": pct(ch, n),
            },
            "started_and_left_ceiling": {
                "extreme_NONE_continued": {"count": ceiling_none, "pct": pct(ceiling_none, n)},
                "extreme_ALL_continued": {"count": ceiling_all, "pct": pct(ceiling_all, n)},
                "moves_between_extremes": ceiling_none != ceiling_all,
                "movement_pp": pct(ceiling_none, n) - pct(ceiling_all, n),
            },
            "continued_ceiling": {
                "extreme_NONE_continued": {"count": cont_ceiling_none,
                                           "pct": pct(cont_ceiling_none, n)},
                "extreme_ALL_continued": {"count": cont_ceiling_all,
                                          "pct": pct(cont_ceiling_all, n)},
                "movement_pp": pct(cont_ceiling_all, n) - pct(cont_ceiling_none, n),
            },
            "never_started_bound_for_the_three_ceilings_check": {
                # the S&L exclusions have |A| >= 1 OBSERVED, so they cannot enter either
                # never-started endpoint: only the never-started exclusions can.
                "floor_count": ret_ns, "floor_pct": pct(ret_ns, n),
                "ceiling_count": ret_ns + e_ns, "ceiling_pct": pct(ret_ns + e_ns, n),
                "degenerate": e_ns == 0,
            },
            "arithmetic_identities_checked": {
                "retained_sl_plus_sl_exclusions_equals_unfiltered_sl":
                    ret_sl + e_sl == unf["started_and_left"],
                "retained_cont_equals_unfiltered_cont": ret_cont == unf["continued"],
                "floor_all_equals_floor_none_minus_channel":
                    floor_all == floor_none - ch,
                "three_ceilings_sum_count_extreme_ALL":
                    (ret_ns + e_ns) + ceiling_all + cont_ceiling_all,
                "three_ceilings_sum_pct_extreme_ALL": (
                    pct(ret_ns + e_ns, n) + pct(ceiling_all, n) + pct(cont_ceiling_all, n)),
                "three_ceilings_excess_pairs": (ret_ns + e_ns) + ceiling_all + cont_ceiling_all - n,
                "excess_decomposition_2xNS_plus_1xSL_plus_1xchannel":
                    2 * e_ns + e_sl + ch,
                "excess_decomposition_matches":
                    (ret_ns + e_ns) + ceiling_all + cont_ceiling_all - n == 2 * e_ns + e_sl + ch,
            },
        }

    # ---- the proposal, compared rather than assumed ---------------------------------------
    d = results["DERIV"]
    rows = [
        ("channel count", PROPOSED["DERIV"]["channel_pairs"],
         d["channel"]["count_half_open_tau1_tau2_SPEC_ITEM_1"], None, None),
        ("S&L floor, extreme ALL", PROPOSED["DERIV"]["floor_ALL_count"],
         d["started_and_left_floor"]["extreme_ALL_continued"]["count"],
         PROPOSED["DERIV"]["floor_ALL_pct"],
         d["started_and_left_floor"]["extreme_ALL_continued"]["pct"]),
        ("S&L floor, extreme NONE", PROPOSED["DERIV"]["floor_NONE_count"],
         d["started_and_left_floor"]["extreme_NONE_continued"]["count"],
         PROPOSED["DERIV"]["floor_NONE_pct"],
         d["started_and_left_floor"]["extreme_NONE_continued"]["pct"]),
        ("S&L ceiling", PROPOSED["DERIV"]["ceiling_count"],
         d["started_and_left_ceiling"]["extreme_ALL_continued"]["count"],
         PROPOSED["DERIV"]["ceiling_pct"],
         d["started_and_left_ceiling"]["extreme_ALL_continued"]["pct"]),
        ("Continued ceiling, extreme ALL", PROPOSED["DERIV"]["continued_ceiling_ALL_count"],
         d["continued_ceiling"]["extreme_ALL_continued"]["count"],
         PROPOSED["DERIV"]["continued_ceiling_ALL_pct"],
         d["continued_ceiling"]["extreme_ALL_continued"]["pct"]),
    ]
    verdicts = []
    for label, p_ct, o_ct, p_pc, o_pc in rows:
        ok = (p_ct == o_ct) and (p_pc is None or round(o_pc, 4) == p_pc)
        verdicts.append({
            "row": label, "population": "DERIV", "n": d["n_pairs_denominator"],
            "proposed_count": p_ct, "my_count": o_ct,
            "proposed_pct": p_pc, "my_pct": None if p_pc is None else round(o_pc, 6),
            "verdict": "CONFIRMED" if ok else "REFUTED",
        })

    out = {
        "step": 7, "task": "DERIV floor verification", "instance": "df_a",
        "namespace_letter": "a", "api_calls": 0,
        "spec": "specs/step7-deriv-floor-verification.md",
        "rule": "ALT-BROAD -- NOT LIVE iff (no insertion instant after tau1) AND (NOT Continued)",
        "silence_anchor": "tau1, and only tau1",
        "W": W, "H": H,
        "source_of_every_figure": "processed/step7/bb_a/masks_W108.npz (instance a's own W=108 "
                                  "ALT-BROAD run); nothing read from the other instance, nothing "
                                  "read from src/step7_floor_extremes.py or its output",
        "integrity_checks_on_the_stored_masks": integrity,
        "populations": results,
        "verdicts_on_the_proposed_DERIV_correction": verdicts,
        "all_rows_confirmed": all(v["verdict"] == "CONFIRMED" for v in verdicts),
    }

    with open(os.path.join(OUT, "floor_check.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    # ---- printed, both populations side by side ------------------------------------------
    print(f"integrity: {integrity}\n")
    hdr = (f"{'pop':6} {'n':>9} {'chan':>5} {'floorNONE':>17} {'floorALL':>17} "
           f"{'move pp':>8} {'S&L ceiling':>17} {'Cont ceilALL':>18}")
    print(hdr)
    for nm, r in results.items():
        f = r["started_and_left_floor"]
        c = r["started_and_left_ceiling"]["extreme_ALL_continued"]
        cc = r["continued_ceiling"]["extreme_ALL_continued"]
        print(f"{nm:6} {r['n_pairs_denominator']:>9,} "
              f"{r['channel']['count_half_open_tau1_tau2_SPEC_ITEM_1']:>5} "
              f"{f['extreme_NONE_continued']['count']:>7,} {f['extreme_NONE_continued']['pct']:>8.4f}% "
              f"{f['extreme_ALL_continued']['count']:>7,} {f['extreme_ALL_continued']['pct']:>8.4f}% "
              f"{f['movement_pp']:>8.4f} "
              f"{c['count']:>7,} {c['pct']:>8.4f}% "
              f"{cc['count']:>8,} {cc['pct']:>8.4f}%")
    print()
    for v in verdicts:
        print(f"{v['verdict']:10} {v['row']:34} proposed {str(v['proposed_count']):>8} "
              f"/ mine {str(v['my_count']):>8}   ({v['proposed_pct']} vs {v['my_pct']})")
    print(f"\nwrote {os.path.join(OUT, 'floor_check.json')}")


if __name__ == "__main__":
    main()
