"""Step 7 (rerun), instance b2 -- stage 4: diagnostics for the write-up.
Aggregates only. Zero API calls."""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "b2"
THR = 914

d = pd.read_csv(OUT / "pair_bracket.csv")
meas = d.state.values == 0
g = d.gap_days.values
live = meas & (g < THR)

acc = d.groupby("user_idx").agg(n=("state", "size"), nlive=("state", lambda s: 0))
tmp = pd.DataFrame({"u": d.user_idx.values, "live": live})
a = tmp.groupby("u").live.agg(["size", "sum"])
mixed = int(((a["sum"] > 0) & (a["sum"] < a["size"])).sum())

boot = []
gm = g[meas]
rng = np.random.default_rng(20260813)
for _ in range(400):
    boot.append(np.percentile(rng.choice(gm, len(gm), replace=True), 99.0))
boot = np.array(boot)

out = {
    "accounts_total": int(d.user_idx.nunique()),
    "accounts_all_pairs_live": int((a["sum"] == a["size"]).sum()),
    "accounts_no_pair_live": int((a["sum"] == 0).sum()),
    "accounts_MIXED_live_and_not": mixed,
    "mixed_pct_of_accounts": round(100.0 * mixed / d.user_idx.nunique(), 2),
    "bootstrap_99th_percentile_days": {
        "point": float(np.percentile(gm, 99.0)),
        "p2.5": float(np.percentile(boot, 2.5)),
        "p97.5": float(np.percentile(boot, 97.5)),
        "ceiled_p2.5": math.ceil(float(np.percentile(boot, 2.5))),
        "ceiled_p97.5": math.ceil(float(np.percentile(boot, 97.5))),
        "resamples": 400, "seed": 20260813,
    },
    "exclusion_composition_at_threshold": {
        "not_live_total": int(len(d) - live.sum()),
        "share_from_measured_gap_pct": round(100.0 * int((meas & ~live).sum()) / int(len(d) - live.sum()), 2),
        "share_from_evidence_absence_pct": round(
            100.0 * int(((d.state.values == 1) | (d.state.values == 2)).sum()) / int(len(d) - live.sum()), 2),
    },
    "no_instant_at_or_before_tau1_share_of_population_pct": round(
        100.0 * int((d.state.values == 2).sum()) / len(d), 2),
    "gap_days_of_failing_pairs": {
        "n": int((meas & ~live).sum()),
        "min": float(np.nanmin(g[meas & ~live])),
        "median": float(np.nanpercentile(g[meas & ~live], 50)),
        "max": float(np.nanmax(g[meas & ~live])),
    },
}
(OUT / "diag.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
