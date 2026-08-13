"""Step 7 gate-closing sensitivity test (decisions/0041 SS4), instance namespace `a`.

STAGE 1 of 4 — population.

Rebuilds the Step 5 waterfall, asserts it against the published figures, takes waterfall
line 4 (the 152,126; decisions/0038 SS2), applies D10 right-censoring at W=108, H=91
(decisions/0040 SS2 puts the liveness derivation AFTER D10), and freezes the row masks the
later stages use.

This is NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved gate.

Zero API calls.
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
P2 = os.path.join(ROOT, "processed/step2")
OUT = os.path.join(ROOT, "processed/step7/sens_a")

SEC_PER_DAY = 86400.0
W_DAYS = 108                  # decisions/0026
H_DAYS = 91                   # D10
BACKFILL_D = 180.0            # Step 5 constant
POSTDATE_D = -30.0            # Step 5 constant
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
FROZEN_LINE = 3               # 0-based index of 152,126 == waterfall line 4
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
    return [w1, w2, w3, w4, w5]


def t0_floor_epoch(p):
    """[[T0]] — T0 floored to UTC midnight, as epoch seconds."""
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

    masks = build_waterfall(p)
    computed = [int(m.sum()) for m in masks]
    assert computed == PUBLISHED_WATERFALL, f"waterfall mismatch: {computed}"
    ref152 = masks[FROZEN_LINE]

    t0f = t0_floor_epoch(p)
    assert int((ref152 & np.isnan(t0f)).sum()) == 0, "T0 undefined inside the reference line"

    need = (max(W_DAYS, 91) + H_DAYS) * SEC_PER_DAY
    keep10 = np.nan_to_num(t0f, nan=np.inf) + need <= TAU_PULL
    ref = ref152 & keep10
    n_pairs = int(ref.sum())

    # tau1 and tau2, per decisions/0034
    tau1 = t0f + W_DAYS * SEC_PER_DAY
    tau2 = t0f + (W_DAYS + H_DAYS) * SEC_PER_DAY

    # L2 == 1 exclusion (Step 8 position 2): a no-op on this frame, asserted not assumed
    f = pd.read_csv(os.path.join(P2, "frame.csv"),
                    usecols=["show_trakt_id", "s2_L", "s2_F", "s2_E"])
    l2 = dict(zip(f.show_trakt_id.astype(int), f.s2_L.astype(int)))
    shows_in_ref = set(int(s) for s in p.show_trakt_id.values[ref])
    l2_one_shows = sorted(s for s in shows_in_ref if l2.get(s, -1) == 1)
    l2_missing = sorted(s for s in shows_in_ref if s not in l2)
    assert not l2_missing, f"{len(l2_missing)} shows in the reference are absent from the frame"

    np.savez_compressed(
        os.path.join(OUT, "population.npz"),
        user_idx=p.user_idx.values, show=p.show_trakt_id.values,
        t0_floor=t0f, tau1=tau1, tau2=tau2,
        ref152=ref152, keep_d10=keep10, ref=ref,
    )

    summary = {
        "step": 7,
        "what": "GATE-CLOSING SENSITIVITY DIAGNOSTIC for Step 7 (decisions/0041 SS4). "
                "NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved gate.",
        "instance": "sens_a",
        "api_calls": 0,
        "W_days": W_DAYS,
        "H_days": H_DAYS,
        "tau_pull_utc": "2026-08-11T00:00:00Z",
        "waterfall_computed": computed,
        "waterfall_published": PUBLISHED_WATERFALL,
        "waterfall_asserted_equal": True,
        "reference_line": "line 4 == 152,126 (decisions/0038 SS2)",
        "line4_pairs": int(ref152.sum()),
        "d10_rule": "[[T0]] + (max(W,91)+H)*24h <= tau_pull",
        "d10_latest_admissible_T0_utc": str(np.datetime64(int(TAU_PULL - need), "s")),
        "d10_removed": int(ref152.sum()) - n_pairs,
        "post_D10_population": n_pairs,
        "post_D10_share_of_line4": round(n_pairs / int(ref152.sum()), 6),
        "n_distinct_shows_in_population": len(shows_in_ref),
        "n_distinct_accounts_in_population": int(np.unique(p.user_idx.values[ref]).size),
        "l2_eq_1_shows_in_population": len(l2_one_shows),
        "l2_eq_1_exclusion_is_a_noop": len(l2_one_shows) == 0,
    }
    with open(os.path.join(OUT, "population.json"), "w") as f2:
        json.dump(summary, f2, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
