"""Step 7 RERUN on ALT-MATCHED (decisions/0052), namespace `a`. STAGE 3 — THE RULE.

THE RULE (0052 SS1)
  NOT LIVE iff  EITHER  (|A| = 0     AND no insertion instant after tau1)
                 OR     (|A| >= 1 AND NOT Continued AND no insertion instant after tau2)

Each null is tested at the instant its own outcome is READ:
  never started     |A| = 0                     read at tau1 -> silence tested at tau1
  started and left  |A| >= 1 and not Continued  read at tau2 -> silence tested at tau2
Continued (|A|>=1 and F2 in A_H and |A_H| >= ceil(0.90*L2), A_H at tau2) is the only state
resting on positive evidence and is NEVER excluded.

Outcome assignment happens at two instants (0034): |A| read at tau1, A_H read at tau2. Every
boundary test is half-open on the UTC instant: watched_at < tau. Distinct episodes, never play
events; membership by SET against E2.

Computed on BOTH populations at every W arm; every figure tagged by population; the exclusion
set split into never-started and started-and-left components everywhere. D10 contains W, so the
population is RE-DERIVED at each arm (0047 SS5); the frozen reading at W = 108 is reported
alongside with its arm named.

ALT-BROAD (both nulls tested at tau1) is computed in parallel as the SUPERSEDED comparator, so
the delta the rule change buys is measured rather than assumed.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
EPZ = os.path.join(ROOT, "processed/step7/alt2_a/episodes_line1.npz")
OUT = os.path.join(ROOT, "processed/step7/mm_a")

SEC_PER_DAY = 86400.0
H_DAYS = 91
W_ADOPTED = 108
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)
# decisions/0027 mandated grid, plus the off-grid arms 0047 SS5 / 0048 SS7 name
MANDATED = [38, 46, 77, 91, 107, 108, 150, 213]
ARMS = [38, 46, 60, 77, 91, 100, 107, 108, 125, 150, 180, 213]
STATES = ["never_started", "continued", "started_and_left"]


def main():
    pop = np.load(os.path.join(OUT, "population.npz"))
    epz = np.load(EPZ)
    li = np.load(os.path.join(OUT, "instants.npz"))

    rows = epz["pair_row"]
    n = rows.size
    assert n == 201900
    user = epz["user_idx"]
    L2 = epz["L2"]
    ep_row, ep_ts, ep_is_f2 = epz["ep_row"], epz["ep_ts"], epz["ep_is_f2"]
    t0f = pop["t0_floor"][rows]
    line4 = pop["line4"][rows]
    has_s2 = pop["has_s2"][rows]
    assert not np.isnan(t0f).any()
    assert (ep_ts < TAU_PULL).all(), "D11: an episode timestamp at or after tau_pull survived"

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
        assert (nA <= nAH).all(), "A subset of A_H violated"
        assert (nAH <= L2).all(), "distinct episodes exceed season length"
        # "after tau" is read STRICTLY: a tie does not prove liveness, so silence is <=
        silent1 = last_inst <= tau1
        silent2 = last_inst <= tau2
        # tau2 > tau1, so silence AFTER tau1 implies silence AFTER tau2: silent1 is a SUBSET of
        # silent2. The tau2-matched started-and-left branch is therefore strictly BROADER than
        # ALT-BROAD's tau1 test, which is why the exclusion count rises (0048 SS3b).
        assert not (silent1 & ~silent2).any(), "silence@tau1 must imply silence@tau2"
        return never, cont, left, silent1, silent2, nA, tau1, tau2

    def d10(W):
        return t0f + (max(W, 91) + H_DAYS) * SEC_PER_DAY <= TAU_PULL

    k10_adopted = d10(W_ADOPTED)
    assert int((line4 & k10_adopted).sum()) == 147370
    assert int(k10_adopted.sum()) == 196654

    arms = {}
    for W in ARMS:
        never, cont, left, silent1, silent2, nA, tau1, tau2 = outcomes(W)
        ex_ns = never & silent1                    # THE RULE, disjunct 1
        ex_sl = left & silent2                     # THE RULE, disjunct 2
        ex = ex_ns | ex_sl
        assert int((ex & cont).sum()) == 0
        assert int((ex_ns & ex_sl).sum()) == 0
        # superseded comparators, measured
        xb = (~cont) & silent1                     # ALT-BROAD: both nulls at tau1
        xa = never & silent1                       # ALT: |A| = 0 only
        row = {"in_mandated_grid_0027": W in MANDATED}
        for label, k10 in (("D10_per_arm", d10(W)), ("D10_frozen_at_W108", k10_adopted)):
            pops = {"DERIV": line4 & k10, "APPLY": k10}
            row[label] = {}
            for nm, m in pops.items():
                e, ens, esl = ex & m, ex_ns & m, ex_sl & m
                row[label][nm] = {
                    "population_pairs": int(m.sum()),
                    "excluded_pairs": int(e.sum()),
                    "excluded_never_started": int(ens.sum()),
                    "excluded_started_and_left": int(esl.sum()),
                    "excluded_share_of_population_pct": round(100.0 * e.sum() / m.sum(), 4),
                    "excluded_accounts": int(np.unique(user[e]).size),
                    "excluded_accounts_never_started_component": int(np.unique(user[ens]).size),
                    "excluded_accounts_started_and_left_component": int(np.unique(user[esl]).size),
                    "SUPERSEDED_ALT_BROAD_total": int((xb & m).sum()),
                    "SUPERSEDED_ALT_BROAD_started_and_left": int((xb & m & left).sum()),
                    "SUPERSEDED_ALT_total": int((xa & m).sum()),
                    "PF_LIMIT_silent_at_tau1_only": int((silent1 & m).sum()),
                    "never_started_in_population": int((never & m).sum()),
                    "continued_in_population": int((cont & m).sum()),
                    "started_and_left_in_population": int((left & m).sum()),
                }
        arms[str(W)] = row
        d = row["D10_per_arm"]
        print(f"W={W:4d}  DERIV pop={d['DERIV']['population_pairs']:6d} "
              f"ex={d['DERIV']['excluded_pairs']:4d} "
              f"(ns {d['DERIV']['excluded_never_started']:4d} / sl "
              f"{d['DERIV']['excluded_started_and_left']:4d})"
              f"   APPLY pop={d['APPLY']['population_pairs']:6d} "
              f"ex={d['APPLY']['excluded_pairs']:4d} "
              f"(ns {d['APPLY']['excluded_never_started']:4d} / sl "
              f"{d['APPLY']['excluded_started_and_left']:4d})"
              f"   [ALT-BROAD {d['APPLY']['SUPERSEDED_ALT_BROAD_total']:4d}]")

    # ---------------- the adopted arm, in full ----------------
    never, cont, left, silent1, silent2, nA, tau1, tau2 = outcomes(W_ADOPTED)
    ex_ns = never & silent1
    ex_sl = left & silent2
    ex = ex_ns | ex_sl
    xb = (~cont) & silent1
    xa = never & silent1

    core = {}
    for nm, m in (("DERIV", line4 & k10_adopted), ("APPLY", k10_adopted)):
        e, ens, esl = ex & m, ex_ns & m, ex_sl & m
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
                "shares_pct_full": dict(zip(STATES, [100.0 * x / tot for x in c])),
            }
        u = settings["no_liveness_filter"]
        f = settings["ADOPTED_RULE"]
        core[nm] = {
            "population_pairs": int(m.sum()),
            "population_accounts": int(np.unique(user[m]).size),
            "settings": settings,
            # computed from UNROUNDED shares: differencing rounded shares moves the last digit
            "delta_vs_no_filter_pp": {
                s: round(f["shares_pct_full"][s] - u["shares_pct_full"][s], 4) for s in STATES},
            "delta_vs_no_filter_pp_6dp": {
                s: round(f["shares_pct_full"][s] - u["shares_pct_full"][s], 6) for s in STATES},
            "exclusions": {
                "total": int(e.sum()),
                "accounts": int(np.unique(user[e]).size),
                "never_started_component": int(ens.sum()),
                "never_started_component_accounts": int(np.unique(user[ens]).size),
                "started_and_left_component": int(esl.sum()),
                "started_and_left_component_accounts": int(np.unique(user[esl]).size),
                "accounts_in_BOTH_components": int(np.intersect1d(user[ens], user[esl]).size),
                "continued_component_must_be_zero": int((e & cont).sum()),
                "share_of_population_pct": round(100.0 * e.sum() / m.sum(), 4),
                "accounts_with_ALL_their_pairs_excluded": int(sum(
                    1 for a in np.unique(user[e])
                    if int((m & (user == a)).sum()) == int((e & (user == a)).sum()))),
            },
            "exclusion_diagnostics": {
                "excluded_with_A_ge_1": int((e & (nA >= 1)).sum()),
                "excluded_with_step5_S2_evidence_flag": int((e & has_s2).sum()),
                "excluded_with_zero_in_E2_S2_episodes": int((e & zero_ep).sum()),
                "sl_component_median_A": float(np.median(nA[esl])) if esl.any() else None,
                "sl_component_A_min": int(nA[esl].min()) if esl.any() else None,
                "sl_component_A_max": int(nA[esl].max()) if esl.any() else None,
            },
            "rule_comparison_at_W108": {
                "PF_LIMIT_silent_at_tau1_only": int((silent1 & m).sum()),
                "SUPERSEDED_ALT_silent_tau1_AND_A_eq_0": int((xa & m).sum()),
                "SUPERSEDED_ALT_BROAD_silent_tau1_AND_not_continued": int((xb & m).sum()),
                "ADOPTED_ALT_MATCHED": int(e.sum()),
                "ALT_MATCHED_minus_ALT_BROAD": int(e.sum()) - int((xb & m).sum()),
                "confirmed_continuers_PF_LIMIT_would_delete": int((silent1 & m & cont).sum()),
                "continuers_a_tau2_PF_LIMIT_would_delete": int((silent2 & m & cont).sum()),
            },
        }

    # how the rule selects: it is a DISJUNCTION of two conjunctions, so the ALT-BROAD-style
    # single funnel does not describe it. Both branches are reported separately.
    decomposition = {}
    for nm, m in (("DERIV", line4 & k10_adopted), ("APPLY", k10_adopted)):
        decomposition[nm] = {
            "population": int(m.sum()),
            "branch_never_started": {
                "step_1_state_is_never_started": int((m & never).sum()),
                "step_2_and_silent_after_tau1": int((m & never & silent1).sum()),
            },
            "branch_started_and_left": {
                "step_1_state_is_started_and_left": int((m & left).sum()),
                "step_2_and_silent_after_tau2": int((m & left & silent2).sum()),
                "counterfactual_if_tested_at_tau1_ALT_BROAD": int((m & left & silent1).sum()),
            },
            "not_continued_total": int((m & ~cont).sum()),
            "silent_after_tau1_total": int((m & silent1).sum()),
            "silent_after_tau2_total": int((m & silent2).sum()),
            "reading": "ALT-MATCHED is a disjunction of two branches, each a state test AND a "
                       "silence test at that state's own reading instant. The ALT-BROAD funnel "
                       "'NOT Continued then silent' does not describe it, because the two "
                       "branches use different thresholds.",
        }

    # is the exclusion set 'the pairs with no S2 record anywhere'? tested, not assumed
    m_apply = k10_adopted
    e_apply = ex & m_apply
    no_record = m_apply & ~has_s2
    identity = {
        "APPLY_pairs_with_no_S2_record_anywhere_step5_flag": int(no_record.sum()),
        "APPLY_pairs_with_zero_distinct_in_E2_S2_episodes": int((m_apply & zero_ep).sum()),
        "excluded_pairs": int(e_apply.sum()),
        "excluded_is_a_SUBSET_of_no_S2_record": int((e_apply & ~no_record).sum()) == 0,
        "excluded_EQUALS_no_S2_record": bool(np.array_equal(e_apply, no_record)),
        "excluded_pairs_that_DO_hold_an_S2_record": int((e_apply & has_s2).sum()),
        "no_S2_record_pairs_that_stay_LIVE": int((no_record & ~ex).sum()),
    }

    out = {
        "step": 7, "instance": "mm_a", "stage": 3, "api_calls": 0,
        "rule": ("NOT LIVE iff (|A|=0 AND silent after tau1) OR "
                 "(|A|>=1 AND NOT Continued AND silent after tau2)"),
        "continued_definition": "|A|>=1 and F2 in A_H and |A_H| >= ceil(0.90*L2), A_H read at tau2",
        "W_adopted": W_ADOPTED, "H_days": H_DAYS,
        "mandated_arms_0027": MANDATED,
        "arms": arms,
        "adopted_arm": core,
        "branch_decomposition": decomposition,
        "exclusion_set_identity_on_APPLY": identity,
    }
    with open(os.path.join(OUT, "arms.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    np.savez_compressed(os.path.join(OUT, "masks_W108.npz"),
                        user=user, never=never, cont=cont, left=left,
                        ex=ex, ex_ns=ex_ns, ex_sl=ex_sl,
                        silent1=silent1, silent2=silent2, nA=nA,
                        deriv=(line4 & k10_adopted), apply_=k10_adopted,
                        has_s2=has_s2, t0f=t0f, tau1=tau1, tau2=tau2, last_inst=last_inst,
                        ex_altbroad=xb, ex_alt=xa)
    print(json.dumps({"adopted_arm": core, "branch_decomposition": decomposition,
                      "identity": identity}, indent=2))


if __name__ == "__main__":
    main()
