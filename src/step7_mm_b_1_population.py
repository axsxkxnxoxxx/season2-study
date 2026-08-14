"""Step 7 RERUN ON THE ADOPTED RULE ALT-MATCHED (instance b, namespace mm_b) -- stage 1.

GATE. NOTHING HERE IS ADOPTED. The Human Lead approves and diffs the two arms.

THE ADOPTED RULE (decisions/0052 Sec 1; task-sheet.md Step 7):

    A user-show pair is NOT LIVE iff EITHER
      (i)  |A| = 0   AND the account shows no insertion instant after
           tau1 = [T0] + W x 24h ;  OR
      (ii) |A| >= 1  AND the pair is NOT Continued AND the account shows no
           insertion instant after tau2 = [T0] + (W + H) x 24h .
    Otherwise it is live.

EACH NULL IS TESTED AT THE INSTANT ITS OWN OUTCOME IS READ. Never-started is
read at tau1; started-and-left is read at tau2, because the Continued condition
it negates is read at tau2. This is the whole change from the superseded
ALT-BROAD (0048), which tested BOTH nulls at tau1.

Stage 1 builds the two populations, D10 per arm, and BOTH silence tests per arm.

  DERIV  Step 5 waterfall line 4 (152,126) less D10 -> 147,370 at W = 108.
  APPLY  Step 5 waterfall line 1 (201,900) less D10 -> 196,654 at W = 108.

The per-account maximum insertion instant is recomputed here from the sweep and
the STORED isotonic calibration -- READ, NEVER REFITTED (0029) -- and then
cross-checked element-wise against this instance's own stored arrays at
processed/step7/bb_b/acct_instants.npz and processed/step7/alt2_b/pairs.npz.
Reuse is verified, not assumed.

ZERO network calls. Reads only.

Out: processed/step7/mm_b/pairs.npz, processed/step7/mm_b/stage1.json
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
PRIOR_PAIRS = ROOT / "processed" / "step7" / "alt2_b" / "pairs.npz"
PRIOR_ACCT = ROOT / "processed" / "step7" / "bb_b" / "acct_instants.npz"
OUT = ROOT / "processed" / "step7" / "mm_b"

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
        "instance": "data-scientist-b", "namespace": "mm_b", "stage": 1,
        "api_calls": 0, "adopts": "nothing",
        "gate": "Step 7 is a GATE. This is a proposal. Nothing here is adopted.",
        "rule": ("NOT LIVE iff EITHER (|A| = 0 AND no insertion after tau1) "
                 "OR (|A| >= 1 AND NOT Continued AND no insertion after tau2)"),
        "rule_source": "decisions/0052 Sec 1; task-sheet.md Step 7",
        "rule_name": "ALT-MATCHED",
        "supersedes": "ALT-BROAD (0048 Sec 1), which tested both nulls at tau1",
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
    prov["step5_waterfall_expected"] = WATERFALL
    prov["step5_waterfall_asserted"] = True

    keep_mask = w[0]                       # line 1 -- APPLY base, before D10
    line4_mask_full = w[3]                 # line 4 -- DERIV base, before D10
    pop = p.loc[keep_mask, ["user_idx", "show_trakt_id", "t0"]].reset_index(drop=True)
    in_line4 = line4_mask_full[keep_mask]
    has_s2_pop = has_s2[keep_mask]
    assert len(pop) == 201_900
    assert int(in_line4.sum()) == 152_126
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

    # ---------- per-account max insertion instant, recomputed from source ----------
    cal = np.load(P5 / "calibration.npz")
    knot_rid, knot_time = cal["knot_rid"], cal["knot_time"]
    prov["calibration"] = {
        "source": "processed/step5/calibration.npz",
        "status": "READ, NEVER REFITTED",
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
    print(f"per-account max insertion instant recomputed  ({time.time() - t:.1f}s)", flush=True)

    # ---------- cross-checks against this instance's own stored arrays ----------
    az = np.load(PRIOR_ACCT)
    prior_max = az["max_inst"]
    assert len(prior_max) == n_users
    assert np.array_equal(np.isfinite(max_inst), np.isfinite(prior_max))
    fin_m = np.isfinite(max_inst)
    assert np.array_equal(max_inst[fin_m], prior_max[fin_m])
    prov["crosscheck_bb_b_acct_instants"] = "EXACT match on all %d accounts" % n_users

    pz = np.load(PRIOR_PAIRS)
    assert np.array_equal(pz["user_idx"], pop.user_idx.values.astype(np.int64))
    assert np.array_equal(pz["show_trakt_id"], sh)
    assert np.array_equal(pz["t0_midnight_epoch"], t0_mid)
    assert np.array_equal(pz["in_line4"], in_line4)
    assert np.array_equal(pz["k"], k)
    assert np.array_equal(pz["f2"], f2)
    assert np.array_equal(pz["L2"], L2)
    prov["crosscheck_alt2_b_pairs"] = (
        "EXACT match on row identity, T0, line-4 flag, k, F2 and L2 for all 201,900 line-1 pairs")

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
        "max_inst_pair": mx,
    }
    per_arm = {}
    for W in W_ARMS:
        tau1 = t0_mid.astype(np.float64) + W * DAY
        tau2 = t0_mid.astype(np.float64) + (W + H) * DAY
        d10 = t0_mid + (max(W, 91) + H) * 86400 <= TAU_PULL
        # "after" is strict: no instant strictly greater than the boundary.
        no_after_1 = mx <= tau1
        no_after_2 = mx <= tau2
        # tau1 < tau2, so "silent after tau1" implies "silent after tau2": the tau2 test is the
        # WEAKER one and its set is a SUPERSET. That is why ALT-MATCHED excludes MORE than
        # ALT-BROAD on the started-and-left null, and it is asserted rather than assumed.
        assert (no_after_1 <= no_after_2).all(), "silence at tau1 must imply silence at tau2"
        out[f"no_after_tau1_W{W}"] = no_after_1
        out[f"no_after_tau2_W{W}"] = no_after_2
        out[f"d10_W{W}"] = d10
        # the stored ALT-BROAD conjunct (a) must reproduce exactly
        assert np.array_equal(no_after_1, pz[f"no_after_W{W}"]), \
            f"recomputed silence-at-tau1 disagrees with the stored array at W={W}"
        assert np.array_equal(d10, pz[f"d10_W{W}"]), f"D10 disagrees at W={W}"
        per_arm[str(W)] = {
            "W": W, "tau2_offset_days": W + H,
            "APPLY_n": int(d10.sum()),
            "DERIV_n": int((d10 & in_line4).sum()),
            "silence_at_tau1_APPLY": int((no_after_1 & d10).sum()),
            "silence_at_tau2_APPLY": int((no_after_2 & d10).sum()),
            "silence_at_tau1_DERIV": int((no_after_1 & d10 & in_line4).sum()),
            "silence_at_tau2_DERIV": int((no_after_2 & d10 & in_line4).sum()),
        }
    prov["crosscheck_silence_at_tau1_and_D10"] = (
        "recomputed silence-at-tau1 and D10 reproduce alt2_b/pairs.npz EXACTLY at all 8 arms")
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
