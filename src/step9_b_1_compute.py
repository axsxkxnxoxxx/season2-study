"""Step 9, arm `b`, stage 1: reproduce the adopted arm and measure the premiere-anchored arm.

Adopts nothing. Zero API calls.

WHAT THIS DOES AND DOES NOT DO.
  - It does NOT rebuild APPLY, DERIV or D4. Every figure for the adopted arm
    (W = 108, finale-anchored) is CONSUMED from Step 8's approved artifacts; the
    reproduction below is a CONTROL on the harness, not a second definition, and
    the file records that it agreed rather than substituting its own numbers.
  - It DOES measure the second headline arm (W = 91, anchored on the later of the
    S2 premiere and the first-pass S1 completion date), because no step in the
    spec produces it. It is measured by driving STEP 8's OWN rule library with a
    substituted T0, so it is the same implementation and not a second one.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
sys.path.insert(0, os.path.join(ROOT, "src"))
import step8_a_lib as L                                       # noqa: E402

OUT = os.path.join(ROOT, "processed/step9/b")
os.makedirs(OUT, exist_ok=True)

scan = np.load(os.path.join(ROOT, "processed/step8/a/scan.npz"), allow_pickle=True)
positions = np.load(os.path.join(ROOT, "processed/step8/a/positions.npz"), allow_pickle=True)
frame = pd.read_csv(os.path.join(ROOT, "processed/step2/frame.csv"))

arms = L.Arms(scan, positions, frame, H=91)

# ---- CONTROL: reproduce the adopted arm before trusting the harness ------------------------
r108 = arms.run(108)
pos5, pos5d = r108["pos5"], r108["pos5_deriv"]
ctl = {
    "position_5_APPLY": int(pos5.sum()),
    "position_5_DERIV": int(pos5d.sum()),
    "liveness_excluded_APPLY": int((pos5 & r108["not_live"]).sum()),
    "liveness_excluded_DERIV": int((pos5d & r108["not_live"]).sum()),
    "never_started_position_5_APPLY": int((pos5 & r108["never"]).sum()),
    "started_and_left_position_5_APPLY": int((pos5 & r108["left"]).sum()),
    "continued_position_5_APPLY": int((pos5 & r108["continued"]).sum()),
    "never_started_position_7_APPLY": int((pos5 & ~r108["not_live"] & r108["never"]).sum()),
    "started_and_left_position_7_APPLY": int((pos5 & ~r108["not_live"] & r108["left"]).sum()),
    "continued_position_7_APPLY": int((pos5 & ~r108["not_live"] & r108["continued"]).sum()),
    "never_started_position_7_DERIV": int((pos5d & ~r108["not_live"] & r108["never"]).sum()),
    "started_and_left_position_7_DERIV": int((pos5d & ~r108["not_live"] & r108["left"]).sum()),
    "continued_position_7_DERIV": int((pos5d & ~r108["not_live"] & r108["continued"]).sum()),
}
EXPECTED = {  # from artifacts/step8-waterfall-{a,b}.json, the approved gate deliverable
    "position_5_APPLY": 196654, "position_5_DERIV": 147370,
    "liveness_excluded_APPLY": 703, "liveness_excluded_DERIV": 99,
    "never_started_position_5_APPLY": 33373, "started_and_left_position_5_APPLY": 19141,
    "continued_position_5_APPLY": 144140,
    "never_started_position_7_APPLY": 32769, "started_and_left_position_7_APPLY": 19042,
    "continued_position_7_APPLY": 144140,
    "never_started_position_7_DERIV": 9145, "started_and_left_position_7_DERIV": 16744,
    "continued_position_7_DERIV": 121382,
}
ctl_ok = all(ctl[k] == v for k, v in EXPECTED.items())

# ---- the channel pairs the started-and-left floor concedes, at the adopted arm --------------
# retained, NOT Continued, live only because they inserted after tau1, last insertion inside
# (tau1, tau2). Recomputed here as a control on the same ruled figures (90 / 89 / 207 / 3).
def channel(mask, r):
    live = ~r["not_live"]
    inside = (arms.last_inst > r["tau1"]) & (arms.last_inst < r["tau2"])
    base = mask & live & ~r["continued"] & inside
    return {"all": int(base.sum()),
            "started_and_left_component": int((base & r["left"]).sum()),
            "never_started_component": int((base & r["never"]).sum())}

ch108 = {"APPLY": channel(pos5, r108), "DERIV": channel(pos5d, r108)}

# ---- the premiere-anchored arm --------------------------------------------------------------
# T0' = max(S2 premiere date, first-pass S1 completion date), midnight UTC.
prem = pd.to_datetime(frame.set_index("show_trakt_id")["s2_premiere_date"], utc=True)
prem_epoch = (prem.astype("int64") // 10 ** 9).reindex(arms.pair_show).to_numpy().astype(np.int64)
s1_date = positions["s1_date"].astype(np.int64)
t0_prem = np.maximum(prem_epoch, s1_date)

t0_finale = positions["t0"].astype(np.int64)
arms.t0 = t0_prem
r91p = arms.run(91)
# THE POPULATION IS THE ADOPTED ARM'S, NOT RE-DERIVED. task-sheet.md Step 9: "Both arms run on
# the same right-censored population, max(W, 91) + H (D10)."  D10's 91-term exists so that the
# 91-day arm is observable on the primary arm's row set; and T0' <= T0 by construction, so
# tau2' <= T0 + 182 d < tau2 <= tau_pull for every retained pair.
r91p["pos5"], r91p["pos5_deriv"] = pos5, pos5d
ch91p = {"APPLY": channel(pos5, r91p), "DERIV": channel(pos5d, r91p)}

premiere = {
    "t0_is_earlier_or_equal_for_every_pair": bool((t0_prem <= t0_finale).all()),
    "pairs_where_t0_moves": int((t0_prem < t0_finale)[pos5].sum()),
    "tau2_observable_on_every_retained_pair_APPLY":
        bool((r91p["tau2"][pos5] <= L.TAU_PULL).all()),
    "tau2_observable_on_every_retained_pair_DERIV":
        bool((r91p["tau2"][pos5d] <= L.TAU_PULL).all()),
}

def counts(mask, r):
    live = ~r["not_live"]
    return {
        "n_position_5": int(mask.sum()),
        "n_post_liveness": int((mask & live).sum()),
        "position_5": {"never_started": int((mask & r["never"]).sum()),
                       "started_and_left": int((mask & r["left"]).sum()),
                       "continued": int((mask & r["continued"]).sum())},
        "position_7": {"never_started": int((mask & live & r["never"]).sum()),
                       "started_and_left": int((mask & live & r["left"]).sum()),
                       "continued": int((mask & live & r["continued"]).sum())},
        "exclusions": {
            "total_pairs": int((mask & r["not_live"]).sum()),
            "never_started_component": int((mask & r["not_live"] & r["never"]).sum()),
            "started_and_left_component": int((mask & r["not_live"] & r["left"]).sum()),
            "continued_component": int((mask & r["not_live"] & r["continued"]).sum()),
            "accounts": int(np.unique(arms.pair_user[mask & r["not_live"]]).size),
            "silence_test_alone": int((mask & r["silent"]).sum()),
            "spared_by_not_continued": int((mask & r["silent"] & r["continued"]).sum()),
        },
        "conjunct_selection": {
            "start": int(mask.sum()),
            "after_conjunct_2_not_continued": int((mask & ~r["continued"]).sum()),
            "after_conjunct_1_silent_at_tau1": int((mask & ~r["continued"] & r["silent"]).sum()),
        },
    }

out = {
    "step": 9, "instance": "data-scientist-b", "arm": "b", "stage": 1, "api_calls": 0,
    "adopts": "nothing",
    "harness_control_against_step8_artifacts": {
        "measured": ctl, "expected": EXPECTED, "agrees": ctl_ok,
        "what_this_is": "a control on the harness, not a republication: the adopted arm's "
                        "figures are CONSUMED from Step 8's artifacts and this run only "
                        "establishes that the same library reproduces them before it is driven "
                        "with a substituted T0",
    },
    "channel_pairs_conceded_by_the_floor": {"W108_s2_finale": ch108, "W91_s2_premiere": ch91p},
    "premiere_arm_preconditions": premiere,
    "W108_s2_finale": {"APPLY": counts(pos5, r108), "DERIV": counts(pos5d, r108)},
    "W91_s2_premiere": {"APPLY": counts(pos5, r91p), "DERIV": counts(pos5d, r91p)},
}
with open(os.path.join(OUT, "stage1_counts.json"), "w") as fh:
    json.dump(out, fh, indent=1)

np.savez_compressed(
    os.path.join(OUT, "pairs.npz"),
    pair_user=arms.pair_user, pos5=pos5, pos5_deriv=pos5d,
    never_108=r108["never"], left_108=r108["left"], cont_108=r108["continued"],
    notlive_108=r108["not_live"],
    never_91p=r91p["never"], left_91p=r91p["left"], cont_91p=r91p["continued"],
    notlive_91p=r91p["not_live"])

print(json.dumps({"control_agrees": ctl_ok,
                  "control": ctl,
                  "channel": ch108,
                  "premiere_pre": premiere}, indent=1))
print(json.dumps(out["W91_s2_premiere"], indent=1))
