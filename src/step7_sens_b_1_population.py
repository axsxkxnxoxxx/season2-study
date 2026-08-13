"""Step 7 gate-closing sensitivity test (instance b, namespace sens_b) -- stage 1.

Builds the population this diagnostic runs on and attaches the liveness
bracketing state already computed in processed/step7/b4/bracket.npz.

NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved gate.

Population, per decisions/0038 Sec 2 as amended by 0040 Sec 2 and 0041 Sec 2:
  Step 5 waterfall line 4 -- the 152,126 -- LESS D10 right-censoring at W = 108.
  This is the liveness derivation AND application population inside Step 7.
  It is NOT the population Step 8 would use (0041 Sec 3: 196,654). Stated as a
  judgement call in the deliverable.

ZERO network calls. Reads only.

Out: processed/step7/sens_b/pairs.npz, processed/step7/sens_b/stage1.json
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
B4 = ROOT / "processed" / "step7" / "b4"
OUT = ROOT / "processed" / "step7" / "sens_b"

BACKFILL_D, POSTDATE_D = 180.0, -30.0
WATERFALL = [201_900, 178_165, 155_131, 152_126, 128_099]
W, H, DAY = 108, 91, 86400.0
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype(np.int64)  # decisions/0011


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()
    prov: dict = {"instance": "data-scientist-b", "namespace": "sens_b", "stage": 1,
                  "api_calls": 0, "W": W, "H": H}

    p = pd.read_csv(P5 / "pair_revision5.csv")
    prov["pair_table_rows"] = int(len(p))
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
    prov["waterfall_measured"] = got
    prov["waterfall_expected"] = WATERFALL
    prov["waterfall_asserted"] = True
    prov["reference_line"] = 4
    prov["n_line4"] = got[3]

    pop = p.loc[w[3], ["user_idx", "show_trakt_id", "t0"]].reset_index(drop=True)
    t0_mid = pd.to_datetime(pop.t0, utc=True).values.astype("datetime64[s]").astype(np.int64)
    assert (t0_mid % 86400 == 0).all(), "T0 is not a bare UTC date"

    # ---- attach the b4 bracketing state. Same construction order, so assert row identity.
    br = np.load(B4 / "bracket.npz")
    assert len(br["user_idx"]) == len(pop) == 152_126
    assert (br["user_idx"] == pop.user_idx.values).all()
    assert (br["show_trakt_id"] == pop.show_trakt_id.values).all()
    assert (br["t0_midnight_epoch"] == t0_mid).all()
    prov["b4_bracket_row_identity_asserted"] = True

    gap = br["gap_days_W108"]          # continuous days; NaN where no measured gap
    state = br["state_W108"]           # 0 measured, 1 no-instant-after, 2 no-instant-at-or-before
    d10 = br["d10_W108"]               # True = retained by right-censoring

    # D10 recomputed here independently of b4 and asserted equal.
    d10_here = t0_mid + (max(W, 91) + H) * 86400 <= TAU_PULL
    assert (d10_here == d10).all()
    prov["D10"] = {
        "rule": "retain iff [T0] + (max(W,91) + H) x 24h <= tau_pull",
        "bound_days": max(W, 91) + H,
        "tau_pull": "2026-08-11T00:00:00Z",
        "n_before": int(len(pop)),
        "POST_D10_COUNT": int(d10.sum()),
        "removed": int((~d10).sum()),
    }
    prov["class_counts_post_D10"] = {
        "measured_bracketing_gap": int(((state == 0) & d10).sum()),
        "open_ended_no_instant_after_tau1": int(((state == 1) & d10).sum()),
        "no_instant_at_or_before_tau1_LIVE_per_0021": int(((state == 2) & d10).sum()),
    }

    # ---- frame fields for the outcome test
    f = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_E", "s2_L", "s2_F"])
    need = {int(r.show_trakt_id): math.ceil(0.90 * int(r.s2_L)) for r in f.itertuples()}
    fin = {int(r.show_trakt_id): int(r.s2_F) for r in f.itertuples()}
    l2 = {int(r.show_trakt_id): int(r.s2_L) for r in f.itertuples()}
    sh = pop.show_trakt_id.values
    k = np.array([need.get(int(s), 10 ** 9) for s in sh], dtype=np.int64)
    f2 = np.array([fin.get(int(s), -1) for s in sh], dtype=np.int64)
    L2 = np.array([l2.get(int(s), -1) for s in sh], dtype=np.int64)
    assert (L2 > 0).all(), "a pair's show is missing from the frame"

    prov["L2_eq_1"] = {
        "pairs_in_line4": int((L2 == 1).sum()),
        "pairs_post_D10": int(((L2 == 1) & d10).sum()),
        "shows_post_D10": int(len(np.unique(sh[(L2 == 1) & d10]))),
        "note": "Step 1 Sec 7 excludes L2 = 1 from the headline population; Step 8 does it "
                "at filter position 2. Handled as a reported variant in stage 3.",
    }
    prov["accounts_post_D10"] = int(len(np.unique(pop.user_idx.values[d10])))
    prov["shows_post_D10"] = int(len(np.unique(sh[d10])))

    np.savez(
        OUT / "pairs.npz",
        user_idx=pop.user_idx.values.astype(np.int64),
        show_trakt_id=sh.astype(np.int64),
        t0_midnight_epoch=t0_mid,
        gap_days=gap, state=state, d10=d10,
        k=k, f2=f2, L2=L2,
    )
    prov["elapsed_s"] = time.time() - t
    (OUT / "stage1.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps(prov, indent=2))


if __name__ == "__main__":
    main()
