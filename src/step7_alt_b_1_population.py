"""Step 7 ALTERNATIVE-RULE EVALUATION (instance b, namespace alt_b) -- stage 1.

EVALUATION ONLY. NOTHING IS ADOPTED. The Human Lead rules after both arms report.

Builds TWO populations and attaches the liveness state to both:

  DERIV  Step 5 waterfall line 4 (152,126) less D10   -- the population
         decisions/0042 published its 751 exclusions on. Line 4 requires
         `has_s2`, i.e. the pair has at least one S2 record somewhere in the
         sweep. That restriction is load-bearing for this evaluation and is
         reported as such.

  APPLY  Step 5 retained ANALYSIS population, line 1 (201,900) less D10 --
         decisions/0041 Sec 3 / 0042 Sec 5 name this as the population Step 8
         will apply liveness to (196,654 at W = 108). It ADMITS pairs with no
         S2 evidence at all, which line 4 excludes by construction.

Liveness state per W arm, matching src/step7_b4_bracket.py exactly:
  a pair is "open-ended" (state 1) iff the account has NO insertion instant
  strictly after that pair's tau1 = [T0] + W x 24h, i.e. max(instants) <= tau1.
  searchsorted(..., side="right") == len(seq), same operator as b4.

The per-account distinct insertion instants are READ from
processed/step7/b4/instants.npz. The stored Step 5 calibration is NOT refitted
here and is not touched at all -- b4 already applied it.

ZERO network calls. Reads only.

Out: processed/step7/alt_b/pairs.npz, processed/step7/alt_b/stage1.json
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
OUT = ROOT / "processed" / "step7" / "alt_b"

BACKFILL_D, POSTDATE_D = 180.0, -30.0
WATERFALL = [201_900, 178_165, 155_131, 152_126, 128_099]
W_ADOPTED, H, DAY = 108, 91, 86400.0
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype(np.int64)  # decisions/0011


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()
    prov: dict = {
        "instance": "data-scientist-b", "namespace": "alt_b", "stage": 1,
        "api_calls": 0, "adopts": "nothing",
        "purpose": "evaluate Red Team's alternative liveness rule against PF-LIMIT",
        "W_adopted": W_ADOPTED, "H": H, "W_arms": W_ARMS,
    }

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
    prov["waterfall_asserted"] = True

    # ---- APPLY population: line 1, the Step 5 retained analysis population.
    keep_mask = w[0]
    line4_mask_full = w[3]
    pop = p.loc[keep_mask, ["user_idx", "show_trakt_id", "t0"]].reset_index(drop=True)
    in_line4 = line4_mask_full[keep_mask]
    has_s2_pop = has_s2[keep_mask]
    assert len(pop) == 201_900
    assert int(in_line4.sum()) == 152_126

    t0_ser = pd.to_datetime(pop.t0, utc=True)
    prov["t0_null_in_line1"] = int(t0_ser.isna().sum())
    assert prov["t0_null_in_line1"] == 0, "a line-1 pair has no clock start"
    t0_mid = t0_ser.values.astype("datetime64[s]").astype(np.int64)
    assert (t0_mid % 86400 == 0).all(), "T0 is not a bare UTC date"

    # ---- row-identity check against b4's line-4 construction
    br = np.load(B4 / "bracket.npz")
    assert (br["user_idx"] == pop.user_idx.values[in_line4]).all()
    assert (br["show_trakt_id"] == pop.show_trakt_id.values[in_line4]).all()
    assert (br["t0_midnight_epoch"] == t0_mid[in_line4]).all()
    prov["b4_line4_row_identity_asserted"] = True

    # ---- frame fields
    f = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_L", "s2_F"])
    need = {int(r.show_trakt_id): math.ceil(0.90 * int(r.s2_L)) for r in f.itertuples()}
    fin = {int(r.show_trakt_id): int(r.s2_F) for r in f.itertuples()}
    l2 = {int(r.show_trakt_id): int(r.s2_L) for r in f.itertuples()}
    sh = pop.show_trakt_id.values
    k = np.array([need.get(int(s), 10 ** 9) for s in sh], dtype=np.int64)
    f2 = np.array([fin.get(int(s), -1) for s in sh], dtype=np.int64)
    L2 = np.array([l2.get(int(s), -1) for s in sh], dtype=np.int64)
    assert (L2 > 0).all(), "a pair's show is missing from the frame"
    prov["L2_eq_1_pairs_in_line1"] = int((L2 == 1).sum())

    # ---- liveness state per arm, on the WHOLE line-1 set
    iz = np.load(B4 / "instants.npz")
    tau_all, offsets = iz["tau"], iz["offsets"]
    uidx = pop.user_idx.values.astype(np.int64)
    n = len(pop)
    # per-account max insertion instant; accounts with zero instants -> -inf
    cnt = np.diff(offsets)
    max_inst = np.full(len(cnt), -np.inf)
    nz = np.nonzero(cnt > 0)[0]
    max_inst[nz] = tau_all[offsets[nz + 1] - 1]        # tau_all is sorted within account
    prov["accounts_with_zero_instants"] = int((cnt == 0).sum())
    prov["accounts_present_in_line1"] = int(len(np.unique(uidx)))

    out: dict = {
        "user_idx": uidx,
        "show_trakt_id": sh.astype(np.int64),
        "t0_midnight_epoch": t0_mid,
        "in_line4": in_line4,
        "has_s2_evidence": has_s2_pop,
        "k": k, "f2": f2, "L2": L2,
    }
    per_arm = {}
    mx = max_inst[uidx]
    for W in W_ARMS:
        tau1 = t0_mid.astype(np.float64) + W * DAY
        d10 = t0_mid + (max(W, 91) + H) * 86400 <= TAU_PULL
        no_after = mx <= tau1                     # NOT LIVE under PF-LIMIT
        out[f"no_after_W{W}"] = no_after
        out[f"d10_W{W}"] = d10
        per_arm[str(W)] = {
            "W": W,
            "line1_after_D10": int(d10.sum()),
            "line4_after_D10": int((d10 & in_line4).sum()),
            "PF_LIMIT_not_live_line1": int((no_after & d10).sum()),
            "PF_LIMIT_not_live_line4": int((no_after & d10 & in_line4).sum()),
        }
        # cross-check against b4's own state array on line 4
        st = br[f"state_W{W}"]
        bd = br[f"d10_W{W}"]
        assert (bd == d10[in_line4]).all(), W
        assert (((st == 1) & bd).sum() == per_arm[str(W)]["PF_LIMIT_not_live_line4"]), W
        assert ((st == 1) == no_after[in_line4]).all(), W
    prov["b4_state_reproduced_on_line4_all_arms"] = True
    prov["per_arm"] = per_arm

    np.savez(OUT / "pairs.npz", **out)
    prov["elapsed_s"] = time.time() - t
    (OUT / "stage1.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps(prov, indent=2))


if __name__ == "__main__":
    main()
