"""The un-guarded channel under ALT-BROAD, per Red Team's fifth Step 7 review.

ALT-BROAD's warrant: a pair silent after tau1 can produce no evidence in
[tau1, tau2) and is scored "left" by construction. That holds identically for a
pair silent after tau1 + eps for any eps < 91 days -- the failure mode is
continuous and the rule cuts it at one end.

This counts what the rule leaves open: pairs that are NOT Continued, are live
ONLY because they inserted after tau1, and whose last insertion falls inside
(tau1, tau2). Reproduces the 703 exclusions as a basis check.

Reads instance A's stored masks. Zero API calls. Nothing adopted.
"""
import json
import numpy as np

M = "processed/step7/bb_a/masks_W108.npz"
DAY, W, H = 86400.0, 108, 91

m = np.load(M)
t0f, last = m["t0f"], m["last_inst"]
tau1, tau2 = t0f + W * DAY, t0f + (W + H) * DAY
ap, cont, never, left = m["apply_"], m["cont"], m["never"], m["left"]

notcont = ~cont
has_after = last > tau1                 # conjunct 1 fails -> the pair is LIVE
excl = ap & notcont & ~has_after        # ALT-BROAD exclusions; must be 703
live_c1 = ap & notcont & has_after      # live ONLY by conjunct 1
chan = live_c1 & (last < tau2)          # last insertion inside (tau1, tau2)

assert int(excl.sum()) == 703, f"basis check failed: {int(excl.sum())} != 703"

g = (last - tau1) / DAY
out = {
    "population_APPLY": int(ap.sum()),
    "not_continued_APPLY": int(notcont[ap].sum()),
    "alt_broad_exclusions_APPLY": int(excl.sum()),
    "live_only_by_conjunct1_APPLY": int(live_c1.sum()),
    "channel_last_insertion_in_open_tau1_tau2": int(chan.sum()),
    "channel_never_started": int((chan & never).sum()),
    "channel_started_and_left": int((chan & left).sum()),
    "closed_share_pct": round(100 * excl.sum() / (excl.sum() + chan.sum()), 1),
    "channel_days_past_tau1": {
        "p50": round(float(np.median(g[chan])), 1),
        "p90": round(float(np.percentile(g[chan], 90)), 1),
        "max": round(float(g[chan].max()), 1),
    },
    "W": W, "H": H, "population": "APPLY = Step 5 line 1 less D10 = 196,654",
    "api_calls": 0,
}
print(json.dumps(out, indent=2))
json.dump(out, open("processed/step7/query/channel.json", "w"), indent=2)
