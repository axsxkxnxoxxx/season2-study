"""Step 7 RERUN on the ADOPTED rule (decisions/0046), namespace `a`. STAGE 4 of 5.

THE RULE
  NOT LIVE iff  (no insertion instant after tau1)  AND  (|A| = 0).
  |A| = 0 is Step 1 SS7's Never-started condition, NOT "no S2 evidence at all".

Computed on BOTH populations at every W arm, with every figure tagged by population:
  DERIV  line 4 less D10        APPLY  line 1 less D10
D10 contains W (it is [[T0]] + (max(W,91)+H)*24h <= tau_pull) and runs at filter position 5,
BEFORE liveness at position 6, so the population is re-derived at each arm. The arm table is
also reported with D10 frozen at the adopted W = 108, because the two readings differ and the
spec does not settle which the per-arm exclusion count means.

Outcome assignment (Step 1 SS7 as amended by 0034) at two instants:
  never      |A| = 0                                                   (tested at tau1)
  continued  |A| >= 1 and F2 in A_H and |A_H| >= ceil(0.90 * L2)       (A_H tested at tau2)
  left       |A| >= 1 and not continued

Zero API calls.
"""
import json
import math
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/alt2_a")

SEC_PER_DAY = 86400.0
H_DAYS = 91
W_ADOPTED = 108
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)
# decisions/0046 SS3 table arms, plus the Step 13 span endpoints (decisions/0027)
ARMS = [38, 46, 60, 77, 91, 100, 107, 108, 125, 150, 180, 213]
STATES = ["never_started", "continued", "started_and_left"]


