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
import step9_b_0_clock as C                                   # noqa: E402

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
#
# THE EPOCH CONVERSION IS DERIVED FROM THE DTYPE, NEVER HARDCODED. An earlier build of this
# stage divided by `10 ** 9`, which is a claim about `datetime64[ns]`; this column resolves at
# `datetime64[us]` and the claim was false, so the whole premiere vector decoded to January 1970
# and T0' collapsed onto the S1 completion date for every pair. A second constant would be the
# same defect with a different number, so `step9_b_0_clock.epoch_seconds()` reads the tick rate
# off the dtype and cross-checks it against numpy's own unit-declared cast.
f_idx = frame.set_index("show_trakt_id")
prem = pd.to_datetime(f_idx["s2_premiere_date"], utc=True)
prem_epoch_by_show, prem_conversion = C.epoch_seconds(prem)
# the finale vector, by the SAME converter, so the premiere/finale ordering below is measured on
# two vectors built the same way rather than on one built two ways
fin_epoch_by_show, _ = C.epoch_seconds(pd.to_datetime(f_idx["s2_finale_date"], utc=True))
prem_epoch = pd.Series(prem_epoch_by_show, index=prem.index).reindex(arms.pair_show).to_numpy()
if np.isnan(np.asarray(prem_epoch, dtype="float64")).any():
    raise AssertionError("HARD STOP: a pair's show is absent from the frame, so its premiere "
                         "date is missing; a NaN cast to int64 would enter the clock silently.")
