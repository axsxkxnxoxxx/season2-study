"""Step 7 RERUN ON THE ADOPTED RULE (instance b, namespace alt2_b) -- stage 1.

GATE. NOTHING IS ADOPTED HERE. The Human Lead approves and diffs the two arms.

THE ADOPTED RULE (decisions/0046 Sec 1, task-sheet Step 7):

    A user-show pair is NOT LIVE iff BOTH
      (a) the account shows no insertion instant strictly after that pair's
          tau1 = [T0] + W x 24h, AND
      (b) |A| = 0, i.e. Step 1 Sec 7's Never-started condition, read at tau1.
    Otherwise it is live.

Stage 1 builds the two populations and conjunct (a).

  DERIV  Step 5 waterfall line 4 (152,126) less D10 -> 147,370 at W = 108.
         Requires S2 evidence by construction.
  APPLY  Step 5 waterfall line 1 (201,900) less D10 -> 196,654 at W = 108.
         This is what Step 8 filters at position 6. It admits pairs with no
         S2 evidence at all.

Conjunct (a) is computed from the per-account MAXIMUM insertion instant.
Insertion instant = the STORED Step 5 isotonic play-id calibration, READ and
NOT REFITTED (task-sheet Step 7; decisions/0029). Application is verbatim
src/step5_calibrate.py::insert_time -> np.interp(rid, knot_rid, knot_time),
which clamps outside the knot range.

The per-account maximum is recomputed here directly from the sweep and the
stored curve, and then cross-checked against the distinct-instant sequence this
instance already built at processed/step7/b4/instants.npz. Reuse is verified,
not assumed.

ZERO network calls. Reads only.

Out: processed/step7/alt2_b/pairs.npz, processed/step7/alt2_b/stage1.json
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
OUT = ROOT / "processed" / "step7" / "alt2_b"

BACKFILL_D, POSTDATE_D = 180.0, -30.0
WATERFALL = [201_900, 178_165, 155_131, 152_126, 128_099]   # Step 5, lines 1-5
W_ADOPTED, H, DAY = 108, 91, 86400.0
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype(np.int64)  # decisions/0011


def insert_time(rid, knot_rid, knot_time):
    """Verbatim from src/step5_calibrate.py. The curve is READ, never refitted."""
    return np.interp(rid.astype(np.float64), knot_rid, knot_time)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()
    prov: dict = {
        "instance": "data-scientist-b", "namespace": "alt2_b", "stage": 1,
        "api_calls": 0, "adopts": "nothing",
        "rule": "NOT LIVE iff (no insertion instant after tau1) AND (|A| = 0 at tau1)",
        "rule_source": "decisions/0046 Sec 1",
        "W_adopted": W_ADOPTED, "H": H, "W_arms": W_ARMS,
    }

    # ---------- Step 5 waterfall, asserted before anything is used ----------
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
    prov["step5_waterfall_measured"] = got
    prov["step5_waterfall_asserted"] = True

    keep_mask = w[0]                       # line 1 -- APPLY base, before D10
    line4_mask_full = w[3]                 # line 4 -- DERIV base, before D10
    pop = p.loc[keep_mask, ["user_idx", "show_trakt_id", "t0"]].reset_index(drop=True)
    in_line4 = line4_mask_full[keep_mask]
    has_s2_pop = has_s2[keep_mask]
    assert len(pop) == 201_900
    assert int(in_line4.sum()) == 152_126
    # line 4 requires S2 evidence -- the construction 0046 Sec 1 calls "forced"
    assert has_s2_pop[in_line4].all()
    prov["line4_implies_has_s2_evidence_asserted"] = True

    t0_ser = pd.to_datetime(pop.t0, utc=True)
    assert int(t0_ser.isna().sum()) == 0, "a line-1 pair has no clock start"
    t0_mid = t0_ser.values.astype("datetime64[s]").astype(np.int64)
    assert (t0_mid % 86400 == 0).all(), "T0 is not a bare UTC date"

    # ---------- frame fields ----------
    f = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_L", "s2_F"])
    need = {int(r.show_trakt_id): math.ceil(0.90 * int(r.s2_L)) for r in f.itertuples()}
    fin = {int(r.show_trakt_id): int(r.s2_F) for r in f.itertuples()}
    l2 = {int(r.show_trakt_id): int(r.s2_L) for r in f.itertuples()}
    sh = pop.show_trakt_id.values.astype(np.int64)
    k = np.array([need.get(int(s), 10 ** 9) for s in sh], dtype=np.int64)
    f2 = np.array([fin.get(int(s), -1) for s in sh], dtype=np.int64)
    L2 = np.array([l2.get(int(s), -1) for s in sh], dtype=np.int64)
    assert (L2 > 0).all(), "a pair's show is missing from the frame"
    prov["L2_eq_1_pairs_in_line1"] = int((L2 == 1).sum())

    # ---------- conjunct (a): per-account max insertion instant ----------
    cal = np.load(P5 / "calibration.npz")
    knot_rid, knot_time = cal["knot_rid"], cal["knot_time"]
    prov["calibration"] = {
        "source": "processed/step5/calibration.npz",
        "status": "READ, NOT REFITTED",
        "n_knots": int(len(knot_rid)),
        "application": "np.interp(rid, knot_rid, knot_time), verbatim step5_calibrate.insert_time",
    }
    z = np.load(P5 / "full_scan.npz")
    user = z["user"]
    rid = z["rid"]
    prov["records_in_sweep"] = int(len(rid))
    tau_rec = insert_time(rid, knot_rid, knot_time)
    prov["calibration"]["records_clamped_below_first_knot"] = int((rid < knot_rid[0]).sum())
    prov["calibration"]["records_clamped_above_last_knot"] = int((rid > knot_rid[-1]).sum())
    n_users = int(user.max()) + 1
    max_inst = np.full(n_users, -np.inf)
    np.maximum.at(max_inst, user, tau_rec)
    del tau_rec, rid, user, z
    print(f"per-account max insertion instant computed  ({time.time() - t:.1f}s)", flush=True)

    # cross-check against the distinct-instant sequence built at b4 (same instance)
    iz = np.load(B4 / "instants.npz")
    tau_all, offsets = iz["tau"], iz["offsets"]
    cnt = np.diff(offsets)
    mx_b4 = np.full(len(cnt), -np.inf)
    nz = np.nonzero(cnt > 0)[0]
    mx_b4[nz] = tau_all[offsets[nz + 1] - 1]      # tau_all sorted within account
    assert len(mx_b4) == n_users
    assert np.array_equal(np.isfinite(max_inst), np.isfinite(mx_b4))
    assert np.allclose(max_inst[np.isfinite(max_inst)], mx_b4[np.isfinite(mx_b4)],
                       rtol=0, atol=0)
    prov["b4_instants_cross_check"] = "exact match on every account's max insertion instant"
    prov["accounts_with_zero_instants"] = int((cnt == 0).sum())

    uidx = pop.user_idx.values.astype(np.int64)
    prov["accounts_present_in_line1"] = int(len(np.unique(uidx)))
    mx = max_inst[uidx]

    out: dict = {
        "user_idx": uidx,
        "show_trakt_id": sh,
        "t0_midnight_epoch": t0_mid,
        "in_line4": in_line4,
        "has_s2_evidence": has_s2_pop,
        "k": k, "f2": f2, "L2": L2,
    }
    per_arm = {}
    for W in W_ARMS:
        tau1 = t0_mid.astype(np.float64) + W * DAY
        d10 = t0_mid + (max(W, 91) + H) * 86400 <= TAU_PULL
        no_after = mx <= tau1                    # conjunct (a): NO instant strictly after tau1
        out[f"no_after_W{W}"] = no_after
        out[f"d10_W{W}"] = d10
        per_arm[str(W)] = {
            "W": W,
            "APPLY_n": int(d10.sum()),
            "DERIV_n": int((d10 & in_line4).sum()),
            "conjunct_a_only_APPLY": int((no_after & d10).sum()),
            "conjunct_a_only_DERIV": int((no_after & d10 & in_line4).sum()),
        }
    assert per_arm["108"]["APPLY_n"] == 196_654, per_arm["108"]
    assert per_arm["108"]["DERIV_n"] == 147_370, per_arm["108"]
    prov["populations_asserted_at_W108"] = {"APPLY": 196_654, "DERIV": 147_370}
    prov["per_arm"] = per_arm

    np.savez(OUT / "pairs.npz", **out)
    prov["elapsed_s"] = time.time() - t
    (OUT / "stage1.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps(prov, indent=2))


if __name__ == "__main__":
    main()
