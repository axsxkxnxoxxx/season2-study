"""Step 7 rerun on ALT-MATCHED (instance b, namespace mm_b) -- stage 4.

(A) The filter waterfall, line 6 outcome-conditional, with monotone decrease
    reported strict / non-strict per population and per arm.

(B) THE CHANNEL. 0052 Sec 3 records that ALT-BROAD left 90 started-and-left
    pairs whose LAST insertion fell inside (tau1, tau2). Two questions, both
    measured, neither assumed:
      1. does ALT-MATCHED close those 90?
      2. does any ANALOGOUS channel remain under ALT-MATCHED?

    The channel's definition, generalised from 0050 Sec 4 / 0052 Sec 3:
      a pair that is LIVE ONLY because of the silence conjunct -- i.e. its
      outcome null holds, but the account inserted after the silence instant --
      AND whose LAST insertion falls strictly before the instant at which that
      pair's outcome is READ. Such a pair can produce no evidence in the
      remainder of the window the outcome test reads, so it is scored by
      construction rather than by observation.

    Under ALT-BROAD the silence instant is tau1 for both nulls while the S&L
    outcome is read at tau2, so the window (tau1, tau2) is 91 days wide and the
    channel is non-empty. Under ALT-MATCHED the silence instant EQUALS the read
    instant for each null, so the window is empty. That is measured, not
    asserted, and the near-boundary distribution is reported alongside so the
    closure is not confused with a claim that no pair sits near the boundary.

ZERO network calls.
Out: processed/step7/mm_b/waterfall.json, processed/step7/mm_b/channel.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "mm_b"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
W, H, DAY = 108, 91, 86400.0
QS = (0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100)


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    in4 = pz["in_line4"]
    t0 = pz["t0_midnight_epoch"].astype(np.float64)
    mx = pz["max_inst_pair"]

    # ------------------------------------------------------------------ (A)
    wf: dict = {
        "instance": "data-scientist-b", "namespace": "mm_b", "stage": "4A",
        "api_calls": 0, "adopts": "nothing", "rule_name": "ALT-MATCHED",
        "positions_1_2": "belong to Step 8 and are not rebuilt here",
        "L2_eq_1_pairs_in_this_frame": int((pz["L2"] == 1).sum()),
        "line6_is_OUTCOME_CONDITIONAL": (
            "Both nulls are read before liveness is applied. Permitted on 0046 Sec 5's "
            "reasoning: the outcome predicate and the liveness predicate are row-local on the "
            "position-5 output and commute exactly, and 0029's ordering rationale concerns "
            "per-filter sample size, which cannot reach position 7 because outcome assignment "
            "removes no rows. Under ALT-MATCHED line 6 is conditional at BOTH instants: branch "
            "(i) reads |A| = 0 at tau1, branch (ii) reads NOT Continued at tau2."),
        "by_population": {},
    }
    for pop in ("DERIV", "APPLY"):
        arms = {}
        for Wa in W_ARMS:
            d10 = pz[f"d10_W{Wa}"]
            base = (d10 & in4) if pop == "DERIV" else d10
            n = int(base.sum())
            ns = ~oz[f"started_W{Wa}"][base]
            sal = oz[f"sal_W{Wa}"][base].astype(bool)
            sil1, sil2 = pz[f"no_after_tau1_W{Wa}"][base], pz[f"no_after_tau2_W{Wa}"][base]
            notlive = (ns & sil1) | (sal & sil2)
            ex = int(notlive.sum())
            # commutation check, coded not assumed: the row set is identical whether the
            # outcome annotation or the liveness predicate is evaluated first.
            order_a = np.nonzero(base)[0][~notlive]
            m = np.zeros(len(in4), dtype=bool)
            m[np.nonzero(base)[0]] = notlive
            order_b = np.nonzero(base & ~m)[0]
            assert np.array_equal(order_a, order_b), "the two predicates do not commute"
            arms[str(Wa)] = {
                "W": Wa, "position5_in": n, "position6_out": n - ex,
                "removed": ex,
                "removed_never_started_branch_i": int((ns & sil1).sum()),
                "removed_started_and_left_branch_ii": int((sal & sil2).sum()),
                "removed_continued": 0,
                "position7_out": n - ex,
                "position7_removes": 0,
                "monotone_decrease_at_line6": "STRICT" if ex > 0 else "NON-STRICT",
                "commutation_checked": True,
            }
        wf["by_population"][pop] = arms
    wf["monotone_summary"] = {
        pop: {"strict_at_every_arm":
              all(v["monotone_decrease_at_line6"] == "STRICT" for v in wf["by_population"][pop].values()),
              "removed_per_arm": [wf["by_population"][pop][str(x)]["removed"] for x in W_ARMS]}
        for pop in ("DERIV", "APPLY")}
    wf["ge_coding_note"] = (
        "Decrease is STRICT on both populations at every tested arm, so `>=` is not needed for "
        "THIS rule. It is kept at Step 8 because the invariant must not encode a property of one "
        "rule -- a filter position that legitimately removes nothing must not fail an assertion.")
    (OUT / "waterfall.json").write_text(json.dumps(wf, indent=2))
    print("waterfall written", flush=True)

    # ------------------------------------------------------------------ (B)
    ch: dict = {
        "instance": "data-scientist-b", "namespace": "mm_b", "stage": "4B",
        "api_calls": 0, "adopts": "nothing", "W": W, "H": H,
        "channel_definition": (
            "LIVE only by the silence conjunct, AND last insertion strictly before the instant "
            "at which that pair's own outcome is read. Such a pair can produce no evidence in the "
            "remainder of the read window, so it is scored by construction."),
        "by_population": {},
    }
    for pop in ("DERIV", "APPLY"):
        d10 = pz[f"d10_W{W}"]
        base = (d10 & in4) if pop == "DERIV" else d10
        n = int(base.sum())
        cont = oz[f"cont_W{W}"][base].astype(bool)
        sal = oz[f"sal_W{W}"][base].astype(bool)
        ns = ~oz[f"started_W{W}"][base]
        sil1, sil2 = pz[f"no_after_tau1_W{W}"][base], pz[f"no_after_tau2_W{W}"][base]
        tau1, tau2, m = t0[base] + W * DAY, t0[base] + (W + H) * DAY, mx[base]

        # ---- reproduce ALT-BROAD's channel exactly, as a basis check (0050 Sec 4) ----
        nl_broad = sil1 & ~cont
        live_only_by_sil_broad = (~sil1) & (~cont)
        in_gap_broad = live_only_by_sil_broad & (m < tau2)
        ch_broad = {
            "not_continued": int((~cont).sum()),
            "live_only_by_the_silence_conjunct": int(live_only_by_sil_broad.sum()),
            "channel_last_insertion_inside_tau1_tau2": int(in_gap_broad.sum()),
            "channel_never_started": int((in_gap_broad & ns).sum()),
            "channel_started_and_left": int((in_gap_broad & sal).sum()),
            "ALT_BROAD_exclusions": int(nl_broad.sum()),
            "0050_claimed_on_APPLY": {"not_continued": 52514, "live_only": 51811,
                                      "channel": 297, "ns": 207, "sl": 90, "excl": 703},
        }
        if int(in_gap_broad.sum()):
            g = (m[in_gap_broad] - tau1[in_gap_broad]) / DAY
            ch_broad["last_insertion_days_past_tau1"] = {
                f"p{q}": float(np.percentile(g, q)) for q in QS}

        # ---- does ALT-MATCHED close the started-and-left half of it? ----
        notlive = (ns & sil1) | (sal & sil2)
        gap_sl = in_gap_broad & sal
        gap_ns = in_gap_broad & ns
        closed_sl = int((gap_sl & notlive).sum())
        closed_ns = int((gap_ns & notlive).sum())
        new_sl = (sal & sil2) & ~(sal & sil1)          # S&L pairs ALT-MATCHED adds
        ch_matched_close = {
            "ALT_BROAD_channel_started_and_left": int(gap_sl.sum()),
            "of_those_now_EXCLUDED_by_ALT_MATCHED": closed_sl,
            "closure_rate_pct": (100.0 * closed_sl / int(gap_sl.sum())) if int(gap_sl.sum()) else None,
            "ALT_BROAD_channel_never_started": int(gap_ns.sum()),
            "of_those_now_excluded": closed_ns,
            "never_started_channel_reading": (
                "the never-started pairs in ALT-BROAD's channel are NOT in the gap and are not "
                "expected to close: never-started is the null |A| = 0 READ AT tau1, and every one "
                "of them has an insertion after tau1 -- exactly the evidence 0021 licenses. "
                "(0052 Sec 3, which is why the closure denominator is the S&L set alone.)"),
            "started_and_left_pairs_ALT_MATCHED_newly_excludes": int(new_sl.sum()),
            "are_they_exactly_the_channel_S_and_L_set": bool(
                np.array_equal(np.nonzero(new_sl)[0], np.nonzero(gap_sl)[0])),
        }

        # ---- does ANY analogous channel remain under ALT-MATCHED? ----
        # branch (i): NS pairs live only by silence -> window (tau1, tau1), empty by construction
        # branch (ii): S&L pairs live only by silence -> window (tau2, tau2), empty by construction
        live_only_i = ns & ~sil1
        live_only_ii = sal & ~sil2
        rem_i = live_only_i & (m < tau1)
        rem_ii = live_only_ii & (m < tau2)
        margin_i = (m[live_only_i] - tau1[live_only_i]) / DAY
        margin_ii = (m[live_only_ii] - tau2[live_only_ii]) / DAY
        ch_remaining = {
            "branch_i_never_started_live_only_by_silence": int(live_only_i.sum()),
            "branch_i_residual_channel": int(rem_i.sum()),
            "branch_ii_started_and_left_live_only_by_silence": int(live_only_ii.sum()),
            "branch_ii_residual_channel": int(rem_ii.sum()),
            "mechanism": (
                "ZERO by construction, and that is the point of the rule change. The channel is "
                "the interval between the silence instant and the read instant; ALT-MATCHED makes "
                "them the same instant for each null, so the interval is empty. There is no "
                "epsilon left to slide along."),
            "near_boundary_branch_i_days_past_tau1": {
                f"p{q}": float(np.percentile(margin_i, q)) for q in QS},
            "near_boundary_branch_ii_days_past_tau2": {
                f"p{q}": float(np.percentile(margin_ii, q)) for q in QS},
            "branch_i_within_1_day_of_flipping": int((margin_i <= 1).sum()),
            "branch_i_within_7_days": int((margin_i <= 7).sum()),
            "branch_i_within_30_days": int((margin_i <= 30).sum()),
            "branch_ii_within_1_day_of_flipping": int((margin_ii <= 1).sum()),
            "branch_ii_within_7_days": int((margin_ii <= 7).sum()),
            "branch_ii_within_30_days": int((margin_ii <= 30).sum()),
            "what_this_does_NOT_close": (
                "the biconditional gap. 0021 licenses 'insertion after the instant => live' as a "
                "SUFFICIENT condition; the rule also asserts the converse. ALT-MATCHED narrows "
                "nothing about that and it stays a Step 14 limitation."),
        }
        ch["by_population"][pop] = {
            "n": n,
            "ALT_BROAD_channel_reproduced": ch_broad,
            "ALT_MATCHED_closure": ch_matched_close,
            "ALT_MATCHED_residual_channel": ch_remaining,
        }
    ch["elapsed_s"] = time.time() - t
    (OUT / "channel.json").write_text(json.dumps(ch, indent=2))
    print(json.dumps(ch["by_population"]["APPLY"], indent=2)[:4000])
    print(f"({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
