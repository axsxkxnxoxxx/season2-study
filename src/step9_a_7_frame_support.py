"""Step 9, arm `a`, stage 7: THE RESAMPLING FRAME'S SUPPORT, MEASURED PER ARM AND PER POPULATION.

decisions/0124 constraint (i): a frame that is arm-independent in MEMBERSHIP is not
arm-independent in SUPPORT. `keep_d10` contains `max(W, 91)`, so the CONTRIBUTING subset moves
with `W` even when the drawn frame does not, and any field declaring the frame arm-independent
must say it describes the DRAW and not the SUPPORT.

Before this script there was no per-arm contributing-account count anywhere in this arm's output,
so nothing published could have distinguished the two even with the wording fixed. This script
measures it, once, in one place.

  MEMBERSHIP = every account with at least one pair in the POSITION-4 output. Built once by
               stage 1, drawn for every quantity regardless of how much it contributes.
  SUPPORT    = the subset of that membership carrying at least one pair in the population a
               given quantity is measured on. It is NOT the frame, it is not resampled, and it
               is not used to select who is drawn: it is a description of the drawn frame.

INPUT is stage 1's emitted column matrix, `processed/step9/a/boot_columns.npz`, which is the
SAME object the published intervals were computed from. THE BOOTSTRAP IS NOT RE-RUN and no
replicate is drawn here: the support is a property of `C`, not of the weights.

THE PRECONDITION IS A SET-MEMBERSHIP TEST, NOT A RANGE TEST (decisions/0123 SS3). Asking only
that a count lands in [0, n_frame] cannot fail on a mis-keyed column -- every wrong answer is
also in that interval. So each measured support is checked by summing the SAME column over the
contributing accounts and requiring the total to equal the population size this arm PUBLISHED
for that arm and population, read from the file. The negative control substitutes a different
arm's column and requires the equality to BREAK, so the check is shown rejecting before it is
trusted passing.

Zero API calls. Writes processed/step9/a/frame_support.json and logs/step9/a_stage7.json.
Writes nothing to artifacts/.
"""
import datetime as dt
import hashlib
import json
import os
import sys

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed", "step9", "a")
LOGS = os.path.join(ROOT, "logs", "step9")
os.makedirs(LOGS, exist_ok=True)

MEAS = json.load(open(os.path.join(OUT, "measured.json")))
cz = np.load(os.path.join(OUT, "boot_columns.npz"))
C = cz["C"]
COLS = [str(c) for c in cz["cols"]]
colidx = {c: i for i, c in enumerate(COLS)}

wz = np.load(os.path.join(OUT, "boot_weights.npz"))
N_FRAME = int(wz["n_frame"])

# The arm keys and populations are READ from the measurement file, never typed here: a typed
# list is a second definition of which arms this file measured.
ARM_KEYS = list(MEAS["arms_measured"].keys())
POPS = ["APPLY", "DERIV"]

assert C.shape[0] == N_FRAME, (C.shape, N_FRAME)


