"""Exclusion count as a function of the silence anchor, swept from tau1 to tau2.

Red Team's seventh review: the continuity argument in 0052 §1 is symmetric. It
shows no instant in [tau1, tau2] is warranted, not that tau2 is. Neither arm was
asked for the curve. This is it.

The never-started branch is held at tau1 throughout -- 0034 anchors it there and
0021 licenses its null on activity after tau1. Only the started-and-left branch's
anchor moves: not live iff (NOT Continued) AND (no insertion after tau1 + f*H*24h).

f = 0 reproduces ALT-BROAD (703 APPLY / 99 DERIV S&L).
f = 1 reproduces ALT-MATCHED (793 / 189).

Zero API calls. Reads instance A's stored masks. Nothing adopted.
"""
import json
import numpy as np

M = "processed/step7/bb_a/masks_W108.npz"
DAY, W, H = 86400.0, 108, 91

m = np.load(M)
t0f, last = m["t0f"], m["last_inst"]
tau1 = t0f + W * DAY
ap, dv, cont, never, left = m["apply_"], m["deriv"], m["cont"], m["never"], m["left"]
notcont = ~cont

ns_excl = {p: int((msk & never & (last <= tau1)).sum()) for p, msk in (("APPLY", ap), ("DERIV", dv))}

rows = []
for f in [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]:
    anchor = tau1 + f * H * DAY
    sl = notcont & ~never & (last <= anchor)      # started-and-left branch
    rows.append({
        "f": f, "anchor_days_past_tau1": round(f * H, 1),
        "APPLY_sl": int((ap & sl).sum()), "APPLY_total": int((ap & sl).sum()) + ns_excl["APPLY"],
        "DERIV_sl": int((dv & sl).sum()), "DERIV_total": int((dv & sl).sum()) + ns_excl["DERIV"],
    })

assert rows[0]["APPLY_total"] == 703, f"f=0 must reproduce ALT-BROAD: {rows[0]}"
assert rows[-1]["APPLY_total"] == 793, f"f=1 must reproduce ALT-MATCHED: {rows[-1]}"

out = {"what": "exclusion count vs silence anchor swept tau1 -> tau2",
       "never_started_branch": "held at tau1 (0034); counts " + json.dumps(ns_excl),
       "api_calls": 0, "W": W, "H": H, "curve": rows}
print(f"{'days past τ1':>13} {'APPLY S&L':>10} {'APPLY tot':>10} {'DERIV S&L':>10} {'DERIV tot':>10}")
for r in rows:
    print(f"{r['anchor_days_past_tau1']:>13} {r['APPLY_sl']:>10} {r['APPLY_total']:>10} {r['DERIV_sl']:>10} {r['DERIV_total']:>10}")
json.dump(out, open("processed/step7/query/anchor_sweep.json", "w"), indent=2)
