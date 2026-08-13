"""Step 7 rerun (instance b4) -- stage 2: population, D10 censoring, bracketing gaps.

READ ONLY. ZERO network calls.

Population, per decisions/0038 Sec 2 as AMENDED by decisions/0040 Sec 2:
  waterfall line 4 (the 152,126), LESS D10 right-censoring, per W arm.
  D10 (Step 1 Sec 6): retain a pair only if [T0] + (max(W,91) + H) x 24h <= tau_pull,
  with H = 91 and tau_pull = 2026-08-11T00:00:00Z (decisions/0011).
  Liveness is applied at Step 8 position 6, AFTER right-censoring at position 5
  (0029), so derivation and application populations are the post-D10 set.

Bracketing gap, decisions/0036 Sec 2: for each pair, tau1 = [T0] + W x 24h; on
that pair's ACCOUNT, over the stage-1 distinct insertion instants, the last
instant at or before tau1 and the first instant strictly after it.

Edge cases, 0036 Sec 2.3 as AMENDED by 0040 Sec 1:
  (i)  no instant after tau1        -> open-ended gap (+inf)
  (ii) no instant at or before tau1 -> WITHDRAWN as a not-live ruling.
       0021 (approved gate 2 of 5): any record inserted after the window closed
       proves the account was alive. These pairs are LIVE. Counted separately.

Out: processed/step7/b4/bracket.npz          (row-level, per W arm)
     processed/step7/b4/population_meta.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "b4"

# Inherited from Step 5, not re-derived.
BACKFILL_D = 180.0
POSTDATE_D = -30.0
WATERFALL = [201_900, 178_165, 155_131, 152_126, 128_099]

W_ADOPTED = 108                                   # decisions/0026, ceiling per 0025
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]     # decisions/0027: union 38..213
H = 91                                            # decisions/0001 D10, held constant
DAY = 86400.0
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype(np.int64)  # decisions/0011


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
    prov["waterfall_asserted"] = True

    prov["reference_line"] = 4
    prov["reference_line_label"] = "completing record not postdated"
    prov["n_before_D10"] = got[3]
    return p[w4].copy(), prov


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()

    pop, prov = build_population()
    print(f"line 4 population {len(pop):,}  ({time.time() - t:.1f}s)", flush=True)

    inst = np.load(OUT / "instants.npz")
    tau_all, offsets = inst["tau"], inst["offsets"]

    uidx = pop.user_idx.values.astype(np.int64)
    t0_mid = pd.to_datetime(pop.t0).values.astype("datetime64[s]").astype(np.int64)
    assert (t0_mid % 86400 == 0).all(), "T0 is not a bare UTC date"

    prov["tau_pull_epoch_s"] = int(TAU_PULL)
    prov["tau_pull"] = "2026-08-11T00:00:00Z"
    prov["H"] = H
    prov["W_adopted"] = W_ADOPTED
    prov["W_arms"] = W_ARMS
    prov["accounts_in_line4"] = int(len(np.unique(uidx)))
    prov["shows_in_line4"] = int(pop.show_trakt_id.nunique())

    n = len(pop)
    order = np.argsort(uidx, kind="stable")
    out = {
        "user_idx": uidx,
        "show_trakt_id": pop.show_trakt_id.values,
        "t0_midnight_epoch": t0_mid,
    }
    per_arm = {}

    for W in W_ARMS:
        tau1 = t0_mid.astype(np.float64) + W * DAY
        # D10 right-censoring, applied BEFORE liveness (0029 positions 5 then 6)
        d10 = t0_mid + (max(W, 91) + H) * 86400 <= TAU_PULL

        gap = np.full(n, np.nan)
        state = np.zeros(n, dtype=np.int8)  # 0 measured, 1 none-after, 2 none-at-or-before
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
            st[no_before] = 2
            state[sl] = st
            i = j

        out[f"gap_days_W{W}"] = gap
        out[f"state_W{W}"] = state
        out[f"d10_W{W}"] = d10

        c = {
            "W": W,
            "censoring_bound_days": max(W, 91) + H,
            "n_before_D10": int(n),
            "n_after_D10": int(d10.sum()),
            "removed_by_D10": int((~d10).sum()),
            "measured_gap": int(((state == 0) & d10).sum()),
            "open_ended_no_instant_after_tau1": int(((state == 1) & d10).sum()),
            "no_instant_at_or_before_tau1_LIVE_per_0021": int(((state == 2) & d10).sum()),
        }
        c["extended_set"] = c["measured_gap"] + c["open_ended_no_instant_after_tau1"]
        c["open_ended_share_of_extended"] = (
            c["open_ended_no_instant_after_tau1"] / c["extended_set"] if c["extended_set"] else None
        )
        per_arm[str(W)] = c
        print(
            f"W={W:3d}  postD10 {c['n_after_D10']:,}  measured {c['measured_gap']:,}  "
            f"open-ended {c['open_ended_no_instant_after_tau1']:,} "
            f"({c['open_ended_share_of_extended']:.4%} of extended)  "
            f"no-pre-instant(LIVE) {c['no_instant_at_or_before_tau1_LIVE_per_0021']:,}  "
            f"({time.time() - t:.1f}s)",
            flush=True,
        )

    np.savez(OUT / "bracket.npz", **out)
    prov["per_arm"] = per_arm
    prov["elapsed_s"] = time.time() - t
    (OUT / "population_meta.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps({k: v for k, v in prov.items() if k != "per_arm"}, indent=2))


if __name__ == "__main__":
    main()
