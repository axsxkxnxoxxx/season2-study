"""Step 7 (instance b3) -- stage 2: the frozen population and its bracketing gaps.

READ ONLY. ZERO network calls.

Population: waterfall line 4, the 152,126 (decisions/0038 Sec 2). Reconstructed
with the same masks src/step5_revision5.py / src/step6_derive_w_b.py used and
asserted against the whole published waterfall
201,900 -> 178,165 -> 155,131 -> 152,126 -> 128,099.

For each pair, tau1 = [T0] + W x 24h  (Step 1 Sec 6/2.4; [T0] = UTC midnight of
T0's calendar date).  On that pair's ACCOUNT, over the distinct insertion
instants from stage 1: the last instant at or before tau1 and the first after
it.  That one gap is the pair's bracketing gap (decisions/0036 Sec 2).

Edge cases, decisions/0036 Sec 2.3, counted separately:
  no instant after tau1        -> not live (open-ended gap)
  no instant at or before tau1 -> not live (no pre-tau1 evidence)

Out: processed/step7/b3/bracket.npz        (per-pair, per-W arm; row-level)
     processed/step7/b3/population_meta.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "b3"

# Inherited from Step 5, not re-derived.
BACKFILL_D = 180.0
POSTDATE_D = -30.0
WATERFALL = [201_900, 178_165, 155_131, 152_126, 128_099]

W_ADOPTED = 108              # decisions/0026, ceiling per 0025
W_ARMS = [46, 77, 108, 150, 213]   # Step 13 arms, decisions/0027 + 0038 Sec 6
DAY = 86400.0


def build_population() -> tuple[pd.DataFrame, dict]:
    p = pd.read_csv(P5 / "pair_revision5.csv")
    prov = {"pair_table_rows": int(len(p))}

    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    the1542 = t0c & ~has_s2
    keep = ~(all_air | the1542)
    fs2_bad = has_s2 & (
        (p.first_s2_lag_days.values > BACKFILL_D)
        | (p.first_s2_airdate.values == 1)
        | (p.first_s2_corrupt.values == 1)
    )

    w1 = keep
    w2 = w1 & has_s2
    w3 = w2 & ~t0c
    w4 = w3 & ~postd
    w5 = w4 & ~fs2_bad
    got = [int(m.sum()) for m in (w1, w2, w3, w4, w5)]
    prov["waterfall_measured"] = got
    prov["waterfall_expected"] = WATERFALL
    assert got == WATERFALL, (got, WATERFALL)

    prov["line_used"] = 4
    prov["line_4_label"] = "completing record not postdated"
    prov["n"] = got[3]
    prov["derivation_and_application_population_identical"] = True

    return p[w4].copy(), prov


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()

    pop, prov = build_population()
    print(f"population {len(pop):,}  ({time.time() - t:.1f}s)")

    inst = np.load(OUT / "instants.npz")
    tau_all, offsets = inst["tau"], inst["offsets"]

    uidx = pop.user_idx.values.astype(np.int64)
    # [T0] = UTC midnight of T0's calendar date
    t0_mid = pd.to_datetime(pop.t0).values.astype("datetime64[s]").astype(np.int64)
    assert (t0_mid % 86400 == 0).all(), "T0 is not a bare UTC date"

    prov["distinct_accounts_in_population"] = int(len(np.unique(uidx)))
    prov["distinct_shows_in_population"] = int(pop.show_trakt_id.nunique())

    n = len(pop)
    order = np.argsort(uidx, kind="stable")
    out = {"user_idx": uidx, "show_trakt_id": pop.show_trakt_id.values,
           "t0_midnight_epoch": t0_mid}

    for W in W_ARMS:
        tau1 = t0_mid.astype(np.float64) + W * DAY
        gap = np.full(n, np.nan)
        state = np.zeros(n, dtype=np.int8)   # 0 measured, 1 none after, 2 none at/before
        # group by account; every pair on an account shares its instant sequence
        i = 0
        while i < n:
            j = i
            u = uidx[order[i]]
            while j < n and uidx[order[j]] == u:
                j += 1
            sl = order[i:j]
            lo, hi = offsets[u], offsets[u + 1]
            seq = tau_all[lo:hi]
            pos = np.searchsorted(seq, tau1[sl], side="right")
            no_before = pos == 0
            no_after = pos == len(seq)
            ok = ~(no_before | no_after)
            g = np.full(len(sl), np.nan)
            if ok.any():
                pk = pos[ok]
                g[ok] = (seq[pk] - seq[pk - 1]) / DAY
            gap[sl] = g
            st = np.zeros(len(sl), dtype=np.int8)
            st[no_after] = 1
            st[no_before] = 2   # no_before dominates only if both, which cannot happen
            state[sl] = st
            i = j
        out[f"gap_days_W{W}"] = gap
        out[f"state_W{W}"] = state
        print(f"W={W:3d}  measured {(state == 0).sum():,}  "
              f"none-after {(state == 1).sum():,}  none-before {(state == 2).sum():,}  "
              f"({time.time() - t:.1f}s)")

    np.savez(OUT / "bracket.npz", **out)
    prov["elapsed_s"] = time.time() - t
    (OUT / "population_meta.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps(prov, indent=2))


if __name__ == "__main__":
    main()
