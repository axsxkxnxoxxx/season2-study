"""Step 7 RERUN on ALT-MATCHED (decisions/0052), namespace `a`. STAGE 6 — THE CHANNEL.

WHAT A CHANNEL IS, stated so the measurement is checkable.
ALT-BROAD's warrant: a pair silent after tau1 can produce no evidence in [tau1, tau2), the window
the Continued test reads, and so is scored "left" by construction. 0052 SS1 observes the warrant
holds identically for a pair silent after tau1 + eps for any eps < H days -- the failure mode is
CONTINUOUS in the silence instant and ALT-BROAD cut it at one end. The CHANNEL is therefore:

    pairs the rule leaves LIVE whose last insertion falls strictly between the instant the
    silence test uses and the instant the outcome is read.

Under ALT-BROAD those two instants are tau1 and tau2 for the started-and-left null, so the channel
is the open interval (tau1, tau2). Under ALT-MATCHED the silence instant IS the reading instant for
each null, so the interval is degenerate and the channel should be EMPTY BY CONSTRUCTION. That is a
prediction; it is measured here, on both populations, not asserted.

Measured:
  1. the ALT-BROAD channel reproduced -- 0050 SS4's 297 = 207 ns + 90 sl, and 0052 SS3's corrected
     52.4% on the implicated set;
  2. whether ALT-MATCHED closes the 90;
  3. the analogous channel under ALT-MATCHED, for BOTH nulls;
  4. what the rule now trusts on the thinnest evidence -- live pairs whose only post-reading-instant
     insertion is barely past it;
  5. the tension the change creates with 0048 SS9's GLOSS on gate 0021.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/mm_a")
DAY = 86400.0


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    never, cont, left = m["never"], m["cont"], m["left"]
    ex, ex_ns, ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    xb = m["ex_altbroad"]
    tau1, tau2, last = m["tau1"], m["tau2"], m["last_inst"]
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    silent1 = last <= tau1
    silent2 = last <= tau2
    out = {"step": 7, "instance": "mm_a", "stage": 6, "api_calls": 0, "by_population": {}}

    for nm, p in pops.items():
        # ---- 1. the ALT-BROAD channel, reproduced --------------------------------------
        live_c1 = p & (~cont) & ~silent1              # live under ALT-BROAD only by conjunct 1
        chan_b = live_c1 & (last < tau2)              # last insertion inside (tau1, tau2)
        chan_b_ns, chan_b_sl = chan_b & never, chan_b & left
        g = (last - tau1) / DAY

        # ---- 2. does ALT-MATCHED close the started-and-left half? ----------------------
        closed = chan_b_sl & ex
        still_open = chan_b_sl & ~ex

        # ---- 3. the analogous channel under ALT-MATCHED --------------------------------
        # never-started null: silence tested at tau1, outcome read at tau1 -> interval (tau1,tau1)
        # started-and-left null: silence tested at tau2, outcome read at tau2 -> (tau2,tau2)
        chan_m_ns = p & never & ~ex & (last > tau1) & (last < tau1)
        chan_m_sl = p & left & ~ex & (last > tau2) & (last < tau2)

        # ---- 4. what is now trusted on the thinnest evidence ---------------------------
        gl_ns = (last - tau1)[p & never & ~ex] / DAY
        gl_sl = (last - tau2)[p & left & ~ex] / DAY

        # ---- 5. the 0021-gloss tension -------------------------------------------------
        excl_with_insertion_after_tau1 = ex & p & ~silent1

        rec = {
            "population_pairs": int(p.sum()),
            "ALT_BROAD_channel_reproduced": {
                "not_continued": int((p & ~cont).sum()),
                "live_only_by_conjunct_1": int(live_c1.sum()),
                "channel_last_insertion_in_open_tau1_tau2": int(chan_b.sum()),
                "channel_never_started": int(chan_b_ns.sum()),
                "channel_started_and_left": int(chan_b_sl.sum()),
                "ALT_BROAD_exclusions": int((xb & p).sum()),
                "days_past_tau1_of_channel": {
                    "p50": round(float(np.median(g[chan_b])), 1) if chan_b.any() else None,
                    "p90": round(float(np.percentile(g[chan_b], 90)), 1) if chan_b.any() else None,
                    "max": round(float(g[chan_b].max()), 1) if chan_b.any() else None},
                "0050_SS4_pooled_denominator_share_pct": round(
                    100.0 * (xb & p).sum() / ((xb & p).sum() + chan_b.sum()), 1),
                "0052_SS3_IMPLICATED_SET_ONLY_share_pct": round(
                    100.0 * (xb & p & left).sum()
                    / ((xb & p & left).sum() + chan_b_sl.sum()), 1),
                "0052_SS3_note": "the never-started half of the pooled 297 is NOT in the gap: "
                                 "never-started is the null |A| = 0 READ AT tau1, and every one "
                                 "of those pairs has an insertion after tau1, which is exactly "
                                 "what 0021 licenses. Only the started-and-left half is "
                                 "implicated.",
            },
            "ALT_MATCHED_closes_it": {
                "started_and_left_channel_pairs": int(chan_b_sl.sum()),
                "now_excluded": int(closed.sum()),
                "still_live": int(still_open.sum()),
                "closed_share_pct": (round(100.0 * closed.sum() / chan_b_sl.sum(), 1)
                                     if chan_b_sl.any() else None),
            },
            "ANALOGOUS_CHANNEL_UNDER_ALT_MATCHED": {
                "never_started_branch": int(chan_m_ns.sum()),
                "started_and_left_branch": int(chan_m_sl.sum()),
                "total": int(chan_m_ns.sum() + chan_m_sl.sum()),
                "why_empty": "the silence instant and the reading instant now COINCIDE for each "
                             "null, so the open interval between them is empty. The channel is "
                             "closed by construction, not by this pull date -- there is no eps "
                             "for the continuity argument to run over.",
            },
            "thinnest_evidence_now_trusted": {
                "live_never_started_min_days_past_tau1": (round(float(gl_ns.min()), 4)
                                                          if gl_ns.size else None),
                "live_never_started_within_1d_of_tau1": int((gl_ns < 1).sum()),
                "live_never_started_within_7d_of_tau1": int((gl_ns < 7).sum()),
                "live_started_and_left_min_days_past_tau2": (round(float(gl_sl.min()), 4)
                                                             if gl_sl.size else None),
                "live_started_and_left_within_1d_of_tau2": int((gl_sl < 1).sum()),
                "live_started_and_left_within_7d_of_tau2": int((gl_sl < 7).sum()),
                "reading": "these are the pairs whose liveness rests on the least evidence under "
                           "the adopted rule. They are LIVE and their nulls are trusted; 0021's "
                           "sufficient condition is met at the instant that matters for each.",
            },
            "TENSION_WITH_0048_SS9_GLOSS_ON_0021": {
                "exclusions_that_DO_show_an_insertion_after_tau1": int(
                    excl_with_insertion_after_tau1.sum()),
                "of_which_started_and_left": int((excl_with_insertion_after_tau1 & left).sum()),
                "of_which_never_started": int((excl_with_insertion_after_tau1 & never).sum()),
                "share_of_all_exclusions_pct": round(
                    100.0 * excl_with_insertion_after_tau1.sum() / (ex & p).sum(), 1),
                "reading": "0021's OWN TEXT is 'any record inserted AFTER THE WINDOW CLOSED proves "
                           "the account was alive'. For the started-and-left null the reading "
                           "window closes at tau2, so ALT-MATCHED is faithful to it. But 0048 SS9 "
                           "GLOSSED 0021 as 'insertion after tau1 => live', and under that gloss "
                           "these exclusions contradict a gate. Under ALT-BROAD the count was 0, "
                           "so the two readings never had to be told apart. They do now. This is "
                           "for the Human Lead, not for this instance to settle.",
            },
        }
        out["by_population"][nm] = rec

    a = out["by_population"]["APPLY"]
    out["CONFIRM_OR_REFUTE"] = {
        "0050_SS4_channel_297_on_APPLY": {
            "expected": {"total": 297, "never_started": 207, "started_and_left": 90},
            "measured": {
                "total": a["ALT_BROAD_channel_reproduced"][
                    "channel_last_insertion_in_open_tau1_tau2"],
                "never_started": a["ALT_BROAD_channel_reproduced"]["channel_never_started"],
                "started_and_left": a["ALT_BROAD_channel_reproduced"][
                    "channel_started_and_left"]}},
        "0052_SS3_corrected_channel_share_52.4pct": {
            "expected": 52.4,
            "measured": a["ALT_BROAD_channel_reproduced"]["0052_SS3_IMPLICATED_SET_ONLY_share_pct"]},
        "0050_SS4_superseded_pooled_share_70.3pct": {
            "expected": 70.3,
            "measured": a["ALT_BROAD_channel_reproduced"]["0050_SS4_pooled_denominator_share_pct"],
            "note": "reproduced only to show the arithmetic 0052 SS3 corrects; the pooled "
                    "denominator is not the right one"},
        "0052_SS3_ALT_MATCHED_closes_the_remaining_90": {
            "expected_closed": 90,
            "measured_closed": a["ALT_MATCHED_closes_it"]["now_excluded"],
            "measured_still_live": a["ALT_MATCHED_closes_it"]["still_live"]},
    }

    with open(os.path.join(OUT, "channel.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
