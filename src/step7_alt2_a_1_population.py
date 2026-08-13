"""Step 7 RERUN on the ADOPTED rule (decisions/0046), instance namespace `a`. STAGE 1 of 5.

THE ADOPTED RULE
  A user-show pair is NOT LIVE iff BOTH
    (i)  the account shows no insertion instant after that pair's tau1 = [[T0]] + W*24h, AND
    (ii) |A| = 0, i.e. Step 1 SS7's Never-started condition.

STAGE 1 builds and ASSERTS the two populations named in decisions/0046 SS0:
  DERIV  Step 5 waterfall line 4 (152,126) less D10   -> asserted == 147,370   requires S2 evidence
  APPLY  Step 5 waterfall line 1 (201,900) less D10   -> asserted == 196,654   Step 8 position 6

D10 right-censoring (Step 1 SS6): [[T0]] + (max(W,91) + H)*24h <= tau_pull, W = 108, H = 91.
Filter order decisions/0029: ... 4 contamination -> 5 right-censoring -> 6 liveness. D10 runs
BEFORE liveness, so a D10-removed pair is never offered to the rule.

Zero API calls.
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
P2 = os.path.join(ROOT, "processed/step2")
OUT = os.path.join(ROOT, "processed/step7/alt2_a")

SEC_PER_DAY = 86400.0
W_DAYS = 108                  # decisions/0026
H_DAYS = 91                   # D10
BACKFILL_D = 180.0            # Step 5 constant
POSTDATE_D = -30.0            # Step 5 constant
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)


def build_waterfall(p):
    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    the1542 = t0c & ~has_s2
    keep = ~(all_air | the1542)
    fs2_bad = has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                        | (p.first_s2_airdate.values == 1)
                        | (p.first_s2_corrupt.values == 1))
    w1 = keep
    w2 = w1 & has_s2
    w3 = w2 & ~t0c
    w4 = w3 & ~postd
    w5 = w4 & ~fs2_bad
    return [w1, w2, w3, w4, w5], has_s2


def t0_floor_epoch(p):
    t0_dt = pd.to_datetime(p.t0, utc=True, errors="coerce")
    v = (t0_dt.dt.floor("D").dt.tz_localize(None).to_numpy()
         .astype("datetime64[s]").astype("int64").astype("float64"))
    v[t0_dt.isna().to_numpy()] = np.nan
    ok = ~np.isnan(v)
    assert v[ok].min() > 0 and v[ok].max() < 2.2e9, "T0 epoch unit wrong"
    return v


def main():
    os.makedirs(OUT, exist_ok=True)

    cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate", "t0_contaminated",
            "complete_rec_lag_days", "first_s2_lag_days", "first_s2_airdate",
            "first_s2_corrupt", "t0"]
    p = pd.read_csv(os.path.join(P5, "pair_revision5.csv"), usecols=cols)

    masks, has_s2 = build_waterfall(p)
    computed = [int(m.sum()) for m in masks]
    assert computed == PUBLISHED_WATERFALL, f"waterfall mismatch: {computed}"
    line1, line4 = masks[0], masks[3]

    t0f = t0_floor_epoch(p)
    nan_line1 = int((line1 & np.isnan(t0f)).sum())
    nan_line4 = int((line4 & np.isnan(t0f)).sum())
    assert nan_line4 == 0, "T0 undefined inside line 4"

    need = (max(W_DAYS, 91) + H_DAYS) * SEC_PER_DAY
    keep10 = np.nan_to_num(t0f, nan=np.inf) + need <= TAU_PULL

    deriv = line1 & masks[3] & keep10      # line4 & D10
    apply_ = line1 & keep10
    n_deriv, n_apply = int(deriv.sum()), int(apply_.sum())
    assert n_deriv == 147370, f"DERIV is {n_deriv}, expected 147,370"
    assert n_apply == 196654, f"APPLY is {n_apply}, expected 196,654"
    assert int((deriv & ~apply_).sum()) == 0, "DERIV must be a subset of APPLY"

    tau1 = t0f + W_DAYS * SEC_PER_DAY
    tau2 = t0f + (W_DAYS + H_DAYS) * SEC_PER_DAY

    # L2 == 1 exclusion (Step 8 position 2): asserted a no-op on BOTH populations, not assumed
    f = pd.read_csv(os.path.join(P2, "frame.csv"),
                    usecols=["show_trakt_id", "s2_L", "s2_F", "s2_E"])
    l2 = dict(zip(f.show_trakt_id.astype(int), f.s2_L.astype(int)))
    l2_one = {}
    for nm, m in (("DERIV", deriv), ("APPLY", apply_)):
        shows = set(int(s) for s in p.show_trakt_id.values[m])
        missing = sorted(s for s in shows if s not in l2)
        assert not missing, f"{len(missing)} shows in {nm} absent from the frame"
        l2_one[nm] = sorted(s for s in shows if l2[s] == 1)

    np.savez_compressed(
        os.path.join(OUT, "population.npz"),
        user_idx=p.user_idx.values.astype(np.int64),
        show=p.show_trakt_id.values.astype(np.int64),
        t0_floor=t0f, tau1=tau1, tau2=tau2,
        line1=line1, line4=line4, keep_d10=keep10,
        deriv=deriv, apply_=apply_, has_s2=has_s2,
    )

    summary = {
        "step": 7,
        "what": "Step 7 RERUN on the ADOPTED rule (decisions/0046). GATE. Adopts nothing.",
        "instance": "alt2_a",
        "stage": 1,
        "api_calls": 0,
        "W_days": W_DAYS, "H_days": H_DAYS,
        "tau_pull_utc": "2026-08-11T00:00:00Z",
        "waterfall_computed": computed,
        "waterfall_published": PUBLISHED_WATERFALL,
        "waterfall_asserted_equal": True,
        "d10_rule": "[[T0]] + (max(W,91)+H)*24h <= tau_pull",
        "d10_latest_admissible_T0_utc": str(np.datetime64(int(TAU_PULL - need), "s")),
        "populations": {
            "DERIV": {
                "definition": "Step 5 waterfall line 4 (152,126) less D10; REQUIRES S2 evidence",
                "before_d10": int(line4.sum()), "d10_removed": int(line4.sum()) - n_deriv,
                "pairs": n_deriv, "asserted_equals": 147370,
                "accounts": int(np.unique(p.user_idx.values[deriv]).size),
                "shows": len(set(int(s) for s in p.show_trakt_id.values[deriv])),
                "pairs_without_any_S2_evidence": int((deriv & ~has_s2).sum()),
            },
            "APPLY": {
                "definition": "Step 5 waterfall line 1 (201,900) less D10; what Step 8 "
                              "filters at position 6",
                "before_d10": int(line1.sum()), "d10_removed": int(line1.sum()) - n_apply,
                "pairs": n_apply, "asserted_equals": 196654,
                "accounts": int(np.unique(p.user_idx.values[apply_]).size),
                "shows": len(set(int(s) for s in p.show_trakt_id.values[apply_])),
                "pairs_without_any_S2_evidence": int((apply_ & ~has_s2).sum()),
            },
        },
        "APPLY_minus_DERIV_pairs": n_apply - n_deriv,
        "t0_undefined_in_line1": nan_line1,
        "t0_undefined_in_line4": nan_line4,
        "l2_eq_1_shows_DERIV": len(l2_one["DERIV"]),
        "l2_eq_1_shows_APPLY": len(l2_one["APPLY"]),
        "l2_eq_1_exclusion_is_a_noop_on_both": (not l2_one["DERIV"]) and (not l2_one["APPLY"]),
    }
    with open(os.path.join(OUT, "population.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
