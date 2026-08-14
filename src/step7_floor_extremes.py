"""The started-and-left floor under both extremes, on both populations.

Human Lead ruling, 2026-08-13: 0054 §3 grounded the widened floor on a margin
statistic -- p5 = 1.7 days, min 0.13 -- which is the tail. The record's median
for the same 90 pairs is 44.5 days (0053 §5, instance B). The tail was cherry
-picked, so the ground is recomputed here from the endpoints themselves:

  extreme A -- NONE of the channel pairs is in truth Continued
  extreme B -- ALL of them are

If the endpoint does not move between the two, the margin distribution is
irrelevant to it and the ground is simply that a floor must cover the case the
filter exists to guard against.

The channel is the set ALT-MATCHED would have excluded and ALT-BROAD does not:
live, NOT Continued, |A| >= 1, last insertion inside (tau1, tau2) -- OPEN at tau2 per 0057.
90 on APPLY,
89 on DERIV -- reproduced here, not taken from the record.

Zero API calls. Reads instance A's stored masks. Adopts nothing.
"""
import json
import sys

import numpy as np

M = "processed/step7/bb_a/masks_W108.npz"
DAY, W, H = 86400.0, 108, 91

m = np.load(M)
last, t0f = m["last_inst"], m["t0f"]
tau1 = t0f + W * DAY
tau2 = t0f + (W + H) * DAY
ap, dv = m["apply_"], m["deriv"]
cont, never = m["cont"], m["never"]

# ALT-BROAD, rebuilt from the primitives rather than read from m["ex"].
not_live = (~cont) & (last <= tau1)
excl_ns = not_live & never
excl_sl = not_live & ~never

# The channel: silent from an instant strictly inside (tau1, tau2), OPEN at tau2, hence live
# under ALT-BROAD, scored started-and-left, and unable to produce Continued
# evidence dated after that instant.
# 0057: OPEN at tau2. At s = tau2 the unobserved remainder (s, tau2) is empty, so nothing admissible
# is missing and the pair is NOT conceded. Both arms measured the two forms inert at W = 108; this
# asserts it rather than assuming it, and it is NOT expected to hold at W = 213, where D10 puts tau2
# at or adjacent to tau_pull and a mass point in last-insertion instants sits.
channel = (~cont) & (~never) & (last > tau1) & (last < tau2)
closed  = (~cont) & (~never) & (last > tau1) & (last <= tau2)
at_tau2 = int((closed & ~channel & (ap | dv)).sum())
assert at_tau2 == 0, f'W=108 no longer inert in the boundary form: {at_tau2} pairs sit exactly at tau2'

POPS = {"APPLY": (ap, 196654), "DERIV": (dv, 147370)}
C_CLOSED = {name: int((msk & closed).sum()) for name, (msk, _) in
            {"APPLY": (ap, 0), "DERIV": (dv, 0)}.items()}
out = {"what": "S&L floor under both extremes; ceiling and Continued ceiling alongside",
       "api_calls": 0, "W": W, "H": H, "populations": {}}

for name, (msk, n) in POPS.items():
    e_ns, e_sl = int((msk & excl_ns).sum()), int((msk & excl_sl).sum())
    ch = int((msk & channel).sum())
    live_sl = int((msk & ~not_live & ~cont & ~never).sum())   # S&L among retained pairs
    live_cont = int((msk & ~not_live & cont).sum())

    floor_none = live_sl                 # extreme A: none of the channel continued
    floor_all = live_sl - ch             # extreme B: all of them did
    ceiling = live_sl + e_ns + e_sl      # every exclusion is in truth S&L
    cont_ceiling = live_cont + e_ns + e_sl + ch

    out["populations"][name] = {
        "n": n, "exclusions": {"never_started": e_ns, "started_and_left": e_sl,
                               "total": e_ns + e_sl},
        "channel_pairs": ch,
        "floor_extreme_NONE_continued": {"count": floor_none, "pct": round(100 * floor_none / n, 4)},
        "floor_extreme_ALL_continued": {"count": floor_all, "pct": round(100 * floor_all / n, 4)},
        "endpoint_movement_pp": round(100 * ch / n, 4),
        "ceiling": {"count": ceiling, "pct": round(100 * ceiling / n, 4)},
        "ceiling_moves": False,
        "continued_ceiling": {"count": cont_ceiling, "pct": round(100 * cont_ceiling / n, 4)},
    }

