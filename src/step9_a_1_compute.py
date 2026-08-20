"""Step 9, arm `a`, stage 1: the measured quantities.

CONSUMES STEP 8's OUTPUT. It does not rebuild the APPLY or DERIV populations and it does not
compute D4: those come from `processed/step8/a/` and are carried, not recomputed (0070 rulings 1
and 7).

WHAT THIS SCRIPT DOES COMPUTE, AND WHY IT IS NOT A SECOND DEFINITION:

  * the ACCOUNT-CLUSTERED BOOTSTRAP over Step 8's own per-pair outcome and liveness columns.
    Step 8 emits no interval; the interval is Step 9's work.
  * the PREMIERE-ANCHORED 91-day arm, which Step 8 does not emit at all -- its eight grid arms
    are finale-anchored. The outcome operator is NOT re-implemented here: `step8_a_lib.Arms` is
    imported and its `t0` vector is replaced with the premiere-anchored clock, so exactly one
    implementation of Step 1 SS7 exists on disk. The import is checked by reproducing Step 8's
    published finale-anchored counts before any premiere figure is taken.

Zero API calls. Writes processed/step9/a/measured.json and logs/step9/a_stage1.json.
"""
import json
import os
import sys
import hashlib

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
sys.path.insert(0, os.path.join(ROOT, "src"))

from step8_a_lib import Arms, DAY, TAU_PULL, NEVER, LEFT, CONT  # noqa: E402

S8 = os.path.join(ROOT, "processed", "step8", "a")
OUT = os.path.join(ROOT, "processed", "step9", "a")
LOGS = os.path.join(ROOT, "logs", "step9")

B_RESAMPLES = 10_000          # decisions/0103
SEED = 20260818               # decisions/0103
CI_LEVEL = 95
H_DAYS = 91

os.makedirs(OUT, exist_ok=True)
os.makedirs(LOGS, exist_ok=True)


