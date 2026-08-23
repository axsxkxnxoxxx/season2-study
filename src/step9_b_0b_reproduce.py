"""Step 9, arm `b`: reproduction of the premiere-clock unit defect, and of its correction.

A FIX ASSERTED TO WORK IS NOT A FIX. This runs the corrected checks against the exact vector the
defective expression produces from the frame ON DISK NOW, and shows that they are REJECTED; then
against the corrected vector, and shows that they are ACCEPTED. It also runs the three
preconditions the corrected build removes, on the SAME wrong vector, and shows that they PASS on
it -- which is the whole of the case against them.

BOTH CHECKS ARE DEMONSTRATED, not one. DEF-A (section 2) verifies the premiere EPOCH vector.
T0PRIME-ORDER (section 5) verifies the ORIGIN vector T0' and its ordering against T0, which is
the warrant the deliverable claims when it runs the premiere arm on the adopted arm's row set
without re-censoring it. Section 5 also runs T0PRIME-ORDER's part 2 -- the bare inequality -- on
the defective vector ON ITS OWN, and shows that it passes there: part 2 alone IS the removed
boolean, and part 1's reconstruction is the whole of what makes the replacement failable.

Reads only `processed/step2/frame.csv`, `processed/step8/a/positions.npz` and
`processed/step8/a/scan.npz`. Writes no study figure, adopts nothing, makes zero API calls.
Run record: logs/step9_b_premiere_clock_repro.txt (decisions/0109 -- code in src/, output in logs/).
"""
import datetime
import json
import os
import sys

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
sys.path.insert(0, os.path.join(ROOT, "src"))
import step9_b_0_clock as C                                            # noqa: E402

LOG = os.path.join(ROOT, "logs/step9_b_premiere_clock_repro.txt")
DAY = 86400

frame = pd.read_csv(os.path.join(ROOT, "processed/step2/frame.csv"))
positions = np.load(os.path.join(ROOT, "processed/step8/a/positions.npz"), allow_pickle=True)
scan = np.load(os.path.join(ROOT, "processed/step8/a/scan.npz"), allow_pickle=True)

pair_show = scan["pair_show"]
f = frame.set_index("show_trakt_id")
prem = pd.to_datetime(f["s2_premiere_date"], utc=True)
truth_by_show = f["s2_premiere_date"].to_numpy()
truth_by_pair = f["s2_premiere_date"].reindex(pair_show).to_numpy()

t0_finale = positions["t0"].astype(np.int64)
s1_date = positions["s1_date"].astype(np.int64)