# Instance A's D-2, actioned 2026-08-13 (0059). This block previously hardcoded its own
# conclusions as bare asserts, so the script could CONFIRM and could not REFUTE: a wrong
# recomputation would have raised AssertionError and been read as "the code is broken",
# never as "the expected value is wrong". A itself flagged that, and 0055 SS5c recorded it
# without acting. The expectations are now DATA, compared and reported per row, and the
# refutation path is the one that prints.
EXPECTED = {
    "source": "the arms' own deliverables and decisions 0054 / 0055, loaded as data, not asserted",
    "APPLY": {"exclusions_total": 703, "exclusions_never_started": 604, "channel_pairs": 90,
              "floor_extreme_ALL": 18952, "continued_ceiling": 144933},
    "DERIV": {"exclusions_total": 99, "exclusions_never_started": 0, "channel_pairs": 89,
              "floor_extreme_ALL": 16655, "continued_ceiling": 121570},
}
verdicts, refuted = [], 0
for pop in ("APPLY", "DERIV"):
    r, e = out["populations"][pop], EXPECTED[pop]
    got = {"exclusions_total": r["exclusions"]["total"],
           "exclusions_never_started": r["exclusions"]["never_started"],
           "channel_pairs": r["channel_pairs"],
           "floor_extreme_ALL": r["floor_extreme_ALL_continued"]["count"],
           "continued_ceiling": r["continued_ceiling"]["count"]}
    for k, want in e.items():
        ok = got[k] == want
        refuted += 0 if ok else 1
        verdicts.append({"population": pop, "row": k, "expected": want, "measured": got[k],
                         "verdict": "CONFIRMED" if ok else "REFUTED"})
out["verdicts"] = verdicts
out["refuted_rows"] = refuted
out["W213_boundary_claim"] = {
    "claim": ("at W = 213 the open and closed channel windows are NOT expected to agree, because "
              "D10 forces tau1 <= tau_pull - 91 d, so tau2 sits at or adjacent to tau_pull, where a "
              "mass point in last-insertion instants lies"),
    "status": "ARGUED, NOT MEASURED",
    "why_not_measured": "only W = 108 masks are on disk; measuring it needs a Step 13 arm rerun",
    "measured_here": {"W": 108,
                      "open_channel": {p: out["populations"][p]["channel_pairs"] for p in ("APPLY", "DERIV")},
                      "closed_channel": {p: C_CLOSED[p] for p in ("APPLY", "DERIV")},
                      "inert_at_this_arm": all(out["populations"][p]["channel_pairs"] == C_CLOSED[p]
                                               for p in ("APPLY", "DERIV"))},
    "do_not_cite_this_script_as_evidence_for_W213": True,
}

hdr = f"{'':8} {'n':>9} {'chan':>5} {'floor NONE':>18} {'floor ALL':>18} {'moves':>8} {'ceiling':>18} {'Cont ceiling':>18}"
print(hdr)
for name, r in out["populations"].items():
    print(f"{name:8} {r['n']:>9,} {r['channel_pairs']:>5} "
          f"{r['floor_extreme_NONE_continued']['count']:>8,} {r['floor_extreme_NONE_continued']['pct']:>8.4f}% "
          f"{r['floor_extreme_ALL_continued']['count']:>8,} {r['floor_extreme_ALL_continued']['pct']:>8.4f}% "
          f"{r['endpoint_movement_pp']:>7.4f} "
          f"{r['ceiling']['count']:>8,} {r['ceiling']['pct']:>8.4f}% "
          f"{r['continued_ceiling']['count']:>8,} {r['continued_ceiling']['pct']:>8.4f}%")

for v in verdicts:
    if v["verdict"] == "REFUTED":
        print(f"  REFUTED  {v['population']} {v['row']}: expected {v['expected']}, "
              f"measured {v['measured']}")
print(f"\n{len(verdicts) - refuted}/{len(verdicts)} rows CONFIRMED, {refuted} REFUTED "
      f"-- reported, not asserted (D-2, 0059)")
print("W = 213 boundary behaviour is ARGUED, NOT MEASURED here; do not cite this script for it.")
json.dump(out, open("processed/step7/query/floor_extremes.json", "w"), indent=2)
sys.exit(1 if refuted else 0)