prem_epoch = prem_epoch.astype(np.int64)
prem_epoch = (prem_epoch // L.DAY) * L.DAY          # midnight UTC, as Step 8 floors T0
s1_date = positions["s1_date"].astype(np.int64)
t0_prem = np.maximum(prem_epoch, s1_date)

# DEF-A, RUN BEFORE ANY FIGURE IS COMPUTED FROM THE VECTOR. The epoch vector is decoded back to
# calendar dates and compared, ELEMENTWISE and on every row, against the frame's own
# s2_premiere_date strings. NOT a calendar window (DEF-B), which passes clean on a vector that is
# wrong in every entry. It RAISES rather than returning a flag a caller can ignore, and it states
# its coverage, because a check that looked at nothing and a check that found nothing report the
# same value.
def_a = C.verify_premiere_epoch(prem_epoch_by_show, f_idx["s2_premiere_date"].to_numpy(),
                                prem_epoch, f_idx["s2_premiere_date"]
                                .reindex(arms.pair_show).to_numpy())

t0_finale = positions["t0"].astype(np.int64)
assert np.array_equal(arms.t0, t0_finale), "the harness did not start on the finale clock"

# THE T0 SUBSTITUTION IS SCOPED. `arms` is the shared harness object and the previous build
# mutated `arms.t0` here and never restored it, so every later read of the harness would have
# been on the premiere clock without saying so. The substitution now lives in a try/finally and
# the restoration is asserted, not assumed.
try:
    arms.t0 = t0_prem
    r91p = arms.run(91)
finally:
    arms.t0 = t0_finale
assert np.array_equal(arms.t0, t0_finale), "arms.t0 was not restored after the premiere run"
assert arms.t0 is t0_finale
# THE POPULATION IS THE ADOPTED ARM'S, NOT RE-DERIVED. task-sheet.md Step 9: "Both arms run on
# the same right-censored population, max(W, 91) + H (D10)."  D10's 91-term exists so that the
# 91-day arm is observable on the primary arm's row set; and T0' <= T0 for every pair, so
# tau2' < tau2 <= tau_pull on every retained one. THAT WARRANT IS CHECKED, BY T0PRIME-ORDER
# BELOW, WHICH RAISES -- it is not asserted here and it is not inferred from the counts.
r91p["pos5"], r91p["pos5_deriv"] = pos5, pos5d
ch91p = {"APPLY": channel(pos5, r91p), "DERIV": channel(pos5d, r91p)}

# ---- the ORDERING warrant, CHECKED --------------------------------------------------------
# THE DELIVERABLE CLAIMS THE ROW SET NEED NOT BE RE-CENSORED BECAUSE T0' <= T0. A deliverable
# asserts only what its arm MEASURED, so that claim is measured here and the check RAISES.
# It is not the bare inequality: `T0' = max(premiere, S1 completion)` makes `T0' <= T0` true
# unconditionally on a collapsed vector, which is exactly what the removed boolean
# `t0_is_earlier_or_equal_for_every_pair` was. Part 1 reconstructs T0' from the frame's own date
# STRINGS -- a source the epoch conversion never touches -- and is what fails on the defective
# vector. Demonstrated failing in src/step9_b_0b_reproduce.py, run record
# logs/step9_b_premiere_clock_repro.txt.
t0p_order = C.verify_t0_prime_order(
    t0_prime=t0_prem,
    t0_finale=t0_finale,
    premiere_dates_by_pair=f_idx["s2_premiere_date"].reindex(arms.pair_show).to_numpy(),
    s1_epoch=s1_date,
    tau2_prime=r91p["tau2"],
    tau2_finale=r108["tau2"],
    tau_pull=L.TAU_PULL,
    retained={"APPLY": pos5, "DERIV": pos5d},
)

# ---- the premiere clock vector, VERIFIED --------------------------------------------------
# WHAT THIS REPLACES, and why. The previous build carried three preconditions here --
# `t0_is_earlier_or_equal_for_every_pair` and `tau2_observable_on_every_retained_pair_{APPLY,
# DERIV}`. All three were guaranteed by T0' having collapsed to ~0, so none could fail and none
# checked anything: run on the defective vector they all return True (demonstrated in
# src/step9_b_0b_reproduce.py, run record logs/step9_b_premiere_clock_repro.txt). DEF-A and
# T0PRIME-ORDER are the replacements; this block only reports what they found.
premiere = {
    "t0_prime_order_verification": t0p_order,
    "clock_vector_verification": {
        "check": "DEF-A, elementwise against the frame's own s2_premiere_date",
        "replaces": ["the divisor claim `// 10 ** 9`"],
        "the_three_removed_booleans_are_replaced_by": "T0PRIME-ORDER, at "
                                                      "$.premiere_arm_preconditions."
                                                      "t0_prime_order_verification",
        "why_replaced": "all three were guaranteed by the defective T0' and returned True on a "
                        "vector that was wrong in every entry; they could not fail and therefore "
                        "checked nothing",
        "raises_on_failure": True,
        "by_show": def_a["by_show"],
        "by_pair": def_a["by_pair"],
        "total_rows_compared": def_a["total_rows_compared"],
        "epoch_conversion": prem_conversion,
        "t0_restored_after_the_substituted_run": bool(np.array_equal(arms.t0, t0_finale)),
    },
    # MEASURED PROPERTIES OF THE CORRECTED VECTOR, reported as counts. These are consequences,
    # not preconditions: they are what the clock does, and they are stated so a reader can see it
    # rather than infer it.
    "pairs_where_t0_moves": int((t0_prem < t0_finale)[pos5].sum()),
    "shows_where_premiere_precedes_finale": int((prem_epoch_by_show < fin_epoch_by_show).sum()),
    "shows_where_premiere_equals_finale": int((prem_epoch_by_show == fin_epoch_by_show).sum()),
    "shows_where_premiere_follows_finale": int((prem_epoch_by_show > fin_epoch_by_show).sum()),
    "shows_total": int(len(f_idx)),
    "pairs_where_t0_prime_is_the_premiere_date": int((t0_prem == prem_epoch)[pos5].sum()),
    "pairs_where_t0_prime_is_the_s1_completion_date": int((t0_prem == s1_date)[pos5].sum()),
    "retained_pairs_with_tau2_after_tau_pull_APPLY":
        int((r91p["tau2"][pos5] > L.TAU_PULL).sum()),
    "retained_pairs_with_tau2_after_tau_pull_DERIV":
        int((r91p["tau2"][pos5d] > L.TAU_PULL).sum()),
    "note_on_the_tau2_counts": "COUNTS, not the check. The same two comparisons are ASSERTED "
                               "elementwise, and raise, in T0PRIME-ORDER part 3; these are the "
                               "counts restated where a reader can see them. ON THEIR OWN THEY "
                               "CANNOT DETECT A WRONG PREMIERE VECTOR -- they are implied by "
                               "T0' <= T0 and D10, and T0' <= T0 is itself implied by any "
                               "collapsed T0'. DEF-A and T0PRIME-ORDER part 1 are what can fail "
                               "on such a vector.",
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
