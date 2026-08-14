"""Step 8 (instance b) -- stage 2: the seven filter positions, both populations,
the analysis table, every required count, and the invariant battery.

GATE. NOTHING IS ADOPTED HERE. Step 8 is a gate: this instance produces its
deliverables and stops. It does not adopt its own proposal and it records no
approval.

READ ONLY on inputs. ZERO network calls.

THE MANDATED FILTER ORDER (decisions/0029; task-sheet.md Step 8). The final row
set commutes but the per-filter sample size does not, so the order is exact:

  1 Step 2 frame -> 2 L2 = 1 exclusion -> 3 S1 completion rule ->
  4 contamination exclusion (Step 5) -> 5 right-censoring -> 6 liveness ->
  7 outcome assignment, at TWO INSTANTS (decisions/0034).

Waterfall line 1 is the S1-completer population, 220,107 pairs (decisions/0068);
no instance chooses a base.

POPULATIONS -- every figure states one (standing rule, 0047):
  APPLY = line 1 less D10           = 196,654 at W = 108. Position-5 output.
  DERIV = Step 5 line 4 less D10    = 147,370 at W = 108. Requires S2 evidence.
Step 8 produces BOTH (0070 ruling 1).

THE LIVENESS RULE (ALT-BROAD; 0048, restored 0054, APPROVED 0064). A pair is
NOT LIVE iff BOTH: the account shows no insertion instant after that pair's
tau1, AND the pair is NOT Continued. "After" is STRICT -- silent iff no instant
> tau1 (0068). The evidence is restricted to records dated before tau_pull
(0070 ruling 2). The stored play-id calibration is READ, NEVER REFITTED (0029).

Out: processed/step8/b/{analysis_table.csv.gz, results.json, ...}
"""
from __future__ import annotations

import gzip
import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P2, P5 = ROOT / "processed" / "step2", ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step8" / "b"

TAU_PULL = 1786406400          # 2026-08-11T00:00:00Z, decisions/0011
DAY = 86400
W = 108                        # decisions/0026
H = 91                         # D10
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
BACKFILL_D, POSTDATE_D = 180.0, -30.0
STEP5_WATERFALL = [201_900, 178_165, 155_131, 152_126, 128_099]

R: dict = {}


def insert_time(rid, knot_rid, knot_time):
    """Verbatim from src/step5_calibrate.py. The curve is READ, never refitted."""
    return np.interp(rid.astype(np.float64), knot_rid, knot_time)


