"""Step 7 RERUN ON THE ADOPTED RULE (instance b, namespace alt2_b) -- stage 4.

Two things.

(1) THE WATERFALL, with line 6 reported OUTCOME-CONDITIONAL (decisions/0046
    Sec 5). Positions 1 and 2 of the Step 8 order belong to Step 8 and are not
    rebuilt here; positions 3 to 6 are measured, and position 7 is recorded as
    an annotation that removes no rows. The monotone-decrease invariant is
    reported as strict or non-strict per line and per population.

(2) THE MECHANISM behind the DERIV zero, tested rather than repeated. 0046
    Sec 1 calls the zero "forced by construction -- line 4 requires S2
    evidence, so no line-4 pair can have |A| = 0 and no S2 record." That
    argument forecloses only the pairs with NO S2 record. A pair whose S2
    evidence is all dated at or after tau1 has |A| = 0 WITH S2 evidence, and
    9,145 such pairs sit on DERIV at W = 108. For one of them to be excluded it
    would additionally need its account silent after tau1 -- i.e. an S2 record
    whose claimed watched_at postdates its own insertion instant. This stage
    measures how many records are future-dated in that sense, which is what
    decides whether the zero is structural or merely observed.

ZERO network calls. Reads only.

Out: processed/step7/alt2_b/waterfall.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
OUT = ROOT / "processed" / "step7" / "alt2_b"
MISSING = np.iinfo(np.int64).min
W, H, DAY = 108, 91, 86400.0


def insert_time(rid, knot_rid, knot_time):
    return np.interp(rid.astype(np.float64), knot_rid, knot_time)


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    rule = json.load(open(OUT / "rule.json"))
    res: dict = {"instance": "data-scientist-b", "namespace": "alt2_b", "stage": 4,
                 "api_calls": 0, "adopts": "nothing", "W": W, "H": H}

    # ---------------- (1) waterfall ----------------
    frame = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_L"])
    res["shows_in_frame"] = int(len(frame))
    res["shows_with_L2_eq_1_in_frame"] = int((frame.s2_L.values == 1).sum())

    p = pd.read_csv(P5 / "pair_revision5.csv", usecols=["user_idx", "show_trakt_id"])
    s1_completer_pairs = int(len(p))

    lines = {}
    for popname in ("APPLY", "DERIV"):
        a = rule["by_population"][popname]["108"]
        n5 = a["n_before_liveness"]
        ex = a["excluded_pairs"]
        n6 = n5 - ex
        pre_censor = 201_900 if popname == "APPLY" else 152_126
        lines[popname] = [
            {"position": "1-2", "name": "Step 2 frame, then L2 = 1 exclusion",
             "rows_out": None,
             "note": "owned by Step 8; not rebuilt here. No show in the frame has L2 = 1, "
                     "so position 2 removes nothing on this frame."},
            {"position": 3, "name": "S1 completion rule", "rows_out": s1_completer_pairs,
             "note": "the Step 5 pair table's row count; Step 2 + Step 1 Sec 4"},
            {"position": 4, "name": "contamination exclusion (Step 5)", "rows_out": pre_censor,
             "note": "Step 5 line 1 (201,900) for APPLY; line 4 (152,126) for DERIV. "
                     "DERIV additionally requires S2 evidence and clean first-S2 timing, "
                     "which is why it is not a Step 8 position"},
            {"position": 5, "name": "right-censoring D10 at W = 108", "rows_out": n5},
            {"position": 6, "name": "liveness (adopted rule)", "rows_out": n6,
             "removed": ex,
             "OUTCOME_CONDITIONAL": True,
             "note": "line 6's removal count is conditional on the position-5 outcome "
                     "annotation, because the rule's second conjunct is |A| = 0. Reported "
                     "as such per 0046 Sec 5; |A| and liveness are row-local predicates on "
                     "the position-5 output and commute exactly, so the final row set does "
                     "not depend on which is read first"},
            {"position": 7, "name": "outcome assignment at tau1 and tau2", "rows_out": n6,
             "removed": 0,
             "note": "an annotation, not a filter -- contributes no waterfall line"},
        ]
        counts = [s1_completer_pairs, pre_censor, n5, n6, n6]
        strict = all(b < a_ for a_, b in zip(counts, counts[1:-1] + [counts[-1]]))
        lines[popname + "_monotone"] = {
            "non_strict_holds": all(b <= a_ for a_, b in zip(counts, counts[1:])),
            "strict_at_line_6": ex > 0,
            "strict_everywhere_through_line_6": bool(strict and ex > 0),
            "statement": ("monotone decrease holds STRICTLY at line 6 on APPLY (604 rows "
                          "removed)" if ex > 0 else
                          "monotone decrease holds ONLY NON-STRICTLY at line 6 on DERIV "
                          "(0 rows removed; the count is unchanged)"),
        }
        lines[popname + "_final_states"] = a["under_rule"]
    res["waterfall"] = lines

    # ---------------- (2) mechanism ----------------
    cal = np.load(P5 / "calibration.npz")
    z = np.load(P5 / "full_scan.npz")
    tau_rec = insert_time(z["rid"], cal["knot_rid"], cal["knot_time"])
    ts = z["ts"]
    user = z["user"]
    season = z["season"]
    show = z["show"]
    dated = ts != MISSING
    future = dated & (ts.astype(np.float64) > tau_rec)
    res["future_dated_records"] = {
        "definition": "a record whose claimed watched_at is later than its own calibrated "
                      "insertion instant",
        "records_dated": int(dated.sum()),
        "future_dated": int(future.sum()),
        "share_pct": 100.0 * int(future.sum()) / int(dated.sum()),
        "future_dated_S2_records": int((future & (season == 2)).sum()),
        "max_future_dating_days": float(
            ((ts.astype(np.float64) - tau_rec)[future].max() / DAY)) if future.any() else None,
    }

    # per-pair: does the pair hold an S2 record dated after its account's LAST insertion?
    n_users = int(user.max()) + 1
    max_inst = np.full(n_users, -np.inf)
    np.maximum.at(max_inst, user, tau_rec)
    m = (season == 2) & dated & (ts.astype(np.float64) > max_inst[user])
    key_pairs = set(zip(show[m].tolist(), user[m].tolist()))
    del z, tau_rec, ts, user, season, show
    line1_keys = set(zip(pz["show_trakt_id"].tolist(), pz["user_idx"].tolist()))
    hits = key_pairs & line1_keys
    res["mechanism_DERIV_zero"] = {
        "line4_pairs_never_started_at_W108": rule["claims_tested"]
            ["C1_mechanism_at_W108_DERIV"]["pairs_with_A_empty"],
        "line4_pairs_with_no_S2_record_anywhere": rule["claims_tested"]
            ["C1_mechanism_at_W108_DERIV"]["pairs_with_no_S2_record_anywhere"],
        "line1_pairs_holding_an_S2_record_dated_after_the_account_last_insertion":
            int(len(hits)),
        "reading": (
            "0046's 'forced by construction' argument covers only pairs with NO S2 record. "
            "A line-4 pair CAN have |A| = 0 while holding S2 evidence dated at or after "
            "tau1 -- 9,145 do at W = 108. Excluding one of those would additionally require "
            "the account to be silent after tau1 while holding a record claiming a watch "
            "after tau1, i.e. a record dated after its own insertion instant. The count of "
            "line-1 pairs where that arises at all is reported above. Where it is zero, the "
            "DERIV zero is structural given the calibration; where it is not, the zero is "
            "an observed fact at these arms and not an identity."),
    }

    res["elapsed_s"] = time.time() - t
    (OUT / "waterfall.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2)[:4000])


if __name__ == "__main__":
    main()
