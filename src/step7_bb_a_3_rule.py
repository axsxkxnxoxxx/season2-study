"""Step 7 RERUN on ALT-BROAD (decisions/0048), namespace `a`. STAGE 3 of 7.

THE RULE
  NOT LIVE iff  (no insertion instant after tau1)  AND  (NOT Continued).

Continued (Step 1 SS7 as amended by 0034) is the ONLY state resting on positive evidence:
  continued  |A| >= 1  and  F2 in A_H  and  |A_H| >= ceil(0.90 * L2)
so the rule's second conjunct selects BOTH nulls:
  never started     |A| = 0                      -> null
  started and left  |A| >= 1 and not continued   -> null on exit

Outcome assignment happens at two instants (0034): |A| read at tau1, A_H read at
tau2 = tau1 + H*24h. Every boundary test is half-open on the UTC instant: watched_at < tau.

Computed on BOTH populations at every W arm, every figure tagged by population, and the
exclusion set split into its never-started and started-and-left components everywhere.
D10 contains W, so the population is re-derived at each arm (decisions/0047 SS5); the frozen
reading at W = 108 is reported alongside, with its arm named.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
PRIOR = os.path.join(ROOT, "processed/step7/alt2_a")
OUT = os.path.join(ROOT, "processed/step7/bb_a")

SEC_PER_DAY = 86400.0
H_DAYS = 91
W_ADOPTED = 108
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)
# decisions/0027 mandated grid, plus the two off-grid arms 0047 SS5 / 0048 SS7 name
MANDATED = [38, 46, 77, 91, 107, 108, 150, 213]
ARMS = [38, 46, 60, 77, 91, 100, 107, 108, 125, 150, 180, 213]
STATES = ["never_started", "continued", "started_and_left"]


def main():
    pop = np.load(os.path.join(OUT, "population.npz"))
    epz = np.load(os.path.join(PRIOR, "episodes_line1.npz"))
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
        no_after = last_inst <= tau1            # strict "after": a tie does not prove liveness
        return never, cont, left, no_after, nA

    def d10(W):
        return t0f + (max(W, 91) + H_DAYS) * SEC_PER_DAY <= TAU_PULL

    k10_adopted = d10(W_ADOPTED)
    assert int((line4 & k10_adopted).sum()) == 147370
    assert int(k10_adopted.sum()) == 196654

    arms = {}
    for W in ARMS:
        never, cont, left, no_after, nA = outcomes(W)
        ex = no_after & ~cont                              # THE RULE
        ex_ns, ex_sl = ex & never, ex & left
        assert int((ex & cont).sum()) == 0
        assert int((ex_ns | ex_sl != ex).sum()) == 0, "components must partition the exclusions"
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
                    "ALT_would_exclude_never_started_only": int(ens.sum()),
                    "PF_LIMIT_would_exclude_all_silent": int((no_after & m).sum()),
                    "PF_LIMIT_minus_ALT_BROAD_confirmed_continuers": int((no_after & m & cont).sum()),
                    "never_started_in_population": int((never & m).sum()),
                    "started_and_left_in_population": int((left & m).sum()),
                    "no_insertion_after_tau1_in_population": int((no_after & m).sum()),
                }
        arms[str(W)] = row
        d = row["D10_per_arm"]
        print(f"W={W:4d}  DERIV pop={d['DERIV']['population_pairs']:6d} "
              f"ex={d['DERIV']['excluded_pairs']:4d} "
              f"(ns {d['DERIV']['excluded_never_started']:4d} / sl {d['DERIV']['excluded_started_and_left']:4d})"
              f"   APPLY pop={d['APPLY']['population_pairs']:6d} "
              f"ex={d['APPLY']['excluded_pairs']:4d} "
              f"(ns {d['APPLY']['excluded_never_started']:4d} / sl {d['APPLY']['excluded_started_and_left']:4d})")

    # ---------------- the adopted arm, in full ----------------
    never, cont, left, no_after, nA = outcomes(W_ADOPTED)
    ex = no_after & ~cont
    ex_ns, ex_sl = ex & never, ex & left
    assert bool((never == (nA == 0)).all())

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
                "continued_component_must_be_zero": int((e & cont).sum()),
                "share_of_population_pct": round(100.0 * e.sum() / m.sum(), 4),
            },
            "exclusion_diagnostics": {
                "excluded_with_|A|>=1": int((e & (nA >= 1)).sum()),
                "excluded_with_step5_S2_evidence_flag": int((e & has_s2).sum()),
                "excluded_with_zero_in_E2_S2_episodes": int((e & zero_ep).sum()),
                "sl_component_median_|A|": float(np.median(nA[esl])) if esl.any() else None,
                "sl_component_|A|_min": int(nA[esl].min()) if esl.any() else None,
                "sl_component_|A|_max": int(nA[esl].max()) if esl.any() else None,
            },
            "rule_comparison": {
                "PF_LIMIT_no_insertion_after_tau1_only": int((no_after & m).sum()),
                "ALT_silent_AND_|A|=0": int(ens.sum()),
                "ALT_BROAD_silent_AND_not_continued": int(e.sum()),
                "confirmed_continuers_PF_LIMIT_would_delete": int((no_after & m & cont).sum()),
            },
        }

    # conjunct decomposition, reported for both populations (0047 SS2 gave it for APPLY only)
    decomposition = {}
    for nm, m in (("DERIV", line4 & k10_adopted), ("APPLY", k10_adopted)):
        decomposition[nm] = {
            "population": int(m.sum()),
            "after_conjunct_2_NOT_continued": int((m & ~cont).sum()),
            "after_both_conjuncts": int((m & ~cont & no_after).sum()),
            "conjunct_1_alone_no_insertion_after_tau1": int((m & no_after).sum()),
            "reading": "conjunct 2 narrows the population to the two nulls; conjunct 1 then "
                       "does almost all of the remaining work, which is why the count moves "
                       "with W at all",
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
        "reading": "under ALT-BROAD the exclusion set is NOT a subset of the no-S2-record "
                   "pairs, because the started-and-left component has |A| >= 1 by definition",
    }

    out = {
        "step": 7, "instance": "bb_a", "stage": 3, "api_calls": 0,
        "rule": "NOT LIVE iff (no insertion instant after tau1) AND (NOT Continued)",
        "continued_definition": "|A|>=1 and F2 in A_H and |A_H| >= ceil(0.90*L2), A_H read at tau2",
        "W_adopted": W_ADOPTED, "H_days": H_DAYS,
        "mandated_arms_0027": MANDATED,
        "arms": arms,
        "adopted_arm": core,
        "conjunct_decomposition": decomposition,
        "exclusion_set_identity_on_APPLY": identity,
    }
    with open(os.path.join(OUT, "arms.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    np.savez_compressed(os.path.join(OUT, "masks_W108.npz"),
                        user=user, never=never, cont=cont, left=left,
                        ex=ex, ex_ns=ex_ns, ex_sl=ex_sl,
                        no_after=no_after, nA=nA, deriv=(line4 & k10_adopted),
                        apply_=k10_adopted, has_s2=has_s2, t0f=t0f, last_inst=last_inst)
    print(json.dumps({"adopted_arm": core, "decomposition": decomposition,
                      "identity": identity}, indent=2))


if __name__ == "__main__":
    main()