# ---- 1. THE VECTOR AS THE DEFECTIVE EXPRESSION PRODUCES IT, from the frame on disk now --------
# This is the literal expression from the run being corrected:
#   prem_epoch = (prem.astype("int64") // 10 ** 9).reindex(pair_show).to_numpy().astype(int64)
wrong_by_show = np.asarray(prem.astype("int64") // 10 ** 9, dtype=np.int64)
wrong_by_pair = ((prem.astype("int64") // 10 ** 9)
                 .reindex(pair_show).to_numpy().astype(np.int64))
wrong_t0 = np.maximum(wrong_by_pair, s1_date)

# ---- 2. THE CORRECTED CHECK, RUN AGAINST THAT VECTOR ------------------------------------------
rejected = None
try:
    C.verify_premiere_epoch(wrong_by_show, truth_by_show, wrong_by_pair, truth_by_pair)
    rejected = False
except AssertionError as exc:
    rejected = True
    rejection_message = str(exc)
wrong_detail = {
    "by_show": C.def_a_compare(wrong_by_show, truth_by_show, "wrong vector, by show"),
    "by_pair": C.def_a_compare(wrong_by_pair, truth_by_pair, "wrong vector, by pair"),
}

# ---- 3. THE TWO PRECONDITIONS THE CORRECTED BUILD REMOVES, ON THE SAME WRONG VECTOR -----------
TAU_PULL = int(np.datetime64("2026-08-11T00:00:00", "s").astype("int64"))
keep_d10 = (t0_finale + (max(108, 91) + 91) * DAY) <= TAU_PULL
pos5 = positions["pos4"] & keep_d10
pos5d = positions["pos4_deriv"] & keep_d10
wrong_tau2 = wrong_t0 + (91 + 91) * DAY
vacuous_on_the_wrong_vector = {
    "t0_is_earlier_or_equal_for_every_pair": bool((wrong_t0 <= t0_finale).all()),
    "tau2_observable_on_every_retained_pair_APPLY": bool((wrong_tau2[pos5] <= TAU_PULL).all()),
    "tau2_observable_on_every_retained_pair_DERIV": bool((wrong_tau2[pos5d] <= TAU_PULL).all()),
}

# ---- 4. THE CORRECTED VECTOR ------------------------------------------------------------------
right_by_show, prov = C.epoch_seconds(prem)
right_by_pair = pd.Series(right_by_show, index=prem.index).reindex(pair_show).to_numpy()
if np.isnan(np.asarray(right_by_pair, dtype="float64")).any():
    raise AssertionError("HARD STOP: a pair's show is absent from the frame.")
right_by_pair = right_by_pair.astype(np.int64)
accepted = C.verify_premiere_epoch(right_by_show, truth_by_show, right_by_pair, truth_by_pair)
right_t0 = np.maximum((right_by_pair // DAY) * DAY, s1_date)

# ---- 5. T0PRIME-ORDER, THE CHECK BEHIND THE DELIVERABLE'S ORDERING CLAIM -----------------------
# The deliverable says the premiere arm's row set is not re-censored BECAUSE T0' <= T0. The
# boolean that used to check that was removed as vacuous, and a claim of having checked is either
# TRUE or it is REMOVED. T0PRIME-ORDER is the replacement, and the whole question is whether it
# can FAIL. Run here against the same defective vector, then against the corrected one.
tau2_finale = t0_finale + (108 + 91) * DAY
retained = {"APPLY": pos5, "DERIV": pos5d}


def run_t0p(t0p, tau2p, label):
    try:
        res = C.verify_t0_prime_order(
            t0_prime=t0p, t0_finale=t0_finale, premiere_dates_by_pair=truth_by_pair,
            s1_epoch=s1_date, tau2_prime=tau2p, tau2_finale=tau2_finale,
            tau_pull=TAU_PULL, retained=retained)
        return {"vector": label, "rejected": False, "message": None, "result": res}
    except AssertionError as exc:
        return {"vector": label, "rejected": True, "message": str(exc), "result": None}


wrong_t0_floored = np.maximum((wrong_by_pair // DAY) * DAY, s1_date)
t0p_wrong = run_t0p(wrong_t0_floored, wrong_t0_floored + (91 + 91) * DAY, "the DEFECTIVE vector")
t0p_right = run_t0p(right_t0, right_t0 + (91 + 91) * DAY, "the CORRECTED vector")

# WHY IT FAILS AND THE OLD BOOLEAN DID NOT, shown side by side on the same vector. The bare
# inequality is TRUE on the defective vector; part 1's reconstruction is not.
t0p_side_by_side = {
    "the_removed_boolean_on_the_defective_vector":
        bool((wrong_t0_floored <= t0_finale).all()),
    "T0PRIME_ORDER_part_2_on_the_defective_vector_would_also_pass":
        bool((wrong_t0_floored <= t0_finale).all()),
    "what_part_1_sees": {
        "pairs_where_the_defective_T0_prime_decodes_to_the_S1_completion_date":
            int((wrong_t0_floored == s1_date).sum()),
        "pairs_where_the_corrected_T0_prime_is_the_premiere_date":
            int((right_t0 == (right_by_pair // DAY) * DAY).sum()),
    },
    "verdict": "part 2 alone reproduces the vacuous boolean exactly -- it passes on a vector "
               "that is wrong in every entry. PART 1 IS WHAT FAILS, because it reconstructs T0' "
               "from the frame's own date strings, which the epoch conversion never touches.",
}

report = {
    "what": "reproduction of the premiere-clock unit defect and of its correction",
    "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"),
    "frame_on_disk": {"rows": int(len(f)), "column": "s2_premiere_date",
                      "dtype_after_to_datetime": str(prem.dtype)},
    "1_defective_expression": {
        "expression": 'prem.astype("int64") // 10 ** 9',
        "why_it_is_wrong": "10 ** 9 is a claim about datetime64[ns]; the column resolves at %s"
                           % prov["resolution_read_off_the_dtype"],
        "first_three_values": [int(x) for x in wrong_by_show[:3]],
        "decodes_to": [str(d) for d in
                       np.asarray(wrong_by_show[:3]).astype("datetime64[s]")],
        "distinct_calendar_days_it_produces": int(np.unique(wrong_by_show // DAY).size),
        "pairs_where_the_wrong_T0_equals_the_S1_completion_date":
            int((wrong_t0 == s1_date).sum()),
        "pairs_total": int(wrong_t0.size),
    },
    "2_corrected_check_against_that_vector": {
        "rejected": rejected,
        "message": rejection_message if rejected else None,
        "detail": wrong_detail,
    },
    "3_removed_preconditions_run_on_that_same_wrong_vector": {
        "results": vacuous_on_the_wrong_vector,
        "verdict": "all three return True on a vector that is wrong in every entry; they are "
                   "guaranteed by T0' collapsing onto the S1 completion date and cannot fail",
    },
    "4_corrected_vector": {
        "conversion_provenance": prov,
        "def_a": accepted,
        "first_three_values": [int(x) for x in right_by_show[:3]],
        "decodes_to": [str(d) for d in
                       np.asarray(right_by_show[:3]).astype("datetime64[s]")],
        "pairs_where_the_corrected_T0_equals_the_S1_completion_date":
            int((right_t0 == s1_date).sum()),
        "pairs_where_the_corrected_T0_is_the_premiere_date":
            int((right_t0 == right_by_pair).sum()),
        "pairs_where_the_two_T0_vectors_differ": int((wrong_t0 != right_t0).sum()),
    },
    "5_t0prime_order": {
        "what_it_is": "the check behind the deliverable's claim that the premiere arm's row set "
                      "need not be re-censored. It replaces the removed boolean "
                      "t0_is_earlier_or_equal_for_every_pair, and the point of the "
                      "reconstruction in its part 1 is that it CAN FAIL where that boolean "
                      "could not.",
        "on_the_defective_vector": {
            "rejected": t0p_wrong["rejected"],
            "message": t0p_wrong["message"],
        },
        "on_the_corrected_vector": {
            "rejected": t0p_right["rejected"],
            "part_1": t0p_right["result"]["part_1_reconstruction"] if t0p_right["result"] else None,
            "part_2": t0p_right["result"]["part_2_ordering"] if t0p_right["result"] else None,
            "part_3": t0p_right["result"]["part_3_observability"] if t0p_right["result"] else None,
            "total_rows_compared":
                t0p_right["result"]["total_rows_compared"] if t0p_right["result"] else None,
        },
        "why_it_fails_where_the_boolean_did_not": t0p_side_by_side,
    },
}

verdict_ok = (rejected is True
              and accepted["by_show"]["passes"] and accepted["by_pair"]["passes"]
              and all(vacuous_on_the_wrong_vector.values())
              and t0p_wrong["rejected"] is True and t0p_right["rejected"] is False)
report["verdict"] = {
    "corrected_check_rejects_the_wrong_vector": rejected,
    "corrected_check_accepts_the_corrected_vector": True,
    "removed_preconditions_pass_on_the_wrong_vector": all(
        vacuous_on_the_wrong_vector.values()),
    "t0prime_order_rejects_the_wrong_vector": t0p_wrong["rejected"],
    "t0prime_order_accepts_the_corrected_vector": not t0p_right["rejected"],
    "t0prime_order_part_2_alone_would_pass_on_the_wrong_vector":
        t0p_side_by_side["T0PRIME_ORDER_part_2_on_the_defective_vector_would_also_pass"],
    "reproduction_complete": bool(verdict_ok),
}

text = json.dumps(report, indent=1)
with open(LOG, "w") as fh:
    fh.write("step9 arm b -- premiere-clock defect reproduction\n")
    fh.write("generator: src/step9_b_0b_reproduce.py\n")
    fh.write("api calls: 0; adopts nothing; no study figure written\n\n")
    fh.write(text + "\n")
print(text)
if not verdict_ok:
    raise SystemExit("reproduction did not complete as stated")