def sha12(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def published_n(arm, pop, pos):
    """The population size this arm PUBLISHED for (arm, pop, pos), read from measured.json."""
    blk = MEAS["arms_measured"][arm][pop]
    return int(blk["n_position_5"] if pos == "p5" else blk["n_post_liveness"])


failures = []
support = {}
for arm in ARM_KEYS:
    for pop in POPS:
        for pos in ("p5", "p7"):
            col = C[:, colidx[f"{arm}|{pop}|{pos}|total"]]
            contributing_mask = col > 0
            n_contrib = int(contributing_mask.sum())
            pairs_over_contributors = int(col[contributing_mask].sum())
            want = published_n(arm, pop, pos)
            ok = pairs_over_contributors == want
            if not ok:
                failures.append(
                    f"{arm}|{pop}|{pos}: the column summed over its {n_contrib} contributing "
                    f"accounts gives {pairs_over_contributors}, and this arm published {want}"
                )
            support[f"{arm}|{pop}|{pos}"] = {
                "frame_membership_accounts": N_FRAME,
                "contributing_accounts": n_contrib,
                "drawn_and_contributing_zero": N_FRAME - n_contrib,
                "pairs_in_this_population": pairs_over_contributors,
                "checked_against_published_n": want,
                "check": "set membership: the same column summed over the accounts it marks as "
                         "contributing must equal the population size published for this arm "
                         "and population. A range test on the account count cannot fail on a "
                         "mis-keyed column; this can, and the negative control below shows it "
                         "doing so.",
                "check_passed": ok,
            }

# ---------------------------------------------------------------------------------------------
# NEGATIVE CONTROL -- the check is shown REJECTING a wrong vector before it is trusted passing.
# Substitute one arm's column for another's wherever the two populations differ in size, and
# require the equality to break. If no substitution can break it, this control has proved
# nothing and must FAIL rather than pass quietly.
# ---------------------------------------------------------------------------------------------
neg_attempts, neg_rejected = 0, 0
neg_detail = []
for pop in POPS:
    for pos in ("p5", "p7"):
        for i, arm_i in enumerate(ARM_KEYS):
            for arm_j in ARM_KEYS[i + 1:]:
                want_i = published_n(arm_i, pop, pos)
                want_j = published_n(arm_j, pop, pos)
                if want_i == want_j:
                    continue                      # cannot discriminate; not counted as a trial
                col_j = C[:, colidx[f"{arm_j}|{pop}|{pos}|total"]]
                got = int(col_j[col_j > 0].sum())
                neg_attempts += 1
                if got != want_i:
                    neg_rejected += 1
                else:
                    neg_detail.append(f"{arm_j}'s column passed as {arm_i}'s at {pop}|{pos}")
neg_ok = neg_attempts > 0 and neg_rejected == neg_attempts
if not neg_ok:
    failures.append(
        f"negative control: {neg_attempts} discriminating substitution(s), {neg_rejected} "
        f"rejected. A precondition that cannot fail on the vector it polices is not a check"
    )

# Constraint (i) itself, measured rather than asserted: membership constant across arms, support
# not. If the support did NOT move, the wording would be making a distinction with no content
# here, and that too is worth knowing rather than assuming.
membership_constant = len({s["frame_membership_accounts"] for s in support.values()}) == 1
support_moves_with_arm = {
    pop: len({support[f"{a}|{pop}|p5"]["contributing_accounts"] for a in ARM_KEYS}) > 1
    for pop in POPS
}

payload = {
    "step": 9, "instance": "a", "stage": 7, "api_calls": 0,
    "decision": "0124 constraint (i)",
    "generated_by": os.path.abspath(__file__),
    "generated_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "read_from": {
        "processed/step9/a/boot_columns.npz": sha12(os.path.join(OUT, "boot_columns.npz")),
        "processed/step9/a/boot_weights.npz": sha12(os.path.join(OUT, "boot_weights.npz")),
        "processed/step9/a/measured.json": sha12(os.path.join(OUT, "measured.json")),
    },
    "bootstrap_rerun": False,
    "what_membership_is": "every account with at least one pair in the position-4 output, built "
                          "once and drawn for every quantity regardless of how much it "
                          "contributes (decisions/0124). Accounts the censoring rule excludes "
                          "are part of the population the uncertainty is ABOUT.",
    "what_support_is": "the subset of that membership with at least one pair in the population "
                       "a quantity is measured on. It describes the draw; it does not select "
                       "it.",
    "frame_membership_accounts": N_FRAME,
    "membership_is_constant_across_arms": membership_constant,
    "support_moves_across_arms_on_position_5": support_moves_with_arm,
    "support": support,
    "negative_control": {
        "what": "one arm's column offered as another's wherever the two published population "
                "sizes differ",
        "discriminating_substitutions": neg_attempts,
        "rejected": neg_rejected,
        "passed_when_it_should_not_have": neg_detail,
        "ok": neg_ok,
    },
    "failures": failures,
    "exit": 1 if failures else 0,
}

with open(os.path.join(OUT, "frame_support.json"), "w") as fh:
    json.dump(payload, fh, indent=1)
with open(os.path.join(LOGS, "a_stage7.json"), "w") as fh:
    json.dump(payload, fh, indent=1)

for k, v in support.items():
    print(f"{k:34s} membership {v['frame_membership_accounts']:,}  contributing "
          f"{v['contributing_accounts']:,}  zero {v['drawn_and_contributing_zero']:,}  "
          f"pairs {v['pairs_in_this_population']:,}  check {'ok' if v['check_passed'] else 'FAIL'}")
print(f"\nnegative control: {neg_rejected}/{neg_attempts} discriminating substitutions rejected")
print(f"membership constant across arms: {membership_constant}; "
      f"support moves across arms (position 5): {support_moves_with_arm}")
sys.exit(1 if failures else 0)
