"""The started-and-left floor under both extremes, on both populations.

Human Lead ruling, 2026-08-14: 0054 §3 grounded the widened floor on a margin
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

a, d = out["populations"]["APPLY"], out["populations"]["DERIV"]
assert (a["exclusions"]["total"], a["exclusions"]["never_started"]) == (703, 604)
assert (d["exclusions"]["total"], d["exclusions"]["never_started"]) == (99, 0)
assert (a["channel_pairs"], d["channel_pairs"]) == (90, 89)
assert a["floor_extreme_ALL_continued"]["count"] == 18952
assert d["floor_extreme_ALL_continued"]["count"] == 16655
assert a["continued_ceiling"]["count"] == 144933
assert d["continued_ceiling"]["count"] == 121570

hdr = f"{'':8} {'n':>9} {'chan':>5} {'floor NONE':>18} {'floor ALL':>18} {'moves':>8} {'ceiling':>18} {'Cont ceiling':>18}"
print(hdr)
for name, r in out["populations"].items():
    print(f"{name:8} {r['n']:>9,} {r['channel_pairs']:>5} "
          f"{r['floor_extreme_NONE_continued']['count']:>8,} {r['floor_extreme_NONE_continued']['pct']:>8.4f}% "
          f"{r['floor_extreme_ALL_continued']['count']:>8,} {r['floor_extreme_ALL_continued']['pct']:>8.4f}% "
          f"{r['endpoint_movement_pp']:>7.4f} "
          f"{r['ceiling']['count']:>8,} {r['ceiling']['pct']:>8.4f}% "
          f"{r['continued_ceiling']['count']:>8,} {r['continued_ceiling']['pct']:>8.4f}%")

json.dump(out, open("processed/step7/query/floor_extremes.json", "w"), indent=2)
