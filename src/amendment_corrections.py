"""Figures for the Step 1 sec 7 amendment, through the revision-10 strip. EVALUATION ONLY. ZERO API calls. Adopts nothing.

D11 IS NOW APPLIED, AND IT WAS NOT BEFORE.
  D11 (approved, Step 1 Section 0): tau_pull is a single global frozen cutoff and
  "records at or after it are discarded" -- from EVERY computation. Neither this
  script's revision-3 form nor src/eval_continued_boundary.py applied that filter.
  They bounded only at tau1 / tau2, which for pairs with a late T0 run past
  tau_pull, so those pairs' Continued windows were evaluated over records that
  D11 forbids. Every figure below is computed on D11-filtered records, and the
  pre-filter counterparts are reported beside them so the movement is visible.

  The filter also removes an artefact revision 3 mislabelled "real and not a bug":
  4 pairs had tau1 > tau_pull and held records dated after the cutoff, making them
  Continued at tau1 but not at the pull bound. Under D11 they cannot arise, and
  the monotonicity cont_tau1 <= cont_tau2 <= ever is asserted rather than
  worked around.

WHAT IS COMPUTED
  sec 4    the outcome table before and after the amendment, D11-filtered
  sec 2.2  fixed-horizon coverage at tau2 AND at tau1 -- the comparator the Human
           Lead ruled must be visible -- on one identical cleared subpopulation
           and one identical denominator, so only the boundary moves
  sec 2.3  the rejected all-cleared-pairs basis, with the FULL count of |A| = 0
           pairs it carries (numerator and window, not the window alone)
  sec 6.1  D8(ii) as a count-FLOOR and a share-CEILING
  sec 6.5  D3-prime clearance per Step 13 arm, now including SHOWS lost

POPULATION
  The Step 5 clean-record estimation sample, rebuilt by the mask used by
  src/eval_continued_boundary.py and asserted against the published waterfall.
  Records come from processed/step5/full_scan.npz -- the source every figure
  revision 2 published was computed on. A correction to a published number must
  be computed on the same basis as the number it corrects.

Output: processed/step7_eval/amendment_corrections.json  (counts only)
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
OUT = ROOT / "processed" / "step7_eval" / "amendment_corrections.json"

BACKFILL_D, POSTDATE_D = 180.0, -30.0
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
MISSING = np.iinfo(np.int64).min
W_ADOPTED, H, DAY = 108, 91, 86400.0
TAU_PULL = pd.Timestamp("2026-08-11", tz="UTC").timestamp()   # decisions/0011
ARMS = [46, 77, 108, 150, 213]        # decisions/0027: 46-107 span, plus 150, 213


def share(a, b):
    return None if not b else round(100.0 * a / b, 2)


def as_date(epoch_s):
    return str(pd.Timestamp(epoch_s, unit="s", tz="UTC").date())


def main():
    # ---------------------------------------------------------------- sample
    p = pd.read_csv(P5 / "pair_revision5.csv")
    has_s2 = p.s2_ev_n.values > 0
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    keep = ~(all_air | (t0c & ~has_s2))
    fs2_bad = has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                        | (p.first_s2_airdate.values == 1)
                        | (p.first_s2_corrupt.values == 1))
    w = [keep]
    for m in (has_s2, ~t0c, ~postd, ~fs2_bad):
        w.append(w[-1] & m)
    waterfall = [int(x.sum()) for x in w]
    assert waterfall == PUBLISHED_WATERFALL, f"waterfall drift: {waterfall}"
    est = p.loc[w[-1], ["user_idx", "show_trakt_id", "t0"]].copy()
    est["t0_ts"] = ((pd.to_datetime(est.t0, utc=True)
                     - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds())

    # ----------------------------------------------------------------- frame
    f = pd.read_csv(P2 / "frame.csv",
                    usecols=["show_trakt_id", "s2_E", "s2_L", "s2_F"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}
    need = {int(r.show_trakt_id): math.ceil(0.90 * int(r.s2_L)) for r in f.itertuples()}
    fin = {int(r.show_trakt_id): int(r.s2_F) for r in f.itertuples()}

    # ------------------------------------ canonical distinct-episode S2 stamps
    z = np.load(P5 / "full_scan.npz")
    m = (z["season"] == 2) & (z["ts"] != MISSING)
    s2 = pd.DataFrame({"user_idx": z["user"][m], "show_trakt_id": z["show"][m],
                       "number": z["number"][m], "ts": z["ts"][m]})
    del z
    s2 = s2[[n in e2.get(sh, ()) for sh, n in
             zip(s2.show_trakt_id.values, s2.number.values)]]
    # Step 1 sec 2.2: canonical timestamp of a distinct episode = min watched_at
    ep = s2.groupby(["user_idx", "show_trakt_id", "number"], as_index=False)["ts"].min()
    del s2

    d = est.reset_index(drop=True)
    d["k"] = [need.get(int(s), 10**9) for s in d.show_trakt_id]
    d["f2"] = [fin.get(int(s), -1) for s in d.show_trakt_id]
    idx = {(u, s): i for i, (u, s) in
           enumerate(zip(d.user_idx.values, d.show_trakt_id.values))}
    n = len(d)
    row_all = np.array([idx.get((u, s), -1) for u, s in
                        zip(ep.user_idx.values, ep.show_trakt_id.values)])
    keep_row = row_all >= 0
    row_all, ets_all, enum_all = (row_all[keep_row], ep.ts.values[keep_row],
                                  ep.number.values[keep_row])
    del ep

    # ================================================================= D11
    d11 = ets_all < TAU_PULL
    d11_report = {
        "rule": "D11: tau_pull is a global frozen cutoff; records at or after it "
                "are discarded from every computation",
        "tau_pull": as_date(TAU_PULL),
        "distinct_episode_records_in_scope": int(len(ets_all)),
        "discarded_at_or_after_tau_pull": int((~d11).sum()),
        "pairs_touched": int(len(set(row_all[~d11].tolist()))),
        "applied_in_revision_3": False,
        "applied_here": True,
    }

    def machinery(mask):
        row, ets, enum = row_all[mask], ets_all[mask], enum_all[mask]
        is_f2 = enum == d.f2.values[row]

        def continued_at(bound):
            sel = ets < bound[row]
            cnt = np.bincount(row[sel], minlength=n)
            f2hit = np.bincount(row[sel & is_f2], minlength=n) > 0
            return f2hit & (cnt >= d.k.values), cnt
        return continued_at

    C_d11 = machinery(d11)                       # D11-compliant
    C_raw = machinery(np.ones(len(d11), bool))   # revision 3's basis, for the delta

    t0 = d.t0_ts.values
    INF = np.full(n, np.inf)

    # ==================================================== sec 4 outcome table
    def table(C):
        tau1 = t0 + W_ADOPTED * DAY
        c1, nA = C(tau1)
        c2, _ = C(tau1 + H * DAY)
        st = nA > 0
        # sec 7's Continued carries the |A| >= 1 conjunct at BOTH bounds. Without
        # it, c2 sweeps in the |A| = 0 pairs that sec 6.1 reports as D8(ii) and the
        # table stops being a partition.
        c1, c2 = st & c1, st & c2
        return {"never_started": int((~st).sum()),
                "continued_before": int(c1.sum()),
                "started_and_left_before": int(st.sum() - c1.sum()),
                "continued_after": int(c2.sum()),
                "started_and_left_after": int(st.sum() - c2.sum()),
                "pairs_moved": int(c2.sum() - c1.sum())}
    t_d11, t_raw = table(C_d11), table(C_raw)
    t_d11["started_and_left_fall_pct"] = share(
        t_d11["started_and_left_before"] - t_d11["started_and_left_after"],
        t_d11["started_and_left_before"])
    t_d11["never_started_share_pct"] = round(100.0 * t_d11["never_started"] / n, 4)
    sec4 = {"D11_applied": t_d11, "revision_3_no_D11_filter": t_raw,
            "movement_from_applying_D11":
                {k: t_d11[k] - t_raw[k] for k in t_raw}}

    # ============================================ sec 2.2 coverage + comparator
    tau1 = t0 + W_ADOPTED * DAY
    tau2 = tau1 + H * DAY
    cont_tau1, nA = C_d11(tau1)
    started = nA > 0
    cont_tau2, _ = C_d11(tau2)
    cont_tau2H, _ = C_d11(tau2 + H * DAY)
    ever, _ = C_d11(INF)
    # D11 restores monotonicity; revision 3 worked around its absence instead
    assert int((cont_tau1 & ~cont_tau2).sum()) == 0
    assert int((cont_tau2 & ~cont_tau2H).sum()) == 0
    assert int((cont_tau2H & ~ever).sum()) == 0

    cleared = t0 + (W_ADOPTED + 2 * H) * DAY <= TAU_PULL     # D3-prime clearance
    cs = cleared & started
    # ONE denominator, ONE population; only the boundary moves between the rows
    den = int((cs & cont_tau2H).sum())
    cov = {
        "population": "pairs with |A| >= 1 at tau1, restricted to "
                      "[T0] + (W + 2H)*24h <= tau_pull",
        "cleared_started_pairs": int(cs.sum()),
        "cleared_share_of_started_pairs_pct": share(int(cs.sum()), int(started.sum())),
        "one_denominator_completers_visible_by_tau2_plus_H": den,
        "at_tau2_the_amended_boundary": {
            "complete_by_bound": int((cs & cont_tau2).sum()),
            "coverage_pct": share(int((cs & cont_tau2).sum()), den)},
        "at_tau1_the_rejected_boundary_COMPARATOR": {
            "complete_by_bound": int((cs & cont_tau1).sum()),
            "coverage_pct": share(int((cs & cont_tau1).sum()), den)},
    }
    cov["points_bought_by_the_boundary_move"] = round(
        cov["at_tau2_the_amended_boundary"]["coverage_pct"]
        - cov["at_tau1_the_rejected_boundary_COMPARATOR"]["coverage_pct"], 2)
    # The shared denominator above is anchored one horizon past the ADOPTED
    # boundary, which flatters the adopted boundary. Judged self-consistently --
    # each bound against its OWN +H denominator, tau1's being completers visible
    # by tau1 + H = tau2 -- the gap is smaller. Reported because it is the less
    # favourable construction and the argument it serves is a demotion.
    cov["self_consistent_each_bound_against_its_own_plus_H_denominator"] = {
        "at_tau1_pct": share(int((cs & cont_tau1).sum()), int((cs & cont_tau2).sum())),
        "at_tau2_pct": share(int((cs & cont_tau2).sum()), den),
        "note": "tau1's denominator is completers visible by tau1 + H = tau2; "
                "tau2's is completers visible by tau2 + H. Same cleared population.",
    }
    cov["self_consistent_each_bound_against_its_own_plus_H_denominator"]["gap_points"] = round(
        cov["self_consistent_each_bound_against_its_own_plus_H_denominator"]["at_tau2_pct"]
        - cov["self_consistent_each_bound_against_its_own_plus_H_denominator"]["at_tau1_pct"], 2)

    # ------------------------- is 12.9% a floor? the premise, tested not assumed
    late = t0 + W_ADOPTED * DAY > TAU_PULL      # tau1 runs past the frozen cutoff
    cov["pairs_whose_tau1_exceeds_tau_pull"] = {
        "n": int(late.sum()),
        "of_which_started": int((late & started).sum()),
        "of_which_never_started": int((late & ~started).sum()),
        "of_which_started_and_left_at_tau1": int((late & started & ~cont_tau1).sum()),
        "why_it_matters": "12.9% = movers / SAL_before. Both terms can grow under "
                          "longer observation, so 'floor' needs a premise: that no "
                          "pair can ENTER SAL_before. Only these pairs could.",
    }

    # sec 5's split, re-derived under D11 to confirm eval_continued_boundary.py's
    # figures survive the filter it never applied
    sal = started & ~cont_tau1
    sec5 = {"started_and_left_at_tau1": int(sal.sum()),
            "of_which_complete_S2_ever": int((sal & ever).sum()),
            "reclassified_by_the_amendment": int((sal & cont_tau2).sum()),
            "residual_not_reclassified": int((sal & ever & ~cont_tau2).sum())}
    sec5["capture_rate_pct"] = share(sec5["reclassified_by_the_amendment"],
                                     sec5["of_which_complete_S2_ever"])
    sec5["residual_share_of_old_started_and_left_pct"] = share(
        sec5["residual_not_reclassified"], int(sal.sum()))
    sec5["residual_share_of_new_started_and_left_pct"] = share(
        sec5["residual_not_reclassified"], t_d11["started_and_left_after"])
    assert (sec5["of_which_complete_S2_ever"] == 5686
            and sec5["reclassified_by_the_amendment"] == 2246
            and sec5["residual_not_reclassified"] == 3440), sec5

    ew_den = int((started & ever).sum())
    cov["exposure_weighted_same_comparison"] = {
        "basis": "denominator = started pairs completing at ANY point before "
                 "tau_pull; observation length varies by show recency",
        "completers": ew_den,
        "at_tau2_pct": share(int((started & cont_tau2).sum()), ew_den),
        "at_tau1_pct": share(int((started & cont_tau1).sum()), ew_den),
        "both_are_upper_bounds": "numerator fixed, denominator truncated; "
                                 "lengthening observation can only grow the "
                                 "denominator, so the untruncated value lies BELOW "
                                 "both. These do not bracket the quantity.",
    }

    # ================================= sec 2.3 the rejected all-cleared basis
    rej_num = int((cleared & cont_tau2).sum())
    rej_win = int((cleared & cont_tau2H & ~cont_tau2).sum())
    sec23 = {
        "why_rejected": "sec 2's population is 'pairs that start S2'. A pair with "
                        "|A| = 0 is Never started under the amendment no matter "
                        "when it completes, so its completion cannot bear on where "
                        "the Continued deadline is set.",
        "complete_by_tau2": rej_num, "complete_in_window": rej_win,
        "coverage_pct": share(rej_num, rej_num + rej_win),
        "A_empty_pairs_it_carries": {
            "in_the_numerator": int((cleared & ~started & cont_tau2).sum()),
            "in_the_window": int((cleared & ~started & cont_tau2H & ~cont_tau2).sum()),
            "total": int((cleared & ~started & cont_tau2H).sum()),
        },
    }

    # ============================== sec 6.1 D8(ii): count floor, share ceiling
    d8_n = int((~started & cont_tau2).sum())
    sec61 = {
        "count": d8_n,
        # NOT the 180-day filter: that is a BACKFILL measure (tau - ts, insertion
        # instant minus claimed watched_at), not a start-time filter. The draft
        # misread it for six revisions; see sec 4.2. The floor rests on the
        # contamination-exclusion channel instead -- and on 50,066, not 73,801,
        # because the 23,735 dropped at the waterfall's SECOND step have no S2
        # evidence at all, so A_H is empty and they can enter no numerator.
        "count_floor_basis": "contamination exclusion: 50,066 pairs dropped at "
                             "waterfall steps 3-5 are present in the population "
                             "D8 runs on and can carry A_H evidence",
        "share_of_estimation_sample_never_started_pct": share(d8_n, int((~started).sum())),
        "estimation_sample_never_started": int((~started).sum()),
        "share_is_a_CEILING": "8,449 is never-started ON THE ESTIMATION SAMPLE, "
                              "which requires S2 evidence. The true never-starters "
                              "-- pairs with no S2 record at all -- were removed at "
                              "the waterfall's second step. D8 runs on a population "
                              "whose denominator includes them.",
        "pairs_removed_at_waterfall_step_2": PUBLISHED_WATERFALL[0] - PUBLISHED_WATERFALL[1],
        "attribution": "NOT the price of the |A| >= 1 conjunct -- dropping that "
                       "conjunct does not deliver these pairs to Continued, it "
                       "makes the definition non-partitioning. The price belongs "
                       "to the asymmetric anchoring of sec 5.1.",
    }

    # ================================ sec 6.5 D3-prime per arm, with shows lost
    shows = d.show_trakt_id.values
    arms = {}
    for wv in ARMS:
        a1 = t0 + wv * DAY
        c1w, nAw = C_d11(a1)
        c2w, _ = C_d11(a1 + H * DAY)
        stw = nAw > 0
        sal = stw & ~c2w                       # Started and left AT tau2
        cl = t0 + (wv + 2 * H) * DAY <= TAU_PULL
        sh_all, sh_cl = set(shows[sal].tolist()), set(shows[sal & cl].tolist())
        arms[f"W={wv}"] = {
            "clearance_days": wv + 2 * H,
            "latest_T0_admitted": as_date(TAU_PULL - (wv + 2 * H) * DAY),
            "started_and_left_at_tau2": int(sal.sum()),
            "cleared_started_and_left": int((sal & cl).sum()),
            "cleared_share_of_started_and_left_pct": share(int((sal & cl).sum()),
                                                           int(sal.sum())),
            "shows_represented": len(sh_all),
            "shows_in_the_cleared_subset": len(sh_cl),
            "shows_lost": len(sh_all) - len(sh_cl),
            "shows_lost_pct": share(len(sh_all) - len(sh_cl), len(sh_all)),
        }

    # ============ sec 7 item 10: the counterweight to item 9, both directions sized
    # NO CORRECTED VALUES ARE COMPUTED HERE, DELIBERATELY.
    # Revisions 6-8 emitted never_started_if_corrected (6,874),
    # never_started_share_if_corrected_pct (5.37) and ratio_if_corrected (0.453).
    # All three are withdrawn: the arithmetic subtracts a FLOOR count from an
    # EXACT-looking denominator, and both known channels that would move the true
    # correction -- contamination exclusion, and D8's larger population -- run the
    # SAME way and neither is measured. A "ratio_before" key was also mislabelled:
    # it divided never-started by the POST-amendment started-and-left. The entry
    # carries counts with their floor/ceiling labels and nothing derived.
    item10 = {
        "mechanism": "never-started is decided at tau1 (108 d) while Continued is "
                     "decided at tau2 (199 d); pairs that start S2 after tau1 and "
                     "complete by tau2 are scored Never started",
        "direction": "UP -- never-started share and the ratio are both overstated",
        "floor_pairs": d8_n,
        "never_started_on_estimation_sample": int((~started).sum()),
        "share_of_that_denominator_pct_CEILING": share(d8_n, int((~started).sum())),
        "no_corrected_value": "not computable from what this study measures; see "
                              "the module note above",
        # Three populations, named. Revision 10 stated 1,573 as "the count on the
        # population D8 runs on", which it is not: D8's population differs from the
        # estimation sample by censoring AND the 50,066 AND the 23,735 AND Step 7
        # liveness. 1,573 is the estimation sample minus right-censoring only.
        "on_estimation_sample": d8_n,
        "surviving_right_censoring": int((~started & cont_tau2
                                          & (t0 + (W_ADOPTED + H) * DAY <= TAU_PULL)).sum()),
        "lost_to_right_censoring": int((~started & cont_tau2
                                        & (t0 + (W_ADOPTED + H) * DAY > TAU_PULL)).sum()),
        "on_D8_population": "not computed; >= the censoring-survivor count, by the "
                            "contamination-exclusion channel",
        # NOT "the valid comparison is COUNT vs COUNT": item 9 acts on the ratio's
        # DENOMINATOR and item 10 on its NUMERATOR, so the two counts are not
        # commensurable and netting them yields a meaningless number.
        "counterweight_to": "item 9, which moves the ratio DOWN on 3,440 pairs. The "
                            "two counts act on different components of the ratio and "
                            "MUST NOT be netted.",
        "item9_count": 3440,
    }

    # ============ the four-pair channel: closed at published precision, not bounded
    sal_before = t_d11["started_and_left_before"]
    movers = t_d11["pairs_moved"]
    ch = {
        "published_pct": round(100.0 * movers / sal_before, 4),
        "worst_case_pct": round(100.0 * movers / (sal_before + 4), 4),
        "both_round_to": round(100.0 * movers / sal_before, 1),
        "why_four": "only pairs with tau1 > tau_pull can change state; of those, 4 "
                    "are Never started and could ENTER the denominator",
        "same_four_as": ["sec 4.1's D11 pairs",
                         "artifacts/step6-w-derivation-a.json tau_pull_conflict",
                         "this channel"],
    }

    # ====== sec 4: DIRECT count of never-started pairs holding no admissible record
    # NOT 8,449 - 4. That 4 is the state-change delta -- pairs that FLIPPED when D11
    # was applied -- and it misses two families: a pair whose in-E2 records are ALL
    # post-cutoff but whose tau1 <= tau_pull is never-started on both bases and
    # contributes 0 to the delta; and a pair whose only S2 evidence falls OUTSIDE E2,
    # which is behaviourally a starter with no admissible in-E2 record at all.
    # Counting admissible in-E2 records per pair catches both.
    adm = np.bincount(row_all[d11], minlength=n)          # in-E2 records with ts < tau_pull
    no_adm = adm == 0
    sec4_adm = {
        "never_started_rows": int((~started).sum()),
        "of_which_hold_NO_admissible_in_E2_record": int((~started & no_adm).sum()),
        "of_which_hold_at_least_one": int((~started & ~no_adm).sum()),
        "the_delta_figure_revision_6_used": int(t_raw["never_started"]
                                                - t_d11["never_started"]) * -1,
        "why_the_delta_understates": "it counts only pairs that changed state when "
                                     "D11 was applied, not pairs lacking an "
                                     "admissible record",
        "warrant": "NOT s2_ev_n > 0 -- that is not the in-E2 object the claim needs, "
                   "and citing it would be circular against the outside-E2 objection "
                   "it answers. The warrant is computed here: 8,445 never-started "
                   "pairs hold adm >= 1, a listed E2 episode with ts < tau_pull, and "
                   "the residual 4 are the D11 flip four, which hold pre-tau1 in-E2 "
                   "records by construction.",
    }

    # ====== the Step 6 leg of the 'same four pairs' claim, computed not asserted
    # Step 6's tau_pull_conflict counts pairs whose FIRST S2 record is at or after
    # tau_pull, on processed/s1s2_scan.npz. This script works on full_scan.npz and
    # counts in-E2 episodes. sec 10 records that the two scans differ by 4 pairs on
    # the completer count, so containment cannot be inferred from the counts alone.
    zs = np.load(ROOT / "processed" / "s1s2_scan.npz")
    ms = (zs["season"] == 2) & (zs["ts"] != MISSING)
    s6 = pd.DataFrame({"user_idx": zs["user"][ms], "show_trakt_id": zs["show"][ms],
                       "number": zs["number"][ms], "ts": zs["ts"][ms]})
    del zs
    first_all = s6.groupby(["user_idx", "show_trakt_id"], as_index=False)["ts"].min()
    s6e = s6[[nn in e2.get(sh, ()) for sh, nn in
              zip(s6.show_trakt_id.values, s6.number.values)]]
    first_e2 = s6e.groupby(["user_idx", "show_trakt_id"], as_index=False)["ts"].min()
    del s6, s6e
    est_keys = set(zip(d.user_idx.values.tolist(), d.show_trakt_id.values.tolist()))

    def late_first(df):
        sub = df[df.ts >= TAU_PULL]
        return {(int(u), int(s)) for u, s in
                zip(sub.user_idx.values, sub.show_trakt_id.values)} & est_keys

    s6_all, s6_e2 = late_first(first_all), late_first(first_e2)
    d11_four = {(int(u), int(s)) for u, s in
                zip(d.user_idx.values[late & ~started], d.show_trakt_id.values[late & ~started])}
    # This is a REPRODUCTION, not an identity check. step6-w-derivation-a.json
    # publishes only a count -- correctly, since artifacts carry no pair
    # identifiers -- so A's own set cannot be compared against. What is done here:
    # re-derive the set under A's definition, on A's source (s1s2_scan.npz), on A's
    # stated population (the estimation sample), confirm the count matches A's
    # published 4, and set-compare the REPRODUCTION against the D11 four.
    same_four = {
        "status": "REPRODUCTION under instance A's definition and source, NOT an "
                  "identity check against A's own set, which is not published",
        "step6_definition": "pairs in the estimation sample whose FIRST S2 record is "
                            "at or after tau_pull, on processed/s1s2_scan.npz",
        "step6_published_count": 4,
        "reproduced_all_S2_records": len(s6_all),
        "reproduced_in_E2_only": len(s6_e2),
        "this_scripts_D11_four": len(d11_four),
        "reproduction_all_S2_set_identical_to_D11_four": sorted(s6_all) == sorted(d11_four),
        "reproduction_in_E2_set_identical_to_D11_four": sorted(s6_e2) == sorted(d11_four),
    }

    # ============ account-wide post-cutoff records -- the scope sec 9's placebo uses
    zf = np.load(P5 / "full_scan.npz")
    ts_all = zf["ts"]
    valid = ts_all != MISSING
    acct = {
        "records_account_wide_with_a_timestamp": int(valid.sum()),
        "at_or_after_tau_pull": int((valid & (ts_all >= TAU_PULL)).sum()),
        "why": "sec 9's placebo runs on account-wide insertion instants over every "
               "record in full_scan.npz, not on the S2/in-E2/estimation-sample "
               "subset the D11 block counts. This is the scope that bounds it.",
    }
    del zf, ts_all, valid

    res = {
        "what": "figures for the Step 1 sec 7 amendment; sec 2.2 and sec 2.3 were CUT at revision 10 and their keys are retained here as history only",
        "sec7_item10_counterweight": item10,
        "four_pair_channel": ch,
        "sec4_admissible_record_count": sec4_adm,
        "same_four_pairs_claim": same_four,
        "account_wide_post_cutoff_records": acct,
        "api_calls": 0, "adopts": "nothing",
        "W_adopted": W_ADOPTED, "H": H, "estimation_sample": n,
        "step5_waterfall_reproduced": waterfall,
        "D11": d11_report,
        "sec4_outcome_table": sec4,
        "sec5_split_rederived_under_D11": sec5,
        "HISTORY_sec2_2_coverage_CUT_AT_REVISION_10": cov,
        "HISTORY_sec2_3_rejected_basis_CUT_AT_REVISION_10": sec23,
        "sec6_1_D8ii": sec61,
        "sec6_5_D3prime_by_step13_arm": arms,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