def main():
    pop = np.load(os.path.join(OUT, "population.npz"))
    epz = np.load(os.path.join(OUT, "episodes_line1.npz"))
    li = np.load(os.path.join(OUT, "last_instant.npz"))

    rows = epz["pair_row"]                 # line-1 rows, in pair_revision5 order
    n = rows.size
    assert n == 201900
    user = epz["user_idx"]
    L2 = epz["L2"]
    ep_row, ep_ts, ep_is_f2 = epz["ep_row"], epz["ep_ts"], epz["ep_is_f2"]
    t0f = pop["t0_floor"][rows]
    line4 = pop["line4"][rows]
    has_s2 = pop["has_s2"][rows]
    assert not np.isnan(t0f).any()

    uids, last = li["uids"], li["last_inst"]
    slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    slot[uids] = np.arange(uids.size)
    assert (slot[user] >= 0).all(), "a population account has no insertion sequence"
    last_inst = last[slot[user]]

    need = np.ceil(0.90 * L2).astype(np.int64)
    n_ep_total = np.bincount(ep_row, minlength=n)
    zero_ep = n_ep_total == 0

    def outcomes(W):
        tau1 = t0f + W * SEC_PER_DAY
        tau2 = t0f + (W + H_DAYS) * SEC_PER_DAY
        selA = ep_ts < tau1[ep_row]
        selH = ep_ts < tau2[ep_row]
        nA = np.bincount(ep_row[selA], minlength=n)
        nAH = np.bincount(ep_row[selH], minlength=n)
        f2_in_AH = np.bincount(ep_row[selH & ep_is_f2], minlength=n) > 0
        never = nA == 0
        cont = (nA >= 1) & f2_in_AH & (nAH >= need)
        left = (nA >= 1) & ~cont
        assert (never.astype(np.int8) + cont + left == 1).all(), "states not a partition"
        assert (nA <= nAH).all(), "A subset of A_H violated (code check)"
        assert (nAH <= L2).all(), "distinct episodes exceed season length"
        no_after = last_inst <= tau1
        return never, cont, left, no_after, nA

    def d10(W):
        return t0f + (max(W, 91) + H_DAYS) * SEC_PER_DAY <= TAU_PULL

    k10_adopted = d10(W_ADOPTED)
    assert int((line4 & k10_adopted).sum()) == 147370
    assert int(k10_adopted.sum()) == 196654

    arms = {}
    for W in ARMS:
        never, cont, left, no_after, nA = outcomes(W)
        ex = no_after & never                      # THE RULE
        assert int((ex & ~never).sum()) == 0, "exclusion set must be a subset of never-started"
        row = {}
        for label, k10 in (("D10_per_arm", d10(W)), ("D10_frozen_at_W108", k10_adopted)):
            pops = {"DERIV": line4 & k10, "APPLY": k10}
            row[label] = {}
            for nm, m in pops.items():
                e = ex & m
                row[label][nm] = {
                    "population_pairs": int(m.sum()),
                    "excluded_pairs": int(e.sum()),
                    "excluded_share_of_population_pct": round(100.0 * e.sum() / m.sum(), 4),
                    "excluded_accounts": int(np.unique(user[e]).size),
                    "excluded_with_S2_evidence_flag": int((e & has_s2).sum()),
                    "excluded_with_zero_in_E2_S2_episodes": int((e & zero_ep).sum()),
                    "never_started_in_population": int((never & m).sum()),
                    "no_insertion_after_tau1_in_population": int((no_after & m).sum()),
                    "PF_LIMIT_would_exclude": int((no_after & m).sum()),
                }
        arms[str(W)] = row
        d = row["D10_per_arm"]
        print(f"W={W:4d}  DERIV pop={d['DERIV']['population_pairs']:6d} ex={d['DERIV']['excluded_pairs']:4d}"
              f"   APPLY pop={d['APPLY']['population_pairs']:6d} ex={d['APPLY']['excluded_pairs']:4d}"
              f"   (PF-LIMIT would exclude APPLY {d['APPLY']['PF_LIMIT_would_exclude']:5d})")

    # ---------------- the adopted arm, in full ----------------
    never, cont, left, no_after, nA = outcomes(W_ADOPTED)
    ex = no_after & never
    assert bool((never == (nA == 0)).all())

    core = {}
    for nm, m in (("DERIV", line4 & k10_adopted), ("APPLY", k10_adopted)):
        e = ex & m
        settings = {}
        for sname, live in (("no_liveness_filter", np.ones(n, bool)), ("ADOPTED_RULE", ~ex)):
            sel = m & live
            tot = int(sel.sum())
            c = [int((never & sel).sum()), int((cont & sel).sum()), int((left & sel).sum())]
            assert sum(c) == tot
            settings[sname] = {
                "pairs": tot,
                "excluded_pairs": int((m & ~live).sum()),
                "counts": dict(zip(STATES, c)),
                "shares_pct": dict(zip(STATES, [round(100.0 * x / tot, 4) for x in c])),
            }
        f = settings["ADOPTED_RULE"]
        u = settings["no_liveness_filter"]
        k = f["excluded_pairs"]
        ns, nl = f["counts"]["never_started"], f["pairs"]
        floor = 100.0 * ns / nl
        ceiling = 100.0 * (ns + k) / (nl + k)
        core[nm] = {
            "population_pairs": int(m.sum()),
            "settings": settings,
            "delta_vs_no_filter_pp": {
                s: round(f["shares_pct"][s] - u["shares_pct"][s], 4) for s in STATES},
            "step9_liveness_bound": {
                "excluded_pairs_all_never_started_by_construction": k,
                "floor_never_started_pct": round(floor, 6),
                "ceiling_never_started_pct": round(ceiling, 6),
                "width_pp": round(ceiling - floor, 6),
                "unfiltered_never_started_pct": round(u["shares_pct"]["never_started"], 6),
                "ceiling_equals_unfiltered_share_exact_rational": (
                    (ns + k) * u["pairs"] == u["counts"]["never_started"] * (nl + k)),
                "ceiling_minus_unfiltered_pp": round(
                    ceiling - 100.0 * u["counts"]["never_started"] / u["pairs"], 12),
            },
            "excluded_composition_by_outcome": {
                "never_started": int((e & never).sum()),
                "continued": int((e & cont).sum()),
                "started_and_left": int((e & left).sum()),
            },
            "excluded_with_positive_S2_evidence_at_tau1_|A|>=1": int((e & (nA >= 1)).sum()),
            "excluded_with_any_S2_record_step5_flag": int((e & has_s2).sum()),
            "PF_LIMIT_comparison": {
                "PF_LIMIT_excluded_pairs": int((no_after & m).sum()),
                "of_which_|A|>=1_no_stated_warrant": int((no_after & m & (nA >= 1)).sum()),
                "of_which_confirmed_continuers": int((no_after & m & cont).sum()),
                "of_which_started_and_left": int((no_after & m & left).sum()),
            },
        }

    # is the exclusion set exactly "the pairs with no S2 record anywhere"? tested, not assumed
    m_apply = k10_adopted
    e_apply = ex & m_apply
    no_record = m_apply & ~has_s2
    identity = {
        "APPLY_pairs_with_no_S2_record_anywhere_step5_flag": int(no_record.sum()),
        "APPLY_pairs_with_zero_distinct_in_E2_S2_episodes": int((m_apply & zero_ep).sum()),
        "excluded_pairs": int(e_apply.sum()),
        "excluded_is_a_SUBSET_of_no_S2_record": int((e_apply & ~no_record).sum()) == 0,
        "excluded_EQUALS_no_S2_record": bool(np.array_equal(e_apply, no_record)),
        "no_S2_record_pairs_that_stay_LIVE": int((no_record & ~ex).sum()),
        "reason_they_stay_live": "they have |A| = 0 but the account HAS an insertion instant "
                                 "after tau1, so conjunct (i) fails",
        "excluded_pairs_that_have_S2_records_but_zero_in_E2_episodes": int(
            (e_apply & has_s2 & zero_ep).sum()),
    }

    # how close is DERIV to firing? margin for its never-started pairs
    m_deriv = line4 & k10_adopted
    nev_d = never & m_deriv
    marg = (last_inst[nev_d] - (t0f[nev_d] + W_ADOPTED * SEC_PER_DAY)) / SEC_PER_DAY
    deriv_margin = {
        "never_started_pairs_on_DERIV": int(nev_d.sum()),
        "days_from_tau1_to_the_account_last_insertion_instant": {
            "min": round(float(marg.min()), 3),
            "p1": round(float(np.percentile(marg, 1)), 3),
            "p5": round(float(np.percentile(marg, 5)), 3),
            "median": round(float(np.median(marg)), 3),
            "max": round(float(marg.max()), 3),
        },
        "count_with_margin_le_0_would_be_excluded": int((marg <= 0).sum()),
        "count_with_margin_le_30_days": int((marg <= 30).sum()),
        "count_with_margin_le_90_days": int((marg <= 90).sum()),
        "reading": "every DERIV never-started pair's account inserts a record after tau1, and "
                   "the smallest margin states how near the zero is to changing",
    }

    out = {
        "step": 7, "instance": "alt2_a", "stage": 4, "api_calls": 0,
        "rule": "NOT LIVE iff (no insertion instant after tau1) AND (|A| = 0)",
        "W_adopted": W_ADOPTED, "H_days": H_DAYS,
        "arms": arms,
        "adopted_arm": core,
        "exclusion_set_identity_on_APPLY": identity,
        "DERIV_margin_diagnostic": deriv_margin,
    }
    with open(os.path.join(OUT, "arms.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    np.savez_compressed(os.path.join(OUT, "masks_W108.npz"),
                        user=user, never=never, cont=cont, left=left, ex=ex,
                        no_after=no_after, nA=nA, deriv=(line4 & k10_adopted),
                        apply_=k10_adopted, has_s2=has_s2)
    print(json.dumps({"adopted_arm": core, "identity": identity,
                      "DERIV_margin": deriv_margin}, indent=2))


if __name__ == "__main__":
    main()
