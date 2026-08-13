"""Step 7 ALTERNATIVE-RULE EVALUATION, namespace `a`.  STAGE 1 of 4 — core measurement at W = 108.

EVALUATION ONLY. Adopts nothing. The approved rule is PF-LIMIT (decisions/0042); Red Team
returned HOLD and proposed an alternative; the Human Lead rules after both arms report.

  PF-LIMIT  (approved)     not live  iff  no insertion instant after tau1
  ALT       (proposed)     not live  iff  (no insertion instant after tau1) AND (|A| = 0)

Both are computed on the SAME frozen inputs already on disk, so nothing is refitted:
  processed/step7/sens_a/pair_states.npz    per-pair outcome + no_before/no_after/gap
  processed/step7/sens_a/outcome_inputs.npz nA, nAH, f2_in_AH, L2, need
The outcome states are RECOMPUTED here from outcome_inputs and cross-checked against the
cached pair_states, so this stage does not trust the cache blindly.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
SENS = os.path.join(ROOT, "processed/step7/sens_a")
OUT = os.path.join(ROOT, "processed/step7/alt_a")

STATES = ["never_started", "continued", "started_and_left"]


def assign(nA, nAH, f2_in_AH, need):
    """Step 1 SS7 as amended by decisions/0034."""
    never = nA == 0
    cont = (nA >= 1) & f2_in_AH & (nAH >= need)
    left = (nA >= 1) & ~cont
    assert (never.astype(int) + cont + left == 1).all(), "states not a partition"
    return never, cont, left


def shares(never, cont, left, live):
    n = int(live.sum())
    c = [int((never & live).sum()), int((cont & live).sum()), int((left & live).sum())]
    assert sum(c) == n
    return n, c, [round(100.0 * x / n, 4) for x in c]


def main():
    os.makedirs(OUT, exist_ok=True)

    st = np.load(os.path.join(SENS, "pair_states.npz"))
    oi = np.load(os.path.join(SENS, "outcome_inputs.npz"))
    user = st["user"]
    no_after, no_before, measured, gap = (
        st["no_after"], st["no_before"], st["measured"], st["gap"])

    never, cont, left = assign(oi["nA"], oi["nAH"], oi["f2_in_AH"], oi["need"])
    # cross-check the recomputation against the cached states
    cache_ok = {
        "never": bool((never == st["never"]).all()),
        "continued": bool((cont == st["continued"]).all()),
        "started_and_left": bool((left == st["left"]).all()),
    }
    assert all(cache_ok.values()), f"recomputed states disagree with cache: {cache_ok}"

    n_pop = never.size
    assert n_pop == 147370

    # |A| = 0 is EXACTLY the Never-started state, by Step 1 SS7. Asserted, not assumed.
    assert bool((never == (oi["nA"] == 0)).all())

    ex_pf = no_after                       # PF-LIMIT exclusion set
    ex_alt = no_after & (oi["nA"] == 0)    # ALT exclusion set
    assert bool((ex_alt & ~ex_pf).sum() == 0), "ALT must be a subset of PF-LIMIT"

    def composition(mask):
        return {
            "pairs": int(mask.sum()),
            "accounts": int(np.unique(user[mask]).size),
            "by_outcome": {
                "never_started": int((mask & never).sum()),
                "continued": int((mask & cont).sum()),
                "started_and_left": int((mask & left).sum()),
            },
        }

    # the DELETED threshold rule's exclusion set, for the 0043 composition claim (1079/163/40)
    T = 1293
    ex_thr = no_after | (measured & (gap >= T))

    settings = {}
    for name, live in [
        ("no_liveness_filter", np.ones(n_pop, bool)),
        ("PF_LIMIT_approved", ~ex_pf),
        ("ALT_proposed", ~ex_alt),
        ("threshold_1293d_deleted", ~ex_thr),
    ]:
        n, c, s = shares(never, cont, left, live)
        ex = ~live
        settings[name] = {
            "pairs_live": n,
            "pairs_excluded": int(ex.sum()),
            "excluded_share_of_post_D10_pct": round(100.0 * ex.sum() / n_pop, 4),
            "accounts_touched_by_exclusion": int(np.unique(user[ex]).size),
            "excluded_composition": composition(ex)["by_outcome"],
            "counts": dict(zip(STATES, c)),
            "shares_pct": dict(zip(STATES, s)),
        }

    # ---------------- the Step 9 liveness bound ----------------
    # "what the never-started share becomes if every inactivity-excluded PAIR is treated as a
    # decliner" (task-sheet Step 9). Floor = the filtered point estimate; ceiling = every
    # excluded pair returned to the denominator AND counted never-started.
    bounds = {}
    for name in ("PF_LIMIT_approved", "ALT_proposed", "threshold_1293d_deleted"):
        s = settings[name]
        nl, k = s["pairs_live"], s["pairs_excluded"]
        ns = s["counts"]["never_started"]
        floor = 100.0 * ns / nl
        ceil = 100.0 * (ns + k) / (nl + k)
        # how many of the excluded pairs carry POSITIVE S2 evidence, i.e. |A| >= 1, and so
        # cannot be decliners at tau1 under Step 1 SS7
        ex = {"PF_LIMIT_approved": ex_pf, "ALT_proposed": ex_alt,
              "threshold_1293d_deleted": ex_thr}[name]
        pos = int((ex & (oi["nA"] >= 1)).sum())
        conf_cont = int((ex & cont).sum())
        bounds[name] = {
            "excluded_pairs": k,
            "floor_never_started_pct": round(floor, 4),
            "ceiling_never_started_pct": round(ceil, 4),
            "bound_width_pp": round(ceil - floor, 4),
            "excluded_with_positive_S2_evidence_at_tau1": pos,
            "excluded_with_positive_S2_evidence_share": (
                round(pos / k, 4) if k else None),
            "excluded_confirmed_continuers": conf_cont,
            "ceiling_counts_a_confirmed_continuer_as_a_decliner_for_n_pairs": conf_cont,
        }

    # ---------------- why ALT is what it is: the joint table ----------------
    joint = {
        "no_after_TRUE_and_nA_eq_0": int((no_after & (oi["nA"] == 0)).sum()),
        "no_after_TRUE_and_nA_ge_1": int((no_after & (oi["nA"] >= 1)).sum()),
        "no_after_FALSE_and_nA_eq_0": int((~no_after & (oi["nA"] == 0)).sum()),
        "no_after_FALSE_and_nA_ge_1": int((~no_after & (oi["nA"] >= 1)).sum()),
    }
    # of the never-started pairs, where does their insertion evidence sit?
    nev = never
    never_diag = {
        "never_started_pairs": int(nev.sum()),
        "of_which_no_instant_after_tau1": int((nev & no_after).sum()),
        "of_which_no_instant_at_or_before_tau1": int((nev & no_before).sum()),
        "of_which_measured_bracketing_gap": int((nev & measured).sum()),
    }

    out = {
        "step": 7,
        "what": "EVALUATION of Red Team's proposed alternative liveness rule against the "
                "approved PF-LIMIT. ADOPTS NOTHING. The Human Lead rules.",
        "instance": "alt_a",
        "api_calls": 0,
        "W_days": 108,
        "H_days": 91,
        "population_post_D10": n_pop,
        "population_line": "Step 5 waterfall line 4 (152,126) less D10 at W=108, H=91",
        "rules": {
            "PF_LIMIT_approved": "not live iff no insertion instant after tau1 (decisions/0042)",
            "ALT_proposed": "not live iff (no insertion instant after tau1) AND (|A| = 0)",
        },
        "recomputed_states_match_cached_pair_states": cache_ok,
        "classes_at_tau1": {
            "measured_bracketing_gap": int(measured.sum()),
            "open_ended_no_instant_after_tau1": int(no_after.sum()),
            "no_instant_at_or_before_tau1_LIVE_per_0021": int(no_before.sum()),
        },
        "joint_table_no_after_by_nA": joint,
        "never_started_diagnostic": never_diag,
        "settings": settings,
        "step9_liveness_bound": bounds,
    }
    with open(os.path.join(OUT, "core_W108.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    np.savez_compressed(os.path.join(OUT, "masks_W108.npz"),
                        user=user, never=never, cont=cont, left=left,
                        ex_pf=ex_pf, ex_alt=ex_alt, ex_thr=ex_thr, nA=oi["nA"])
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