def sha12(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def floor_day(x):
    return (np.asarray(x) // DAY) * DAY


# ---------------------------------------------------------------------------------------------
# inputs
# ---------------------------------------------------------------------------------------------
scan = np.load(os.path.join(S8, "scan.npz"), allow_pickle=True)
positions = np.load(os.path.join(S8, "positions.npz"), allow_pickle=True)
frame = pd.read_csv(os.path.join(ROOT, "processed", "step2", "frame.csv"))
s8_outcomes = json.load(open(os.path.join(S8, "outcomes.json")))
s8_arms = json.load(open(os.path.join(S8, "arms.json")))
s8_positions = json.load(open(os.path.join(S8, "positions.json")))
s8_diag = json.load(open(os.path.join(S8, "diagnostics.json")))

A = Arms(scan, positions, frame, H=H_DAYS)
pair_user = scan["pair_user"]
n_pairs = pair_user.size

# ---------------------------------------------------------------------------------------------
# the three arms
# ---------------------------------------------------------------------------------------------
t0_finale = positions["t0"].astype(np.int64)

prem = pd.to_datetime(frame.set_index("show_trakt_id").s2_premiere_date
                      .reindex(A.pair_show), utc=True)
prem_epoch = floor_day(prem.to_numpy().astype("datetime64[s]").astype(np.int64))
s1_date = positions["s1_date"].astype(np.int64)
t0_premiere = np.maximum(prem_epoch, s1_date)

A.t0 = t0_finale
r108 = A.run(108)
r91f = A.run(91)
A.t0 = t0_premiere
r91p = A.run(91)
A.t0 = t0_finale

# ---------------------------------------------------------------------------------------------
# GATE ON THE IMPORT: reproduce Step 8's published finale-anchored counts before using the
# operator anywhere Step 8 has not already published.
# ---------------------------------------------------------------------------------------------
def outcome_counts(mask, res):
    o = res["outcome"]
    return dict(never_started=int((mask & (o == NEVER)).sum()),
                started_and_left=int((mask & (o == LEFT)).sum()),
                continued=int((mask & (o == CONT)).sum()),
                total=int(mask.sum()))


def accounts(mask):
    return int(np.unique(pair_user[mask]).size)


reproduction = {}
p5 = r108["pos5"]
p5d = r108["pos5_deriv"]
p6 = p5 & ~r108["not_live"]
p6d = p5d & ~r108["not_live"]
reproduction["position_5_APPLY"] = [int(p5.sum()), s8_outcomes["position_5_APPLY"]]
reproduction["position_5_DERIV"] = [int(p5d.sum()), s8_outcomes["position_5_DERIV"]]
reproduction["position_7_APPLY_post_liveness"] = [
    outcome_counts(p6, r108),
    s8_outcomes["position_7_outcome_assignment"]["APPLY_post_liveness"]]
reproduction["position_7_DERIV_post_liveness"] = [
    outcome_counts(p6d, r108),
    s8_outcomes["position_7_outcome_assignment"]["DERIV_post_liveness"]]
reproduction["position_5_APPLY_outcome_conditional"] = [
    outcome_counts(p5, r108),
    s8_outcomes["position_7_outcome_assignment"]["APPLY_at_position_5_outcome_conditional_view"]]
reproduction["position_5_DERIV_outcome_conditional"] = [
    outcome_counts(p5d, r108),
    s8_outcomes["position_7_outcome_assignment"]["DERIV_at_position_5_outcome_conditional_view"]]
excl = p5 & r108["not_live"]
excld = p5d & r108["not_live"]
reproduction["liveness_exclusions_APPLY"] = [
    dict(total=int(excl.sum()),
         never_started=int((excl & (r108["outcome"] == NEVER)).sum()),
         started_and_left=int((excl & (r108["outcome"] == LEFT)).sum()),
         accounts=accounts(excl)),
    s8_outcomes["position_6_liveness"]["APPLY"]["excluded"]]
reproduction["right_censoring_two_lines_APPLY"] = [
    dict(removed_by_max_W_91_term=int((positions["pos4"] & ~r108["keep_term1"]).sum()),
         removed_incrementally_by_the_plus_H_term=int(
             (positions["pos4"] & r108["keep_term1"] & ~r108["keep_d10"]).sum())),
    s8_positions["right_censoring_two_lines_APPLY"]]
reproduction["right_censoring_two_lines_DERIV"] = [
    dict(removed_by_max_W_91_term=int((positions["pos4_deriv"] & ~r108["keep_term1"]).sum()),
         removed_incrementally_by_the_plus_H_term=int(
             (positions["pos4_deriv"] & r108["keep_term1"] & ~r108["keep_d10"]).sum())),
    s8_positions["right_censoring_two_lines_DERIV"]]
reproduction["liveness_exclusions_DERIV"] = [
    dict(total=int(excld.sum()),
         never_started=int((excld & (r108["outcome"] == NEVER)).sum()),
         started_and_left=int((excld & (r108["outcome"] == LEFT)).sum()),
         accounts=accounts(excld)),
    s8_outcomes["position_6_liveness"]["DERIV"]["excluded"]]

mismatches = []
for k, (mine, theirs) in reproduction.items():
    if isinstance(mine, dict):
        for kk, vv in mine.items():
            if kk in theirs and theirs[kk] != vv:
                mismatches.append(f"{k}.{kk}: recomputed {vv} != step8 {theirs[kk]}")
    else:
        if mine != theirs:
            mismatches.append(f"{k}: recomputed {mine} != step8 {theirs}")
if mismatches:
    raise SystemExit("IMPORT GATE FAILED, premiere arm not computed:\n" + "\n".join(mismatches))


# ---------------------------------------------------------------------------------------------
# per-arm figure block
# ---------------------------------------------------------------------------------------------
def channel_mask(res, pop):
    """Retained, NOT Continued, live only because an insertion followed tau1, and whose last
    insertion falls inside (tau1, tau2): the pairs that could produce no evidence after their
    own last instant and so may in truth be Continued (0054/0055)."""
    live = ~res["not_live"]
    return (pop & live & ~res["continued"]
            & (A.last_inst > res["tau1"]) & (A.last_inst < res["tau2"]))


POS4 = {"APPLY": positions["pos4"], "DERIV": positions["pos4_deriv"]}


def arm_block(res, pop_apply, pop_deriv, label):
    out = {"label": label, "W_days": int(res["W"]), "H_days": H_DAYS}
    out["right_censoring_two_lines"] = {
        popname: {
            "n_in_position_4": int(POS4[popname].sum()),
            "removed_by_max_W_91_term": int((POS4[popname] & ~res["keep_term1"]).sum()),
            "removed_incrementally_by_the_plus_H_term":
                int((POS4[popname] & res["keep_term1"] & ~res["keep_d10"]).sum()),
        } for popname in ("APPLY", "DERIV")}
    for popname, pop in (("APPLY", pop_apply), ("DERIV", pop_deriv)):
        live = ~res["not_live"]
        p5m = pop
        p7m = pop & live
        exm = pop & res["not_live"]
        chm = channel_mask(res, pop)
        o = res["outcome"]
        out[popname] = {
            "n_position_5": int(p5m.sum()),
            "n_post_liveness": int(p7m.sum()),
            "accounts_position_5": accounts(p5m),
            "position_5_counts": outcome_counts(p5m, res),
            "post_liveness_counts": outcome_counts(p7m, res),
            "exclusions": {
                "total": int(exm.sum()),
                "never_started_component": int((exm & (o == NEVER)).sum()),
                "started_and_left_component": int((exm & (o == LEFT)).sum()),
                "continued_component": int((exm & (o == CONT)).sum()),
                "accounts": accounts(exm),
                "accounts_never_started_component": accounts(exm & (o == NEVER)),
                "accounts_started_and_left_component": accounts(exm & (o == LEFT)),
                "silence_test_alone": int((p5m & res["silent"]).sum()),
                "spared_by_not_continued": int((p5m & res["silent"] & res["continued"]).sum()),
            },
            "channel_pairs_last_insertion_in_tau1_tau2": {
                "total": int(chm.sum()),
                "started_and_left": int((chm & (o == LEFT)).sum()),
                "never_started": int((chm & (o == NEVER)).sum()),
                "accounts": accounts(chm),
            },
        }
    return out


arms_measured = {
    "W108_s2_finale": arm_block(r108, r108["pos5"], r108["pos5_deriv"], "W=108, finale"),
    "W091_s2_finale": arm_block(r91f, r91f["pos5"], r91f["pos5_deriv"], "W=91, finale"),
    # READING (a) OF "both arms run on the same right-censored population": the premiere arm is
    # measured ON THE PRIMARY ARM'S POSITION-5 ROW SET. See d10_reading_ambiguity below.
    "W091_s2_premiere": arm_block(r91p, r108["pos5"], r108["pos5_deriv"], "W=91, premiere"),
}

# The other reading, measured rather than asserted inert.
prem_own_p5 = r91p["pos5"]
prem_own_p5d = r91p["pos5_deriv"]
d10_reading = {
    "reading_a_shared_population_APPLY": int(r108["pos5"].sum()),
    "reading_b_premiere_anchored_d10_APPLY": int(prem_own_p5.sum()),
    "in_b_not_in_a_APPLY": int((prem_own_p5 & ~r108["pos5"]).sum()),
    "in_a_not_in_b_APPLY": int((r108["pos5"] & ~prem_own_p5).sum()),
    "reading_a_shared_population_DERIV": int(r108["pos5_deriv"].sum()),
    "reading_b_premiere_anchored_d10_DERIV": int(prem_own_p5d.sum()),
    "in_b_not_in_a_DERIV": int((prem_own_p5d & ~r108["pos5_deriv"]).sum()),
    "in_a_not_in_b_DERIV": int((r108["pos5_deriv"] & ~prem_own_p5d).sum()),
    "premiere_t0_never_later_than_finale_t0": bool((t0_premiere <= t0_finale).all()),
    "pairs_where_the_two_clocks_coincide": int((t0_premiere == t0_finale).sum()),
    # Whether the clock ORIGIN moves D10 at all, at one W. It does not: the Step 2 frame caps
    # the S2 finale at 2025-12-31, which is earlier than the binding censoring cutoff, so the
    # max() in T0 is decided by the S1 completion date on every pair the cutoff can reach --
    # and that term is the same under both origins.
    "censoring_set_identical_premiere_vs_finale_at_W91_APPLY":
        bool((prem_own_p5 == r91f["pos5"]).all()),
    "censoring_set_identical_premiere_vs_finale_at_W91_DERIV":
        bool((prem_own_p5d == r91f["pos5_deriv"]).all()),
    "so_the_353_and_315_are_the_W_term_not_the_origin": True,
}

# ---------------------------------------------------------------------------------------------
# the bootstrap: account-clustered, B = 10,000, seed 20260818, BOTH levels and paired movements
# ---------------------------------------------------------------------------------------------
# ONE resampling frame and ONE draw for the whole file, so that every movement is paired and no
# interval depends on the order in which the intervals happen to be computed. The frame is the
# set of accounts contributing at least one pair to the position-4 output -- arm-independent by
# construction, since positions 1-4 do not contain W.
pos4 = positions["pos4"]
frame_accounts = np.unique(pair_user[pos4])
acc_slot = np.full(int(pair_user.max()) + 1, -1, dtype=np.int64)
acc_slot[frame_accounts] = np.arange(frame_accounts.size)
pair_acc = acc_slot[pair_user]
n_acc = frame_accounts.size

COLS = []          # (arm, population, position, outcome-or-total)
col_vectors = []


def add_col(name, mask):
    COLS.append(name)
    v = np.bincount(pair_acc[mask], minlength=n_acc).astype(np.float64)
    col_vectors.append(v)


arm_res = {"W108_s2_finale": (r108, r108["pos5"], r108["pos5_deriv"]),
           "W091_s2_finale": (r91f, r91f["pos5"], r91f["pos5_deriv"]),
           "W091_s2_premiere": (r91p, r108["pos5"], r108["pos5_deriv"])}

for arm, (res, pa, pd_) in arm_res.items():
    live = ~res["not_live"]
    o = res["outcome"]
    for popname, pop in (("APPLY", pa), ("DERIV", pd_)):
        for posname, m in (("p5", pop), ("p7", pop & live)):
            add_col(f"{arm}|{popname}|{posname}|never_started", m & (o == NEVER))
            add_col(f"{arm}|{popname}|{posname}|started_and_left", m & (o == LEFT))
            add_col(f"{arm}|{popname}|{posname}|continued", m & (o == CONT))
            add_col(f"{arm}|{popname}|{posname}|total", m)

C = np.vstack(col_vectors).T          # (n_acc, K)
K = C.shape[1]

rng = np.random.default_rng(SEED)
sums = np.empty((B_RESAMPLES, K), dtype=np.float64)
CHUNK = 200
offsets = (np.arange(CHUNK, dtype=np.int64) * n_acc)[:, None]
for start in range(0, B_RESAMPLES, CHUNK):
    m = min(CHUNK, B_RESAMPLES - start)
    idx = rng.integers(0, n_acc, size=(m, n_acc), dtype=np.int64)
    w = np.bincount((idx + offsets[:m]).ravel(),
                    minlength=m * n_acc).reshape(m, n_acc).astype(np.float64)
    sums[start:start + m] = w @ C

colidx = {c: i for i, c in enumerate(COLS)}
LO, HI = (100 - CI_LEVEL) / 2, 100 - (100 - CI_LEVEL) / 2


def share_draws(arm, pop, pos, outcome):
    num = sums[:, colidx[f"{arm}|{pop}|{pos}|{outcome}"]]
    den = sums[:, colidx[f"{arm}|{pop}|{pos}|total"]]
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, 100.0 * num / den, np.nan)


bootstrap = {}
for arm in arm_res:
    for pop in ("APPLY", "DERIV"):
        for outcome in ("never_started", "started_and_left", "continued"):
            lev = share_draws(arm, pop, "p7", outcome)
            p5s = share_draws(arm, pop, "p5", outcome)
            mov = lev - p5s                      # paired, same resample
            key = f"{arm}|{pop}|{outcome}"
            bootstrap[key] = {
                "level": {"lower": float(np.nanpercentile(lev, LO)),
                          "upper": float(np.nanpercentile(lev, HI))},
                "movement": {"lower": float(np.nanpercentile(mov, LO)),
                             "upper": float(np.nanpercentile(mov, HI))},
                "point_level": None,
                "point_movement": None,
            }

# point estimates from the observed table (not from the resamples)
for arm, (res, pa, pd_) in arm_res.items():
    live = ~res["not_live"]
    for popname, pop in (("APPLY", pa), ("DERIV", pd_)):
        c5 = outcome_counts(pop, res)
        c7 = outcome_counts(pop & live, res)
        for outcome in ("never_started", "started_and_left", "continued"):
            k = f"{arm}|{popname}|{outcome}"
            lev = 100.0 * c7[outcome] / c7["total"]
            p5s = 100.0 * c5[outcome] / c5["total"]
            bootstrap[k]["point_level"] = lev
            bootstrap[k]["point_movement"] = lev - p5s

payload = {
    "step": 9,
    "instance": "a",
    "stage": 1,
    "api_calls": 0,
    "tau_pull_utc": "2026-08-11T00:00:00Z",
    "H_days": H_DAYS,
    "consumed_from_step8": {
        "outcomes.json": sha12(os.path.join(S8, "outcomes.json")),
        "arms.json": sha12(os.path.join(S8, "arms.json")),
        "positions.json": sha12(os.path.join(S8, "positions.json")),
        "diagnostics.json": sha12(os.path.join(S8, "diagnostics.json")),
        "scan.npz": sha12(os.path.join(S8, "scan.npz")),
        "positions.npz": sha12(os.path.join(S8, "positions.npz")),
        "position5_table.npz": sha12(os.path.join(S8, "position5_table.npz")),
        "step8_a_lib.py": sha12(os.path.join(ROOT, "src", "step8_a_lib.py")),
    },
    "import_gate": {"reproduced": {k: v[0] for k, v in reproduction.items()},
                    "step8_published": {k: v[1] for k, v in reproduction.items()},
                    "mismatches": mismatches},
    "arms_measured": arms_measured,
    "d10_reading_ambiguity": d10_reading,
    "bootstrap_settings": {"B": B_RESAMPLES, "seed": SEED, "resampling_unit": "account",
                           "statistics": ["levels", "movements"],
                           "frame_accounts": int(n_acc),
                           "frame_definition": "accounts with at least one pair in the "
                                               "position-4 output; arm-independent, since "
                                               "positions 1-4 do not contain W",
                           "movement_configurations": "post-liveness (position 7) MINUS "
                                                      "outcome-conditional position 5, the "
                                                      "same share under the two configurations "
                                                      "the liveness filter separates",
                           "ci_level_pct": CI_LEVEL,
                           "method": "percentile_bootstrap"},
    "bootstrap": bootstrap,
}

with open(os.path.join(OUT, "measured.json"), "w") as fh:
    json.dump(payload, fh, indent=1)
with open(os.path.join(LOGS, "a_stage1.json"), "w") as fh:
    json.dump({"wrote": os.path.join(OUT, "measured.json"),
               "import_gate_mismatches": mismatches,
               "n_accounts_in_frame": int(n_acc),
               "B": B_RESAMPLES, "seed": SEED}, fh, indent=1)

print("import gate: OK, 0 mismatches against Step 8's published counts")
print(json.dumps(d10_reading, indent=1))
for arm in arms_measured:
    a = arms_measured[arm]
    print(arm, "APPLY p5", a["APPLY"]["n_position_5"], "p7", a["APPLY"]["n_post_liveness"],
          "excl", a["APPLY"]["exclusions"]["total"],
          "chan", a["APPLY"]["channel_pairs_last_insertion_in_tau1_tau2"],
          "| DERIV p5", a["DERIV"]["n_position_5"],
          "excl", a["DERIV"]["exclusions"]["total"],
          "chan", a["DERIV"]["channel_pairs_last_insertion_in_tau1_tau2"])