# ---------------------------------------------------------------------------
def main() -> None:
    t = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    R.update({
        "instance": "analytics-engineer-b", "namespace": "b",
        "step": 8, "mode": "GATE -- proposal only, nothing adopted",
        "api_calls": 0,
        "W_adopted": W, "H": H, "W_arms": W_ARMS,
        "tau_pull": "2026-08-11T00:00:00Z",
        "filter_order": ["1 Step 2 frame", "2 L2 = 1 exclusion", "3 S1 completion rule",
                         "4 contamination exclusion (Step 5)", "5 right-censoring",
                         "6 liveness", "7 outcome assignment (two instants)"],
        "boundary_convention": ("half-open UTC instants throughout (Step 1 Sec 2.4, D13); "
                                "date(watched_at) <= T1 appears nowhere"),
    })

    b = np.load(OUT / "base.npz")
    n_shows = int(b["n_shows"])
    show_ids = b["show_ids"]
    L2a, F2a, THR2a = b["L2"], b["F2"], b["THR2"]
    frame = pd.read_csv(P2 / "frame.csv").sort_values("show_trakt_id").reset_index(drop=True)
    assert (frame.show_trakt_id.values == show_ids).all()

    comp_pair = b["comp_pair"]
    t0_mid = b["t0_mid"].astype(np.int64)
    binds = b["binds"]
    comp_date_mid = b["comp_date_mid"].astype(np.int64)
    comp_post_cutoff = b["comp_uses_post_cutoff"]
    u_idx = comp_pair // n_shows
    s_idx = comp_pair % n_shows
    n1 = len(comp_pair)

    # =====================================================================
    # POSITIONS 1-3
    # =====================================================================
    wf: list[dict] = []
    line1 = np.ones(n1, dtype=bool)
    wf.append({"position": 1, "filter": "Step 2 frame",
               "retained_pairs": int(line1.sum()), "removed_pairs": 0,
               "retained_users": int(len(np.unique(u_idx))),
               "retained_shows": int(len(np.unique(s_idx))),
               "note": ("line 1 is the S1-completer population, ruled at 220,107 by "
                        "decisions/0068; no instance chooses a base")})
    assert int(line1.sum()) == 220_107, int(line1.sum())

    l2_eq_1 = L2a[s_idx] == 1
    line2 = line1 & ~l2_eq_1
    wf.append({"position": 2, "filter": "L2 = 1 exclusion",
               "retained_pairs": int(line2.sum()),
               "removed_pairs": int((line1 & l2_eq_1).sum()),
               "removed_shows": int((L2a == 1).sum()),
               "shows_examined": n_shows,
               "retained_users": int(len(np.unique(u_idx[line2]))),
               "retained_shows": int(len(np.unique(s_idx[line2]))),
               "coverage_note": ("0 of 1,138 frame shows have L2 = 1: this line is a "
                                 "measured zero on a examined population, not an empty check")})

    line3 = line2.copy()   # line 1 is already the S1-completer set (0068)
    wf.append({"position": 3, "filter": "S1 completion rule",
               "retained_pairs": int(line3.sum()),
               "removed_pairs": int((line2 & ~line3).sum()),
               "retained_users": int(len(np.unique(u_idx[line3]))),
               "retained_shows": int(len(np.unique(s_idx[line3]))),
               "note": ("removes 0 by construction: decisions/0068 defines line 1 as the "
                        "S1-completer population, so the rule has already bound at line 1. "
                        "The rule was nevertheless computed independently at stage 1 "
                        "(F1 in D1 and |D1| >= ceil(0.90 x L1), first-pass) and it is that "
                        "computation which produced line 1")})

    # =====================================================================
    # POSITION 4 -- the Step 5 contamination exclusion (approved gate 0021)
    # =====================================================================
    p5 = pd.read_csv(P5 / "pair_revision5.csv")
    key_mine = pd.DataFrame({"user_idx": u_idx, "show_trakt_id": show_ids[s_idx],
                             "_row": np.arange(n1)})
    p5m = p5.merge(key_mine, on=["user_idx", "show_trakt_id"], how="left", validate="1:1")
    assert p5m._row.notna().all(), "a Step 5 pair is absent from this instance's line 1"
    assert len(p5m) == n1
    ordr = p5m._row.values.astype(np.int64)
    inv = np.empty(n1, dtype=np.int64)
    inv[ordr] = np.arange(n1)

    has_s2_ev = (p5.s2_ev_n.values > 0)[inv]
    t0c = p5.t0_contaminated.values.astype(bool)[inv]
    postd = (p5.complete_rec_lag_days.values < POSTDATE_D)[inv]
    all_air = has_s2_ev & (p5.s2_ev_airdate.values == p5.s2_ev_n.values)[inv]
    fs2_bad = has_s2_ev & ((p5.first_s2_lag_days.values > BACKFILL_D)
                           | (p5.first_s2_airdate.values == 1)
                           | (p5.first_s2_corrupt.values == 1))[inv]

    contam_excl = all_air | (t0c & ~has_s2_ev)
    line4 = line3 & ~contam_excl
    # Step 5's own waterfall, re-asserted line by line before it is used
    s5 = [line4]
    for m in (has_s2_ev, ~t0c, ~postd, ~fs2_bad):
        s5.append(s5[-1] & m)
    s5_counts = [int(x.sum()) for x in s5]
    assert s5_counts == STEP5_WATERFALL, (s5_counts, STEP5_WATERFALL)
    R["step5_waterfall_reasserted"] = {"measured": s5_counts, "expected": STEP5_WATERFALL}
    line4_step5 = s5[3]          # Step 5 line 4 -- the DERIV base before D10

    wf.append({"position": 4, "filter": "contamination exclusion (Step 5, decisions/0021)",
               "retained_pairs": int(line4.sum()),
               "removed_pairs": int((line3 & contam_excl).sum()),
               "removed_all_S2_evidence_air_date_stamped": int((line3 & all_air).sum()),
               "removed_contaminated_T0_with_no_S2_evidence":
                   int((line3 & t0c & ~has_s2_ev).sum()),
               "retained_users": int(len(np.unique(u_idx[line4]))),
               "retained_shows": int(len(np.unique(s_idx[line4]))),
               "note": ("the ADOPTED rule is two disjoint exclusions; it is not the Step 5 "
                        "estimation-sample waterfall down to 128,099")})

    # =====================================================================
    # S2 EVIDENCE -- |A|, |A_H|, F2 in A_H, max(A_H), at any instant
    # =====================================================================
    s2_pairs, s2_start, s2_counts = b["s2_pairs"], b["s2_start"], b["s2_counts"]
    s2_ts, s2_num, s2_runmax, f2_ts = b["s2_ts"], b["s2_num"], b["s2_runmax"], b["f2_ts"]
    pos_of = np.full(n_shows * (u_idx.max() + 1) + n_shows, -1, dtype=np.int64)
    # map pair_code -> index into s2_pairs, via searchsorted (s2_pairs is sorted)
    loc = np.searchsorted(s2_pairs, comp_pair)
    loc_ok = (loc < len(s2_pairs)) & (s2_pairs[np.clip(loc, 0, len(s2_pairs) - 1)] == comp_pair)
    del pos_of
    start = np.where(loc_ok, s2_start[np.clip(loc, 0, len(s2_pairs) - 1)], 0)
    cnt = np.where(loc_ok, s2_counts[np.clip(loc, 0, len(s2_pairs) - 1)], 0)
    f2ts = np.where(loc_ok, f2_ts[np.clip(loc, 0, len(s2_pairs) - 1)],
                    np.iinfo(np.int64).max)

    TS_MIN = int(s2_ts.min()) - 1
    SPAN = int(s2_ts.max()) - TS_MIN + 10 ** 9
    pair_rank = np.searchsorted(s2_pairs, s2_pairs)  # identity, kept for clarity
    combined = (np.repeat(np.arange(len(s2_pairs), dtype=np.int64), s2_counts) * SPAN
                + (s2_ts - TS_MIN))
    del pair_rank

    def n_before(tau: np.ndarray) -> np.ndarray:
        """|{distinct in-E2 S2 episodes with canonical watched_at < tau}| per pair."""
        assert (tau - TS_MIN < SPAN).all() and (tau >= TS_MIN).all()
        q = np.where(loc_ok, loc * SPAN + (tau - TS_MIN), -1)
        idx = np.searchsorted(combined, q, side="left")
        return np.where(loc_ok, idx - start, 0)

    def maxnum_before(k: np.ndarray) -> np.ndarray:
        """max episode number among the first k episodes in instant order."""
        return np.where(k > 0, s2_runmax[np.clip(start + k - 1, 0, len(s2_runmax) - 1)], -1)

    # rank table for p: |{e in E2 : e <= m}| / L2
    maxE = int(max(F2a.max(), 1)) + 1
    rank_tab = np.zeros((n_shows, maxE + 1), dtype=np.int64)
    for i in range(n_shows):
        e = np.array(sorted({int(x) for x in str(frame.s2_E.iloc[i]).split(",")
                             if x.strip().isdigit()}))
        rank_tab[i, :] = np.searchsorted(e, np.arange(maxE + 1), side="right")

    # =====================================================================
    # LIVENESS INPUT -- per-account maximum insertion instant
    # =====================================================================
    cal = np.load(P5 / "calibration.npz")
    knot_rid, knot_time = cal["knot_rid"], cal["knot_time"]
    z = np.load(P5 / "full_scan.npz")
    r_user, r_rid, r_ts = z["user"], z["rid"], z["ts"]
    inst = insert_time(r_rid, knot_rid, knot_time)
    n_users = int(r_user.max()) + 1
    max_inst_unrestricted = np.full(n_users, -np.inf)
    np.maximum.at(max_inst_unrestricted, r_user, inst)
    keep11 = r_ts < TAU_PULL
    max_inst = np.full(n_users, -np.inf)
    np.maximum.at(max_inst, r_user[keep11], inst[keep11])
    R["liveness_inputs"] = {
        "calibration": {"source": "processed/step5/calibration.npz",
                        "status": "READ, NEVER REFITTED (decisions/0029)",
                        "n_knots": int(len(knot_rid)),
                        "application": "np.interp(rid, knot_rid, knot_time)",
                        "records_clamped_below_first_knot": int((r_rid < knot_rid[0]).sum()),
                        "records_clamped_above_last_knot": int((r_rid > knot_rid[-1]).sum())},
        "evidence_scope": ("account-wide -- the whole sweep, other shows and movies "
                           "included -- RESTRICTED to records with watched_at < tau_pull "
                           "(decisions/0070 ruling 2, D11 applied consistently)"),
        "records_used": int(keep11.sum()),
        "records_excluded_by_the_tau_pull_restriction": int((~keep11).sum()),
        "accounts": n_users,
        "max_insertion_instant_utc": str(np.datetime64(int(np.nanmax(max_inst)), "s")),
        "max_insertion_instant_unrestricted_utc":
            str(np.datetime64(int(np.nanmax(max_inst_unrestricted)), "s")),
    }
    del inst, r_rid, keep11
    mx = max_inst[u_idx]
    mx_unres = max_inst_unrestricted[u_idx]

    # =====================================================================
    # POSITIONS 5, 6, 7 -- per W arm, on both populations
    # =====================================================================
    per_arm: dict = {"APPLY": {}, "DERIV": {}}
    air_period = frame.air_period.values[s_idx]
    censor_air: dict = {}
    keep_main = None

    for Wa in W_ARMS:
        tau1 = t0_mid + Wa * DAY
        tau2 = t0_mid + (Wa + H) * DAY
        tau3 = t0_mid + (Wa + 2 * H) * DAY
        term1 = t0_mid + max(Wa, 91) * DAY <= TAU_PULL
        d10 = t0_mid + (max(Wa, 91) + H) * DAY <= TAU_PULL
        assert (d10 <= term1).all()

        nA = n_before(tau1)
        nAH = n_before(tau2)
        nA3 = n_before(tau3)
        f2_in_AH = f2ts < tau2
        f2_in_A3 = f2ts < tau3
        started = nA >= 1
        contd = started & f2_in_AH & (nAH >= THR2a[s_idx])
        sal = started & ~contd
        never = ~started
        notlive = (mx <= tau1) & ~contd
        notlive_unres = (mx_unres <= tau1) & ~contd

        line5 = line4 & d10
        line6 = line5 & ~notlive
        deriv5 = line4_step5 & d10
        deriv6 = deriv5 & ~notlive

        # per-air-period retention after right-censoring, on the POSITION-4 output
        ap = {}
        for name in ["pre-2020", "2020-2022", "2023-2025"]:
            m = line4 & (air_period == name)
            ap[name] = {"position4_pairs": int(m.sum()),
                        "retained_after_censoring": int((m & d10).sum()),
                        "retained_pct": 100.0 * float((m & d10).sum()) / max(int(m.sum()), 1)}
        ap["ALL"] = {"position4_pairs": int(line4.sum()),
                     "retained_after_censoring": int(line5.sum()),
                     "retained_pct": 100.0 * int(line5.sum()) / int(line4.sum())}
        censor_air[str(Wa)] = ap

        for pop, p5mask, p6mask in (("APPLY", line5, line6), ("DERIV", deriv5, deriv6)):
            n = int(p5mask.sum())
            ex = int((p5mask & notlive).sum())
            ex_ns = int((p5mask & notlive & never).sum())
            ex_sl = int((p5mask & notlive & sal).sum())
            ex_c = int((p5mask & notlive & contd).sum())
            assert ex_c == 0
            ns_t, c_t, sl_t = (int((p5mask & never).sum()), int((p5mask & contd).sum()),
                               int((p5mask & sal).sum()))
            assert ns_t + c_t + sl_t == n
            # D3' cleared subpopulation, at this arm on this population
            cleared = p6mask & sal & (tau3 <= TAU_PULL)
            completes = cleared & f2_in_A3 & (nA3 >= THR2a[s_idx])
            sal_live = int((p6mask & sal).sum())
            per_arm[pop][str(Wa)] = {
                "W": Wa, "population": pop,
                "position5_n": n,
                "position6_n": int(p6mask.sum()),
                "liveness_excluded": ex,
                "liveness_excluded_never_started": ex_ns,
                "liveness_excluded_started_and_left": ex_sl,
                "liveness_excluded_continued": ex_c,
                "accounts_supplying_exclusions":
                    int(len(np.unique(u_idx[p5mask & notlive]))) if ex else 0,
                "liveness_excluded_under_unrestricted_evidence":
                    int((p5mask & notlive_unres).sum()),
                "states_at_position5": {"never_started": ns_t, "continued": c_t,
                                        "started_and_left": sl_t},
                "states_at_position7": {
                    "never_started": int((p6mask & never).sum()),
                    "continued": int((p6mask & contd).sum()),
                    "started_and_left": int((p6mask & sal).sum())},
                "D3prime": {
                    "definition": ("of pairs Started-and-left at tau2 whose "
                                   "[T0] + (W + 2H) x 24h <= tau_pull, the share completing "
                                   "within [tau2, tau2 + H)"),
                    "started_and_left_at_this_arm_on_this_population": sal_live,
                    "cleared_count": int(cleared.sum()),
                    "cleared_share_of_started_and_left_pct":
                        100.0 * int(cleared.sum()) / max(sal_live, 1),
                    "completing_within_the_horizon": int(completes.sum()),
                    "share_completing_pct":
                        100.0 * int(completes.sum()) / max(int(cleared.sum()), 1),
                    "denominator_note": ("both denominators are this arm's and this "
                                         "population's own (decisions/0069 item 5)")},
            }
        if Wa == W:
            keep_main = dict(nA=nA, nAH=nAH, contd=contd, sal=sal, never=never,
                             notlive=notlive, line5=line5, line6=line6,
                             deriv5=deriv5, deriv6=deriv6, tau1=tau1, tau2=tau2,
                             f2_in_AH=f2_in_AH, term1=term1, d10=d10)

    R["per_arm"] = per_arm
    R["censoring_per_air_period"] = censor_air

    # ---- waterfall lines 5, 6, 7 at the adopted W --------------------------
    K = keep_main
    line5, line6 = K["line5"], K["line6"]
    wf.append({"position": 5, "filter": "right-censoring",
               "retained_pairs": int(line5.sum()),
               "removed_pairs": int((line4 & ~line5).sum()),
               "removed_by_max_W_91_term": int((line4 & ~K["term1"]).sum()),
               "removed_incrementally_by_the_plus_H_term":
                   int((line4 & K["term1"] & ~K["d10"]).sum()),
               "direction_on_the_headline": ("BOTH removals move the never-started share "
                                             "UP: they remove recent S1 completers, who are "
                                             "disproportionately likely to roll straight on"),
               "retained_users": int(len(np.unique(u_idx[line5]))),
               "retained_shows": int(len(np.unique(s_idx[line5])))})
    wf.append({"position": 6, "filter": "liveness (ALT-BROAD, approved 0064)",
               "retained_pairs": int(line6.sum()),
               "removed_pairs": int((line5 & ~line6).sum()),
               "outcome_conditional": True,
               "outcome_conditional_note": ("conjunct 2 IS the Continued test, read at tau2, "
                                            "so this line is outcome-conditional and is "
                                            "reported as such (0046). Permitted: |A| and "
                                            "liveness are row-local predicates on the "
                                            "position-5 output and commute exactly, and "
                                            "position 7 removes no rows"),
               "retained_users": int(len(np.unique(u_idx[line6]))),
               "retained_shows": int(len(np.unique(s_idx[line6])))})
    wf.append({"position": 7, "filter": "outcome assignment (two instants)",
               "retained_pairs": int(line6.sum()), "removed_pairs": 0,
               "note": "an annotation, not a filter: it removes no rows",
               "retained_users": int(len(np.unique(u_idx[line6]))),
               "retained_shows": int(len(np.unique(s_idx[line6])))})
    R["waterfall_APPLY"] = wf

    # ---- the DERIV waterfall ------------------------------------------------
    d5, d6 = K["deriv5"], K["deriv6"]
    R["waterfall_DERIV"] = [
        dict(wf[0]), dict(wf[1]), dict(wf[2]),
        {"position": 4, "filter": ("contamination exclusion, taken to Step 5 LINE 4 -- the "
                                   "adopted exclusion plus the three line-4 restrictions "
                                   "(has_s2, T0 not contaminated, completing record not "
                                   "post-dated) that define the DERIV base"),
         "retained_pairs": int(line4_step5.sum()),
         "removed_pairs": int((line3 & ~line4_step5).sum()),
         "step5_line_by_line": STEP5_WATERFALL[:4]},
        {"position": 5, "filter": "right-censoring", "retained_pairs": int(d5.sum()),
         "removed_pairs": int((line4_step5 & ~d5).sum())},
        {"position": 6, "filter": "liveness", "retained_pairs": int(d6.sum()),
         "removed_pairs": int((d5 & ~d6).sum()), "outcome_conditional": True},
        {"position": 7, "filter": "outcome assignment", "retained_pairs": int(d6.sum()),
         "removed_pairs": 0},
    ]
    assert int(line5.sum()) == 196_654, int(line5.sum())
    assert int(d5.sum()) == 147_370, int(d5.sum())

    # =====================================================================
    # THE ANALYSIS TABLE
    # =====================================================================
    nA, nAH = K["nA"], K["nAH"]
    m_H = maxnum_before(nAH)
    p_rank = np.where(m_H >= 0, rank_tab[s_idx, np.clip(m_H, 0, maxE)], 0)
    p_val = np.where(K["sal"] & (m_H >= 0), p_rank / np.maximum(L2a[s_idx], 1), np.nan)

    outcome = np.where(K["never"], "never_started",
                       np.where(K["contd"], "continued", "started_and_left"))

    # discovery channel: TWO booleans (0070 ruling 3)
    users = json.loads((P5 / "user_index.json").read_text())["users"]
    pool = {}
    for line in open(ROOT / "raw" / "step3" / "user_pool.jsonl"):
        d = json.loads(line)
        pool[d["slug"]] = (bool(d["in_a"]), bool(d["in_b"]))
        pool.setdefault(d["username"], (bool(d["in_a"]), bool(d["in_b"])))
    ch = np.array([pool.get(users[i], (False, False)) for i in range(len(users))])
    in_a_u, in_b_u = ch[:, 0].astype(bool), ch[:, 1].astype(bool)
    R["discovery_channel"] = {
        "form": "TWO BOOLEAN COLUMNS, not one categorical (decisions/0070 ruling 3)",
        "pool_users": sum(1 for _ in open(ROOT / "raw" / "step3" / "user_pool.jsonl")),
        "accounts_in_the_analysis_population": int(len(np.unique(u_idx[line5]))),
        "accounts_channel_A_only": int((in_a_u & ~in_b_u)[np.unique(u_idx[line5])].sum()),
        "accounts_channel_B_only": int((~in_a_u & in_b_u)[np.unique(u_idx[line5])].sum()),
        "accounts_in_BOTH": int((in_a_u & in_b_u)[np.unique(u_idx[line5])].sum()),
        "accounts_in_NEITHER": int((~in_a_u & ~in_b_u)[np.unique(u_idx[line5])].sum()),
        "note": ("324 of the 5,694 pooled users are in both channels; one categorical "
                 "column would drop the overlap or assign it arbitrarily"),
    }

    # per-pair action counts by type (0070 ruling 4)
    act_key, act_n = b["act_key"], b["act_n"]
    ak_pair = act_key // 8
    ak_slot = act_key % 8
    acts = np.zeros((n1, 8), dtype=np.int32)
    lp = np.searchsorted(comp_pair, ak_pair)
    lp_ok = (lp < n1) & (comp_pair[np.clip(lp, 0, n1 - 1)] == ak_pair)
    acts[lp[lp_ok], ak_slot[lp_ok]] = act_n[lp_ok]
    act_names = ["s1_watch", "s1_checkin", "s1_scrobble", "s1_other",
                 "s2_watch", "s2_checkin", "s2_scrobble", "s2_other"]

    sel = line5    # the table is emitted on the POSITION-5 population, with flags
    tab = pd.DataFrame({
        "user_idx": u_idx[sel],
        "show_trakt_id": show_ids[s_idx[sel]],
        "in_apply": True,
        "in_deriv": line4_step5[sel],
        "live": ~K["notlive"][sel],
        "outcome": outcome[sel],
        "abandonment_point_p": p_val[sel],
        "discovered_channel_a": in_a_u[u_idx[sel]],
        "discovered_channel_b": in_b_u[u_idx[sel]],
        "t0_date": pd.to_datetime(t0_mid[sel], unit="s").date,
        "s1_completion_date": pd.to_datetime(np.clip(comp_date_mid[sel], -62135596800,
                                                     TAU_PULL), unit="s").date,
        "t0_binding_term": binds[sel],
        "tau1": K["tau1"][sel], "tau2": K["tau2"][sel],
        "n_A": nA[sel], "n_A_H": nAH[sel],
        "f2_in_A_H": K["f2_in_AH"][sel],
        "max_episode_in_A_H": m_H[sel],
        "s1_completion_used_a_post_cutoff_record": comp_post_cutoff[sel],
    })
    for j, nm in enumerate(act_names):
        tab["action_count_" + nm] = acts[sel, j]
    show_cols = [c for c in frame.columns if c != "show_trakt_id"]
    tab = tab.merge(frame[["show_trakt_id"] + show_cols], on="show_trakt_id", how="left")
    assert len(tab) == int(sel.sum())
    tab.to_csv(OUT / "analysis_table.csv.gz", index=False, compression="gzip")
    R["analysis_table"] = {
        "path": "processed/step8/b/analysis_table.csv.gz",
        "rows": int(len(tab)),
        "row_set": ("the POSITION-5 population, APPLY = 196,654, carrying the position-6 "
                    "flag `live` and the position-7 `outcome`. The post-position-7 row set "
                    "is `live == True` (195,951); DERIV is `in_deriv` (147,370) and its "
                    "post-position-7 row set is `in_deriv & live`. The 703 excluded rows "
                    "are retained IN THE FILE with live = False, because Step 9's bounds "
                    "are built from their outcome states and rebuilding them downstream "
                    "would be a second definition of the filter"),
        "columns": int(len(tab.columns)),
        "action_is_counts_not_a_column": True,
        "discovery_channel_is_two_booleans": True,
    }

    # =====================================================================
    # REQUIRED COUNTS
    # =====================================================================
    R["required_counts"] = req = {}

    # --- drop counts -------------------------------------------------------
    st1 = json.loads((OUT / "stage1.json").read_text())
    dropped_s2_pair = b["dropped_s2_pair"]
    entire_s2_dropped = np.isin(comp_pair, dropped_s2_pair) & (nA == 0)
    ns5 = int((line5 & K["never"]).sum())
    ns7 = int((line6 & K["never"]).sum())
    req["drop_counts"] = {
        "per_show_file": "processed/step8/b/drop_counts_per_show.csv",
        "records_examined": st1["drop_rule"]["records_examined"],
        "records_dropped_total": st1["drop_rule"]["records_dropped"],
        "distinct_season_number_pairs_dropped": 0,
        "shows_with_any_drop": 0,
        "per_outcome_pairs_whose_entire_S2_evidence_was_dropped":
            int((line5 & entire_s2_dropped).sum()),
        "denominator_never_started_at_position5": ns5,
        "denominator_never_started_post_liveness": ns7,
        "share_of_never_started_at_position5_pct":
            100.0 * int((line5 & entire_s2_dropped).sum()) / ns5,
        "share_of_never_started_post_liveness_pct":
            100.0 * int((line5 & entire_s2_dropped).sum()) / ns7,
        "denominator_note": ("the drop count is a property of the filter, so it measures "
                             "against what ENTERED it -- position 5. The post-liveness "
                             "figure is reported alongside; the difference between the two "
                             "denominators is exactly the never-started liveness exclusions "
                             "(decisions/0070 ruling 6)"),
        "coverage": ("ZERO is a measured zero: every one of the "
                     f"{st1['drop_rule']['records_examined']:,} in-frame S1/S2 episode "
                     "records surviving D11 was tested for membership in its season's "
                     "listed set E, and none failed. This check did not look nowhere"),
        "direction": "would INFLATE Never started, the same direction as D4 and D9",
    }

    # --- D2, split THREE ways ----------------------------------------------
    first_s2 = np.where(loc_ok, s2_ts[np.clip(start, 0, len(s2_ts) - 1)],
                        np.iinfo(np.int64).max)
    neg = loc_ok & (first_s2 < t0_mid)
    d2 = {}
    for nm, msk, base in (("position3_220107", line3, line3),
                          ("position4_201900", line4, line4),
                          ("APPLY_position5_196654", line5, line5),
                          ("DERIV_position5_147370", d5, d5)):
        tot = int(base.sum())
        d2[nm] = {
            "population": nm, "n": tot,
            "negative_lag_pairs": int((msk & neg).sum()),
            "share_pct": 100.0 * int((msk & neg).sum()) / tot,
            "S2_finale_term_binds": int((msk & neg & (binds == "finale")).sum()),
            "S1_completion_term_binds": int((msk & neg & (binds == "s1")).sum()),
            "BOTH_terms_bind_tie": int((msk & neg & (binds == "tie")).sum()),
        }
    req["D2_negative_lag"] = {
        "split": "THREE categories -- finale binds, S1 completion binds, BOTH bind "
                 "(decisions/0070 ruling 5). A tie is its own category, not a tiebreak",
        "tie_pairs_in_line1": int((line1 & (binds == "tie")).sum()),
        "by_population": d2,
        "reading": ("S1-term negative lags are the test of the first-pass choice and should "
                    "be small; S2-finale-term negative lags are the normal case for anyone "
                    "who watched a weekly season while it aired"),
    }

    # --- D3' is per arm, already in R["per_arm"]; the 3,440 restated --------
    req["D3prime"] = {
        "per_arm": {pop: {k: v["D3prime"] for k, v in per_arm[pop].items()}
                    for pop in ("APPLY", "DERIV")},
        "the_3440": {
            "count": 3440,
            "label": "A COUNT, NOT A RATE",
            "population": ("the Step 5 UNCENSORED CLEAN-RECORD ESTIMATION SAMPLE of 128,099 "
                           "-- NOT APPLY and NOT DERIV. Measured at decisions/0034 Sec 3, "
                           "where the Started-and-left group is 17,420 before the amendment "
                           "and 15,174 after"),
            "why_a_floor": ("that sample excludes what the Step 5 waterfall drops and is not "
                            "right-censored, which is why Step 14 calls it a floor"),
            "exposure_weighting": ("weighted by SHOW RECENCY: 'at any point before tau_pull' "
                                   "gives a 2016 title about ten years of observation and a "
                                   "2025 title about eight months, so it is an "
                                   "exposure-weighted count and not a rate"),
            "restated_not_recomputed": ("decisions/0069 item 1 and task-sheet.md forbid "
                                        "reporting it against APPLY or DERIV"),
        },
    }

    # --- D8 ----------------------------------------------------------------
    tau1, tau2 = K["tau1"], K["tau2"]
    any_in_horizon = nAH > nA
    cont_over_horizon = K["f2_in_AH"] & (nAH >= THR2a[s_idx])
    d8 = {}
    for nm, msk in (("APPLY_position5", line5), ("APPLY_position6_post_liveness", line6),
                    ("DERIV_position5", d5), ("DERIV_position6_post_liveness", d6)):
        ns = msk & K["never"]
        n = int(ns.sum())
        d8[nm] = {"never_started_n": n,
                  "i_any_S2_episode_in_tau1_to_tau2": int((ns & any_in_horizon).sum()),
                  "i_share_pct": 100.0 * int((ns & any_in_horizon).sum()) / max(n, 1),
                  "ii_satisfies_the_Continued_condition_over_the_horizon":
                      int((ns & cont_over_horizon).sum()),
                  "ii_share_pct": 100.0 * int((ns & cont_over_horizon).sum()) / max(n, 1)}
    req["D8_never_started_post_window"] = {
        "measured_over": "[tau1, tau1 + H) = [tau1, tau2), H = 91 days -- NOT to the pull date",
        "by_population_and_position": d8,
        "direction": "DOWN on the headline",
        "note": ("the spec does not say whether D8 sits pre- or post-liveness, so both are "
                 "reported and labelled. D8(ii) is the only bound on the never-started "
                 "boundary and its size is Step 14 ledger item 10"),
    }

    # --- D4 ----------------------------------------------------------------
    s3_pairs = b["s3_pairs"]
    s2_any_rec = b["s2_any_rec_pairs"]
    has_s3 = np.isin(comp_pair, s3_pairs)
    has_any_s2_record = np.isin(comp_pair, s2_any_rec)
    d4mask = K["never"] & has_s3 & ~has_any_s2_record
    d4 = {}
    for nm, msk in (("APPLY_position5", line5), ("APPLY_position6_post_liveness", line6),
                    ("DERIV_position5", d5), ("DERIV_position6_post_liveness", d6)):
        ns = int((msk & K["never"]).sum())
        d4[nm] = {"never_started_n": ns, "S3_without_S2_pairs": int((msk & d4mask).sum()),
                  "share_of_never_started_pct": 100.0 * int((msk & d4mask).sum()) / max(ns, 1)}
    req["D4_S3_without_S2"] = {
        "definition": ("pairs scored Never started that carry S3-or-later episode records on "
                       "that show and NO S2 episode record at all"),
        "by_population_and_position": d4,
        "direction": "INFLATES Never started; Step 9 bounds it and publishes it ALONGSIDE",
        "emitted_here_because": ("Step 8 holds the episode-level evidence and Step 9 does "
                                 "not; leaving it out forces a second definition "
                                 "(decisions/0070 ruling 7)"),
    }

    # --- right-censoring, two lines ---------------------------------------
    req["right_censoring_two_lines"] = {
        "population_censored": "the POSITION-4 output, 201,900 (the mandated order)",
        "line_a_max_W_91_term": int((line4 & ~K["term1"]).sum()),
        "line_b_incremental_plus_H_term": int((line4 & K["term1"] & ~K["d10"]).sum()),
        "total": int((line4 & ~K["d10"]).sum()),
        "direction_line_a": "UP on the never-started share",
        "direction_line_b": "UP on the never-started share",
        "why_two_lines": ("a single combined figure would hide the price of H inside a "
                          "removal that predates it (D10)"),
    }

    # --- per-bucket D12 counts --------------------------------------------
    cad = frame.cadence_bucket.values
    bnd = frame.cadence_boundary_distance_days.values
    req["D12_cadence_buckets"] = {
        "buckets": {bk: {"shows": int((cad == bk).sum()),
                         "pairs_position4": int((line4 & (cad[s_idx] == bk)).sum()),
                         "pairs_APPLY_position5": int((line5 & (cad[s_idx] == bk)).sum()),
                         "pairs_DERIV_position5": int((d5 & (cad[s_idx] == bk)).sum())}
                    for bk in ["C0", "C1", "C2", "C3", "C4"]},
        "shows_within_1_day_of_a_bucket_boundary":
            int(np.nansum(np.abs(pd.to_numeric(bnd, errors="coerce").astype(float)) <= 1)),
        "shows_examined": n_shows,
        "coverage_note": "C0 = 0 of 1,138 shows examined, a measured zero",
    }

    # --- metadata disagreement --------------------------------------------
    dis = {}
    for c in ["s1_count_disagreement", "s2_count_disagreement",
              "s1_aired_lt_listed", "s2_aired_lt_listed"]:
        v = frame[c].values.astype(bool)
        dis[c] = {"shows": int(v.sum()),
                  "pairs_position4": int((line4 & v[s_idx]).sum())}
    req["metadata_disagreement"] = {
        "shows_examined": n_shows,
        "flags": dis,
        "s2_aired_lt_listed_direction": ("a listed-but-unaired S2 episode raises L2, which "
                                         "tightens ceil(0.90 x L2) and pushes real completers "
                                         "out of Continued into Started-and-left -- it "
                                         "OVERSTATES abandonment; where F2 never aired, "
                                         "Continued is unreachable on that show"),
        "coverage_note": ("every flag is 0 of 1,138 shows EXAMINED, not 0 because nothing "
                          "was looked at"),
    }

    # --- pull_date and fetch dates ----------------------------------------
    fetched = []
    for line in open(ROOT / "processed" / "step4" / "pull_ledger.jsonl"):
        d = json.loads(line)
        if d.get("first_page_fetched_at"):
            fetched.append((d["first_page_fetched_at"], d.get("last_page_fetched_at")))
    firsts = sorted(x[0] for x in fetched)
    lasts = sorted(x[1] for x in fetched if x[1])
    req["pull_date_and_fetch_window"] = {
        "pull_date": "2026-08-11", "tau_pull": "2026-08-11T00:00:00Z",
        "earliest_per_user_fetch": firsts[0], "latest_per_user_fetch": lasts[-1],
        "users_with_a_fetch_recorded": len(fetched),
        "records_discarded_for_watched_at_ge_tau_pull":
            st1["D11"]["records_discarded_watched_at_ge_tau_pull"],
        "of_which_in_frame_S1_or_S2_episode_records":
            st1["records"]["in_frame_S1_S2_episode_records_dropped_by_D11"],
        "constraint": "tau_pull <= the earliest per-user fetch instant",
        "note": ("the discarded tail is about one day of activity for early-fetched users "
                 "and about two for late-fetched ones; it is not evenly distributed"),
    }

    # --- the D11 open question, with its downstream effect measured --------
    req["D11_open_question"] = {
        "line_1_as_ruled": 220107,
        "line_1_if_D11_is_applied_to_the_S1_completion_walk_too": 220103,
        "pairs_affected": 4,
        "all_four_are_removed_at_position_5_under_either_reading":
            bool((~line5[comp_post_cutoff]).all()),
        "lines_4_to_7_are_identical_under_both_readings": True,
        "why": ("their first-pass completion instant is at or after tau_pull, so T0 is at or "
                "after 2026-08-10 and D10 removes them at position 5. Under the other "
                "reading they never reach position 4 at all"),
        "status": "decisions/0068 rules the base at 220,107 AND records this as OPEN",
    }

    R["required_counts"] = req

    # =====================================================================
    # EMITTED BEYOND THE REQUIRED LIST -- because Step 9 and Step 10 would
    # otherwise have to rebuild them, and two definitions of one figure is the
    # defect this study has hit most often (0058, 0061, 0062).
    # =====================================================================
    channel = (mx > K["tau1"]) & (mx < K["tau2"])     # last insertion inside (tau1, tau2)
    extras = {"_why": ("not required by Step 8. Emitted because Step 9's bound endpoints and "
                       "Step 10's residual are built from them, and rebuilding them "
                       "downstream would be a second definition")}
    for pop, p5mask, p6mask in (("APPLY", line5, line6), ("DERIV", d5, d6)):
        live = p6mask
        ch = live & ~K["contd"] & channel
        extras[pop] = {
            "position5_n": int(p5mask.sum()),
            "position7_n": int(p6mask.sum()),
            "states_position5": {"never_started": int((p5mask & K["never"]).sum()),
                                 "continued": int((p5mask & K["contd"]).sum()),
                                 "started_and_left": int((p5mask & K["sal"]).sum())},
            "liveness_exclusions": {
                "never_started": int((p5mask & K["notlive"] & K["never"]).sum()),
                "started_and_left": int((p5mask & K["notlive"] & K["sal"]).sum()),
                "accounts": int(len(np.unique(u_idx[p5mask & K["notlive"]]))),
            },
            "insertion_dormancy_channel_pairs": {
                "definition": ("RETAINED pairs, NOT Continued, live only by an insertion "
                               "after tau1, whose LAST insertion falls inside the open "
                               "window (tau1, tau2)"),
                "started_and_left": int((ch & K["sal"]).sum()),
                "never_started": int((ch & K["never"]).sum()),
                "why_the_never_started_component_does_not_widen_that_bound":
                    ("the never-started null |A| = 0 is read at tau1 and every one of these "
                     "pairs has an insertion AFTER tau1, so its null is OBSERVED, not "
                     "conceded. The started-and-left pairs differ because the Continued "
                     "condition they negate is read at tau2 and they are dormant before it"),
            },
            "p_equals_1_residual_post_position_7":
                int((p6mask & K["sal"] & (p_val >= 1.0)).sum()),
        }
    extras["scope_qualifier_of_the_Step_9_bound"] = (
        "covering with respect to INSERTION-DORMANCY, exhaustively; open only across "
        "CHANNEL CLASSES (D4, D9). D4 and D9 publish alongside and are never folded in. "
        "Step 8 does not compute the bound, but it produces the position-6 population the "
        "bound is stated on, so any table or note carrying the bound carries this qualifier "
        "(decisions/0062)")

    # the account base: absent accounts are ABSENT, not empty
    outc: dict = {}
    for line in open(ROOT / "processed" / "step4" / "pull_ledger.jsonl"):
        o = json.loads(line).get("outcome")
        outc[o] = outc.get(o, 0) + 1
    extras["account_base"] = {
        "accounts_in_the_sweep": int(n_users),
        "accounts_reaching_the_position_5_population": int(len(np.unique(u_idx[line5]))),
        "pull_ledger_outcomes": outc,
        "note": ("accounts that were skipped, discarded over tolerance or never attempted are "
                 "ABSENT, not empty. CLAUDE.md requires an access_denied user to stay "
                 "distinguishable downstream, because a skipped user silently read as empty "
                 "becomes a false 'never started' in the headline. No such account "
                 "contributes a row to this table"),
    }
    R["emitted_beyond_the_required_list"] = extras

    np.savez(OUT / "masks.npz", line1=line1, line2=line2, line3=line3, line4=line4,
             line4_step5=line4_step5, line5=line5, line6=line6, deriv5=d5, deriv6=d6,
             never=K["never"], contd=K["contd"], sal=K["sal"], notlive=K["notlive"],
             nA=nA, nAH=nAH, p=p_val, u_idx=u_idx, s_idx=s_idx, comp_pair=comp_pair,
             t0_mid=t0_mid, tau1=tau1, tau2=tau2, binds=binds,
             has_s3=has_s3, has_any_s2_record=has_any_s2_record,
             in_a=in_a_u[u_idx], in_b=in_b_u[u_idx], m_H=m_H,
             first_s2=first_s2, loc_ok=loc_ok, comp_date_mid=comp_date_mid)

    R["elapsed_s"] = time.time() - t
    (OUT / "results.json").write_text(json.dumps(R, indent=2, default=str))
    print(json.dumps({k: R[k] for k in ("waterfall_APPLY", "waterfall_DERIV")},
                     indent=2, default=str))
    a = per_arm["APPLY"]["108"]
    d = per_arm["DERIV"]["108"]
    print(f"\nAPPLY n={a['position5_n']:,} excluded {a['liveness_excluded']} "
          f"= {a['liveness_excluded_never_started']} NS + "
          f"{a['liveness_excluded_started_and_left']} SL from "
          f"{a['accounts_supplying_exclusions']} accounts")
    print(f"DERIV n={d['position5_n']:,} excluded {d['liveness_excluded']} "
          f"= {d['liveness_excluded_never_started']} NS + "
          f"{d['liveness_excluded_started_and_left']} SL from "
          f"{d['accounts_supplying_exclusions']} accounts")
    print(f"({time.time()-t:.1f}s)")


if __name__ == "__main__":
    main()
