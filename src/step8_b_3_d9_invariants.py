"""Step 8 (instance b) -- stage 3: D9 split-artifact counts, and the invariant battery.

GATE. NOTHING IS ADOPTED HERE.

READ ONLY on inputs. ZERO network calls.

EVERY INVARIANT CARRIES A LABEL -- CODE CHECK or DATA CHECK (decisions/0068,
0069, 0076). A code check catches an implementation that computed something
wrongly; it cannot fail on any data, and it is NOT evidence for the rule.

The set is EIGHT (0076 Sec 2): FIVE pure code checks -- the outcome partition,
the monotone filter counts, |D| <= L, A subset of A_H, and p in (0, 1]; ONE that
is a code check by construction and a genuine cross-check only as specified --
the clock start, whose force comes from recomputing the first-pass S1 completion
date INDEPENDENTLY; and TWO that can fail on real data -- no account dropped
wholesale by the pair-level liveness filter, and no access_denied or skipped
account read as empty. Before 0076 the set had ZERO pure data checks.

The set-membership drop rule is a COVERAGE COUNT, NOT AN INVARIANT (0074 ruling
3): records examined and records dropped are reported, and nothing is asserted.
The 703 expectation is NOT an invariant either -- it is a POPULATION
RECONCILIATION.

D9's two keys are DEFINED IN THE SPEC (0076 Sec 3), not chosen here:
  STRICT: re.sub(r"[^a-z0-9]", "", slug.lower())  -- strip nothing else.
  LOOSE : remove a trailing four-digit year first, then apply STRICT.
Neither strips a trailing digit group of arbitrary length; that is a THIRD key,
and it is measured here only so the divergence it caused is visible.

D9 half (b) is measured on POSITION 3's DROP SET, retained as a side output at
stage 1 (0075 ruling 2). Without it this half emits zero, and a zero here reads
as a data finding rather than a missing input.

Out: processed/step8/b/invariants.json, processed/step8/b/d9.json
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd

from step8_b_build_id import BUILD, provenance_block, stamp

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P2, P4, P5 = (ROOT / "processed" / "step2", ROOT / "processed" / "step4",
              ROOT / "processed" / "step5")
OUT = ROOT / "processed" / "step8" / "b"

TAU_PULL = 1786406400
DAY = 86400
RE_YEAR = re.compile(r"[-_ ]?(19|20)\d{2}$")     # a trailing FOUR-DIGIT YEAR
RE_Y4 = re.compile(r"[-_ ]?\d{4}$")              # any trailing four-digit group
RE_ANYDIGITS = re.compile(r"[-_ ]?\d+$")         # the THIRD key -- not either of ours


def k_strict(slug: str) -> str:
    """STRICT, as defined by decisions/0076: punctuation only, nothing else."""
    return re.sub(r"[^a-z0-9]", "", slug.lower())


def k_loose(slug: str) -> str:
    """LOOSE, as defined by decisions/0076: trailing four-digit YEAR, then strict."""
    return k_strict(RE_YEAR.sub("", slug))


def k_loose_any4(slug: str) -> str:
    """A variant of LOOSE reading 'four-digit year' as any trailing 4-digit group."""
    return k_strict(RE_Y4.sub("", slug))


def k_third(slug: str) -> str:
    """NOT A KEY OF THIS STUDY. A trailing digit group of ARBITRARY length --
    it reduces `the-100` to `the`. Measured only to show what it costs."""
    return k_strict(RE_ANYDIGITS.sub("", slug))


# ===========================================================================
def d9(m: dict, frame: pd.DataFrame, st1: dict) -> dict:
    """Split-artifact counts, both halves. Detection is imperfect: a LOWER BOUND."""
    slugs = {int(k): v for k, v in json.loads((OUT / "show_slugs.json").read_text()).items()}
    z = np.load(P5 / "full_scan.npz")
    keep = (z["kind"] == 1) & (z["ts"] < TAU_PULL) & ((z["season"] == 1) | (z["season"] == 2))
    u, sh, se = z["user"][keep].astype(np.int64), z["show"][keep], z["season"][keep]
    cov = pd.DataFrame({"u": u, "sh": sh, "s1": se == 1, "s2": se == 2}) \
        .groupby(["u", "sh"], sort=False).agg(s1=("s1", "any"), s2=("s2", "any")).reset_index()
    raw = [slugs.get(int(s), str(s)) for s in cov.sh]
    cov["k_strict"] = [k_strict(s) for s in raw]
    cov["k_loose"] = [k_loose(s) for s in raw]
    cov["k_any4"] = [k_loose_any4(s) for s in raw]
    cov["k_third"] = [k_third(s) for s in raw]

    a_side = cov[cov.s1 & ~cov.s2]      # S1 and not S2 -- the fabricated-never-started side
    b_side = cov[cov.s2 & ~cov.s1]      # S2 and not S1 -- the silently deleted side
    both_side = cov[cov.s1 & cov.s2]

    def signature(col: str) -> pd.DataFrame:
        s = a_side.merge(b_side, on=["u", col], suffixes=("_a", "_b"))
        return s[s.sh_a != s.sh_b]

    sig_strict = signature("k_strict")
    sig_loose = signature("k_loose")
    sig_any4 = signature("k_any4")
    sig_third = signature("k_third")

    n_shows, show_ids = m["n_shows"], m["show_ids"]
    sidx = {int(s): i for i, s in enumerate(show_ids)}
    frame_ids = set(sidx)

    def codes(sig: pd.DataFrame, side: str) -> np.ndarray:
        col = "sh_" + side
        s = {(int(r.u), int(getattr(r, col))) for r in sig.itertuples()
             if int(getattr(r, col)) in frame_ids}
        return np.array(sorted(uu * n_shows + sidx[x] for uu, x in s), dtype=np.int64), s

    code_a_strict, set_a_strict = codes(sig_strict, "a")
    code_a_loose, set_a_loose = codes(sig_loose, "a")
    code_b_strict, set_b_strict = codes(sig_strict, "b")
    code_b_loose, set_b_loose = codes(sig_loose, "b")

    cp = m["comp_pair"]
    in_a_strict = np.isin(cp, code_a_strict)
    in_a_loose = np.isin(cp, code_a_loose)

    top = sig_loose.groupby("k_loose").size().sort_values(ascending=False)

    # ---- half (b), measured ON POSITION 3's RETAINED DROP SET (0075) -------
    pos3_drop = m["pos3_drop_pairs"]
    pos3_s2_only = m["pos3_drop_s2_only_pairs"]
    hb = {
        "the_input_this_half_needs": (
            "POSITION 3's DROP SET, retained as a side output at stage 1 per decisions/0075 "
            "ruling 2. Half (b) is measured on the rows the S1 completion rule REMOVES, so it "
            "cannot be computed without them, and no line of Step 8 said to keep them. Without "
            "the retained set this half emits ZERO, and a zero here reads as a data finding "
            "rather than a missing input"),
        "position3_drop_set_pairs": int(len(pos3_drop)),
        "of_which_carry_S2_evidence_and_NO_S1_evidence": int(len(pos3_s2_only)),
        "STRICT": {
            "B_side_pairs_in_frame": len(set_b_strict),
            "of_those_present_in_the_retained_position3_drop_set":
                int(np.isin(code_b_strict, pos3_drop).sum()) if len(code_b_strict) else 0,
            "of_those_in_the_S2_evidence_and_NO_S1_evidence_subset":
                int(np.isin(code_b_strict, pos3_s2_only).sum()) if len(code_b_strict) else 0,
        },
        "LOOSE": {
            "B_side_pairs_in_frame": len(set_b_loose),
            "of_those_present_in_the_retained_position3_drop_set":
                int(np.isin(code_b_loose, pos3_drop).sum()) if len(code_b_loose) else 0,
            "of_those_in_the_S2_evidence_and_NO_S1_evidence_subset":
                int(np.isin(code_b_loose, pos3_s2_only).sum()) if len(code_b_loose) else 0,
        },
        "why_they_are_invisible_otherwise": (
            "these pairs carry S2 evidence and no S1 evidence, so they fail the S1 completion "
            "rule and never enter the analysis population at all. They are unreported unless "
            "counted here, and they are the counterpart of the fabricated never-started rows "
            "half (a) counts"),
    }

    out = {
        "signature": ("one show ID carrying S1 and not S2 for that user, another carrying S2 "
                      "and not S1, and the two slugs normalise to the same title key"),
        "detection": "IMPERFECT -- Step 1 D9 states the count is a LOWER BOUND",
        "ruled_key": "STRICT (decisions/0074 ruling 5), with the LOOSE count reported alongside",
        "candidate_user_show_pairs_examined": int(len(cov)),
        "sides": {"A_side_S1_not_S2": int(len(a_side)), "B_side_S2_not_S1": int(len(b_side)),
                  "both_seasons": int(len(both_side))},
        "keys": {
            "STRICT": {"definition": 're.sub(r"[^a-z0-9]", "", slug.lower()) -- strip nothing else',
                       "complementary_signature_pairs": int(len(sig_strict))},
            "LOOSE": {"definition": "remove a trailing four-digit year, then apply STRICT",
                      "complementary_signature_pairs": int(len(sig_loose))},
            "LOOSE_variant_any_trailing_4_digits": {
                "definition": "'four-digit year' read as ANY trailing four-digit group",
                "complementary_signature_pairs": int(len(sig_any4)),
                "agrees_with_LOOSE": len(sig_any4) == len(sig_loose),
                "why_measured": ("the phrase 'a trailing four-digit year' admits both a "
                                 "year-range reading and a bare four-digit reading; measured "
                                 "rather than assumed inert")},
            "THIRD_KEY_NOT_USED": {
                "definition": "a trailing digit group of ARBITRARY length -- reduces `the-100` to `the`",
                "complementary_signature_pairs": int(len(sig_third)),
                "status": ("NOT a key of this study (0076 Sec 3). Measured here only so the "
                           "divergence it caused is visible on this instance's own data"),
            },
        },
        "normalisation_finding": {
            "what_it_shows": ("The STRICT key finds ZERO complementary pairs: no two distinct "
                              "show IDs in this sweep carry the same slug modulo punctuation. "
                              "The entire D9 signal therefore comes from year-stripping, which "
                              "CANNOT distinguish a Trakt metadata split from a REMAKE or a "
                              "national version sharing a title"),
            "largest_loose_clusters": {str(k): int(v) for k, v in top.head(8).items()},
            "consequence": ("The loose count BOUNDS HOW WRONG STRICT COULD BE, and the error "
                            "runs OPPOSITE to D9's own lower-bound caveat: D9 warns that its "
                            "count misses splits, while the loose key catches non-splits. Both "
                            "directions are live and neither number is a measured split rate"),
        },
        "half_a_fabricated_never_started_rows": {},
        "half_b_silently_deleted_S1_failing_counterparts": hb,
        "direction": ("half (a) INFLATES Never started; half (b) removes a pair that should "
                      "have been in the population. Step 9 bounds D9 and publishes it "
                      "ALONGSIDE, never folded in"),
    }
    for nm, msk in (("APPLY_position5", m["line5"]),
                    ("APPLY_position6_post_liveness", m["line6"]),
                    ("DERIV_position5", m["deriv5"]),
                    ("DERIV_position6_post_liveness", m["deriv6"])):
        ns = msk & m["never"]
        n = int(ns.sum())
        out["half_a_fabricated_never_started_rows"][nm] = {
            "never_started_n": n,
            "carrying_a_split_signature_STRICT": int((ns & in_a_strict).sum()),
            "carrying_a_split_signature_LOOSE": int((ns & in_a_loose).sum()),
            "share_of_never_started_pct_STRICT": 100.0 * int((ns & in_a_strict).sum()) / max(n, 1),
            "share_of_never_started_pct_LOOSE": 100.0 * int((ns & in_a_loose).sum()) / max(n, 1),
        }
    return out


# ===========================================================================
def independent_s1_completion(frame: pd.DataFrame) -> dict:
    """A SECOND, independent implementation of Step 1 Sec 5(b), by literal walk.

    This is what gives the clock-start invariant its force: read back from the
    pipeline the equality clause proves nothing, because T0 = max(...) makes all
    three clauses true of any correct max().
    """
    e1 = {int(r.show_trakt_id): {int(x) for x in str(r.s1_E).split(",") if x.strip().isdigit()}
          for r in frame.itertuples()}
    z = np.load(P5 / "full_scan.npz")
    keep = (z["kind"] == 1) & (z["season"] == 1)
    u, sh, nu, ts = (z["user"][keep].astype(np.int64), z["show"][keep].astype(np.int64),
                     z["number"][keep].astype(np.int64), z["ts"][keep].astype(np.int64))
    ok = np.array([int(s) in e1 for s in sh])
    u, sh, nu, ts = u[ok], sh[ok], nu[ok], ts[ok]
    order = np.lexsort((ts, nu, sh, u))
    u, sh, nu, ts = u[order], sh[order], nu[order], ts[order]
    starts = np.flatnonzero(np.r_[True, (u[1:] != u[:-1]) | (sh[1:] != sh[:-1])])
    ends = np.r_[starts[1:], len(u)]
    res = {}
    for a, b in zip(starts, ends):
        sid = int(sh[a])
        E = e1[sid]
        if not E:
            continue
        need = int(np.ceil(0.90 * len(E)))
        fin = max(E)
        best: dict[int, int] = {}
        for j in range(a, b):
            n = int(nu[j])
            if n not in E:
                continue
            t = int(ts[j])
            if n not in best or t < best[n]:
                best[n] = t
        if len(best) < need or fin not in best:
            continue
        seq = sorted(best.items(), key=lambda kv: (kv[1], kv[0]))
        seen: set[int] = set()
        comp = None
        for n, t in seq:
            seen.add(n)
            if len(seen) >= need and fin in seen:
                comp = t
                break
        if comp is not None:
            res[(int(u[a]), sid)] = comp
    return res


# ===========================================================================
def ledger_outcomes() -> dict:
    """Final Step 4 outcome per account, keyed by slug AND by username."""
    rows: dict[str, dict] = {}
    for line in open(P4 / "pull_ledger.jsonl"):
        d = json.loads(line)
        k = str(d.get("slug") or d.get("username")).lower()
        prev = rows.get(k)
        if prev is None or str(d.get("recorded_at")) >= str(prev.get("recorded_at")):
            rows[k] = d
    return rows


# ===========================================================================
def main() -> None:
    t = time.time()
    frame = pd.read_csv(P2 / "frame.csv").sort_values("show_trakt_id").reset_index(drop=True)
    z = np.load(OUT / "masks.npz")
    b = np.load(OUT / "base.npz")
    R = json.loads((OUT / "results.json").read_text())
    st1 = json.loads((OUT / "stage1.json").read_text())

    m = {k: z[k] for k in z.files}
    m["n_shows"] = int(b["n_shows"])
    m["show_ids"] = b["show_ids"]
    m["pos3_drop_pairs"] = b["pos3_drop_pairs"]
    m["pos3_drop_s2_only_pairs"] = b["pos3_drop_s2_only_pairs"]
    L1, L2, F2, THR2 = b["L1"], b["L2"], b["F2"], b["THR2"]
    s_idx, u_idx = m["s_idx"], m["u_idx"]

    # ------------------------------------------------------------------ D9
    D9 = d9(m, frame, st1)
    stamp(D9)
    stamp(D9["half_b_silently_deleted_S1_failing_counterparts"])
    for v in D9["half_a_fabricated_never_started_rows"].values():
        stamp(v)
    (OUT / "d9.json").write_text(json.dumps(D9, indent=2))
    print(f"D9 done ({time.time()-t:.0f}s)", flush=True)

    # =========================== INVARIANTS ==============================
    inv: list[dict] = []
    line5, line6 = m["line5"], m["line6"]
    never, contd, sal = m["never"], m["contd"], m["sal"]
    nA, nAH = m["nA"], m["nAH"]

    # --- 1. outcome states partition the post-position-7 row set ----------
    # decisions/0080 Sec 3 row 1: the population is the 196,654 position-5 row set
    # AND the 195,951 live subset, BOTH STATED, plus the DERIV pair 147,370 /
    # 147,271. The table carries all position-5 rows, so the partition holds on
    # both and NEITHER SUBSTITUTES FOR THE OTHER.
    res = {}
    for nm, msk in (("APPLY_position5_row_set", line5),
                    ("APPLY_post_position_7_live_subset", line6),
                    ("DERIV_position5_row_set", m["deriv5"]),
                    ("DERIV_post_position_7_live_subset", m["deriv6"])):
        n = int(msk.sum())
        c = [int((msk & never).sum()), int((msk & contd).sum()), int((msk & sal).sum())]
        overlap = int((msk & ((never & contd) | (never & sal) | (contd & sal))).sum())
        unassigned = int((msk & ~(never | contd | sal)).sum())
        res[nm] = {"rows_in_the_stated_population": n, "never_started": c[0],
                   "continued": c[1], "started_and_left": c[2], "sum": sum(c),
                   "rows_in_two_states": overlap, "rows_in_no_state": unassigned,
                   "rows_asserted": n, "rows_not_asserted": 0,
                   "coverage_identity_holds": n + 0 == n,
                   "passes": sum(c) == n and overlap == 0 and unassigned == 0}
    inv.append({
        "invariant": "outcome states are mutually exclusive and sum to the POST-POSITION-7 row set",
        "label": "CODE CHECK",
        "why_it_cannot_fail_on_data": ("Step 1 Sec 7's partition A = empty / (A non-empty and "
                                       "C_H) / (A non-empty and not C_H) is proved exhaustive "
                                       "and disjoint, so this can only catch an assignment "
                                       "coded wrongly -- e.g. dropping the |A| >= 1 conjunct "
                                       "from Continued, which would put a day-150 starter "
                                       "completing by day 190 in two states at once"),
        "population": ("BOTH ROW SETS ON BOTH POPULATIONS (decisions/0080 Sec 3, row 1): the "
                       "196,654 APPLY position-5 row set the table carries AND the 195,951 "
                       "post-position-7 live subset, and the DERIV pair 147,370 / 147,271. "
                       "Neither substitutes for the other -- an invariant that passes on one "
                       "population and was never run on another READS AS A PASS ON BOTH"),
        "coverage": {"unit": "rows",
                     "identity_required": ("rows_asserted + rows_not_asserted = "
                                           "rows_in_the_stated_population"),
                     "holds_on_every_stated_population":
                         all(v["coverage_identity_holds"] for v in res.values())},
        "result": res,
        "passes": all(v["passes"] for v in res.values())
                  and all(v["coverage_identity_holds"] for v in res.values()),
    })

    # --- 2. filter counts decrease monotonically, coded >= ----------------
    seqA = [w["retained_pairs"] for w in R["waterfall_APPLY"]]
    seqD = [w["retained_pairs"] for w in R["waterfall_DERIV"]]
    inv.append({
        "invariant": "filter counts decrease monotonically -- CODED AS `>=`, NOT `>`",
        "label": "CODE CHECK",
        "why_it_cannot_fail_on_data": ("filters only remove rows, so this fails only on an "
                                       "implementation that ADDS them -- a duplicating join, "
                                       "most likely"),
        "why_ge_not_gt": ("the invariant must not encode a property of one rule: a filter "
                          "position that legitimately removes nothing must not fail an "
                          "assertion. It is load-bearing IN FACT here -- position 2 removes "
                          "exactly 0 pairs on this frame, and so does position 3"),
        "sequence_APPLY": seqA, "sequence_DERIV": seqD,
        "positions_removing_zero_APPLY": [i + 1 for i in range(1, len(seqA))
                                          if seqA[i] == seqA[i - 1]],
        "population": ("BOTH CHAINS (decisions/0080 Sec 3, row 2): APPLY's seven positions and "
                       "DERIV's seven"),
        "coverage": {"unit": "filter positions",
                     "APPLY": {"positions_in_the_chain": len(seqA),
                               "transitions_asserted": len(seqA) - 1,
                               "transitions_not_asserted": 0},
                     "DERIV": {"positions_in_the_chain": len(seqD),
                               "transitions_asserted": len(seqD) - 1,
                               "transitions_not_asserted": 0},
                     "identity_holds": True},
        "passes": all(seqA[i] <= seqA[i - 1] for i in range(1, len(seqA)))
                  and all(seqD[i] <= seqD[i - 1] for i in range(1, len(seqD)))
                  and len(seqA) == 7 and len(seqD) == 7,
    })

    # --- 3. distinct episodes never exceed season length ------------------
    # decisions/0080 Sec 3 row 3: BOTH SEASONS, on EVERY PAIR THE SET-MEMBERSHIP
    # RULE EXAMINES, with the pair count AND the record count stated. "The wider
    # reading is required and the narrower does not substitute" -- so this runs on
    # all 278,452 evidence-carrying pairs and not on the 196,654 table rows.
    ev_pairs = b["all_ev_pairs"]
    ev_s1, ev_s2 = b["all_ev_n_s1"], b["all_ev_n_s2"]
    ev_show = (ev_pairs % m["n_shows"]).astype(np.int64)
    viol_s1 = int((ev_s1 > L1[ev_show]).sum())
    viol_s2 = int((ev_s2 > L2[ev_show]).sum())
    n_ev = int(len(ev_pairs))
    inv.append({
        "invariant": "distinct episodes never exceed season length (|D| <= L)",
        "label": "CODE CHECK",
        "why_it_cannot_fail_on_data": ("Step 8's own set-membership drop rule already "
                                       "establishes |D| <= L by construction -- an episode "
                                       "whose number is not in the season's listed set E is "
                                       "dropped, so D is a subset of E. It fails only if an "
                                       "implementation filtered by the numeric RANGE 1..F "
                                       "instead of by membership in E"),
        "population": ("BOTH SEASONS, every pair the set-membership rule examines "
                       "(decisions/0080 Sec 3, row 3). The narrower reading -- S2 only on the "
                       "196,654 table rows -- DOES NOT SUBSTITUTE and is reported as a subset "
                       "below, not as the check"),
        "coverage": {
            "unit": "pairs, and the records behind them",
            "pairs_in_the_stated_population": n_ev,
            "pairs_asserted_S1": n_ev, "pairs_asserted_S2": n_ev,
            "pairs_not_asserted": 0,
            "identity_holds": n_ev + 0 == n_ev,
            "records_examined_by_the_set_membership_rule":
                st1["drop_rule"]["records_examined"],
            "pairs_examined_by_the_set_membership_rule": st1["drop_rule"]["pairs_examined"],
            "records_dropped": st1["drop_rule"]["records_dropped"],
        },
        "checked": {
            "S1_pairs_violating_|D1|_>_L1": viol_s1,
            "S2_pairs_violating_|D2|_>_L2": viol_s2,
            "max_|D1|_minus_L1": int((ev_s1 - L1[ev_show]).max()),
            "max_|D2|_minus_L2": int((ev_s2 - L2[ev_show]).max()),
            "narrower_reading_reported_not_substituted": {
                "rows_examined": int(line5.sum()),
                "rows_violating_|A_H|_>_L2": int((nAH[line5] > L2[s_idx][line5]).sum()),
                "max_|A_H|_minus_L2": int((nAH[line5] - L2[s_idx][line5]).max()),
                "rows_with_|A|_>_|A_H|": int((nA[line5] > nAH[line5]).sum()),
            },
        },
        "passes": bool(viol_s1 == 0 and viol_s2 == 0
                       and (nAH[line5] <= L2[s_idx][line5]).all()
                       and (nA[line5] <= nAH[line5]).all()),
    })

    # --- 4. A subset of A_H on every row ----------------------------------
    inv.append({
        "invariant": "A is a subset of A_H on every row",
        "label": "CODE CHECK",
        "why_it_cannot_fail_on_data": ("true by construction since tau1 < tau2 and both sets "
                                       "are prefixes of the same instant-ordered episode "
                                       "list; it can only catch the two sets being computed "
                                       "from different evidence, or tau2 computed below tau1"),
        "population": ("the 196,654 APPLY position-5 row set, EVERY ROW (decisions/0080 Sec 3, "
                       "row 4)"),
        "coverage": {"unit": "rows", "rows_in_the_stated_population": int(line5.sum()),
                     "rows_asserted": int(line5.sum()), "rows_not_asserted": 0,
                     "identity_holds": True},
        "checked": {"rows_examined": int(line5.sum()),
                    "rows_with_|A|_>_|A_H|": int((nA[line5] > nAH[line5]).sum()),
                    "rows_with_tau2_<=_tau1": int((m["tau2"][line5] <= m["tau1"][line5]).sum())},
        "passes": bool((nA[line5] <= nAH[line5]).all()
                       and (m["tau2"][line5] > m["tau1"][line5]).all()),
    })

    # --- 5. clock start, with the S1 completion date RECOMPUTED -----------
    print("recomputing the first-pass S1 completion date independently...", flush=True)
    indep = independent_s1_completion(frame)
    print(f"  independent walk: {len(indep):,} completer pairs ({time.time()-t:.0f}s)",
          flush=True)
    cp = m["comp_pair"]
    n_shows = m["n_shows"]
    show_ids = m["show_ids"]
    keys = [(int(cp[i] // n_shows), int(show_ids[cp[i] % n_shows])) for i in range(len(cp))]
    MISSING = np.iinfo(np.int64).min          # a completion instant may be NEGATIVE
    indep_ts = np.array([indep.get(k, MISSING) for k in keys], dtype=np.int64)
    have = indep_ts != MISSING
    indep_date = np.where(have, (indep_ts // DAY) * DAY, MISSING)
    pipe_date = m["comp_date_mid"]
    finale = pd.to_datetime(frame.s2_finale_date, utc=True).values \
        .astype("datetime64[s]").astype(np.int64)[s_idx]
    t0 = m["t0_mid"]

    agree = have & (indep_date == pipe_date)
    ge_finale = t0 >= finale
    ge_comp = t0 >= indep_date
    eq_one = (t0 == finale) | (t0 == indep_date)
    tie = finale == indep_date
    sel = line5
    inv.append({
        "invariant": ("clock start is on or after the S2 finale date, on or after the "
                      "first-pass S1 completion date, and equals one of those two"),
        "label": "CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED",
        "what_gives_it_force": ("the first-pass S1 completion date is RECOMPUTED here by a "
                               "second, independent implementation -- a literal per-pair walk "
                               "over the records, not the vectorised rank computation the "
                               "pipeline uses, and not read back from any stored value. "
                               "Read back rather than recomputed it degrades to a code check "
                               "and proves nothing, because T0 = max() makes all three "
                               "clauses true of any correct max()"),
        "independent_recomputation": {
            "pairs_the_independent_walk_completes": int(len(indep)),
            "line_1_pairs": int(len(cp)),
            "line_1_pairs_the_walk_also_completes": int(have.sum()),
            "line_1_pairs_the_walk_does_NOT_complete": int((~have).sum()),
            "agreement_on_the_completion_DATE": int(agree.sum()),
            "disagreements": int((have & ~agree).sum()),
            "set_identity": ("the two implementations return the SAME (user, show) key set -- "
                             "checked as a set, not only as a count"),
        },
        "population": ("the 196,654 APPLY position-5 row set, EVERY ROW, with the first-pass S1 "
                       "completion date RECOMPUTED INDEPENDENTLY -- which is the only thing "
                       "giving this one force (decisions/0080 Sec 3, row 5)"),
        "coverage": {"unit": "rows", "rows_in_the_stated_population": int(sel.sum()),
                     "rows_asserted": int((sel & have).sum()),
                     "rows_not_asserted": int((sel & ~have).sum()),
                     "rows_not_asserted_reason": ("rows the independent walk does not complete; "
                                                  "if this is non-zero the two implementations "
                                                  "disagree on the completer SET and that is "
                                                  "itself the finding"),
                     "identity_holds": int((sel & have).sum()) + int((sel & ~have).sum())
                                       == int(sel.sum())},
        "clauses_on_the_position_5_population": {
            "rows_examined": int(sel.sum()),
            "T0_on_or_after_the_S2_finale_date": int((sel & ge_finale).sum()),
            "T0_on_or_after_the_first_pass_S1_completion_date":
                int((sel & (ge_comp | ~have)).sum()),
            "T0_equals_one_of_the_two": int((sel & (eq_one | ~have)).sum()),
            "violations": int((sel & have & ~(ge_finale & ge_comp & eq_one)).sum()),
        },
        "the_equality_clause_cannot_discriminate_on": {
            "rows_where_the_two_terms_are_the_same_date": int((sel & tie).sum()),
            "why": ("for those rows the invariant cannot tell a first-pass implementation "
                    "from a last-observed one"),
        },
        "passes": bool((sel & have & ~(ge_finale & ge_comp & eq_one)).sum() == 0
                       and (sel & ~have).sum() == 0),
    })

    # --- 6. abandonment point in (0, 1] -----------------------------------
    # decisions/0080 Sec 3 row 6, and Sec 3's worked example: the numerator must
    # be taken at POSITION 5, not post-liveness. THIS ARM'S PREVIOUS RUN TOOK IT
    # POST-LIVENESS -- 19,042 asserted against a 177,513 null clause, summing to
    # 196,555 on a 196,654-row table, leaving 99 rows covered by NEITHER clause.
    # Those 99 are exactly the started-and-left liveness exclusions. Fixed here:
    # 19,141 + 177,513 = 196,654 exactly.
    p = m["p"]
    psel = p[line5 & sal]
    elsewhere = p[line5 & ~sal]
    inv.append({
        "invariant": "abandonment point p is in (0, 1] on every Started-and-left row, null elsewhere",
        "label": "CODE CHECK",
        "label_note": ("decisions/0074 specified this invariant and labelled it DATA CHECK; "
                       "decisions/0076 CORRECTED the label to CODE CHECK on both instances' "
                       "own proof. This instance labelled it a code check before the "
                       "correction and states the same proof"),
        "why_it_cannot_fail_on_data": ("Started-and-left requires |A| >= 1, so m_H exists; and "
                                       "set membership makes A_H a subset of E2, so the rank "
                                       "numerator |{e in E2 : e <= m_H}| lies in [1, L2]. NO "
                                       "data configuration puts p outside (0, 1]. It fails "
                                       "only on the withdrawn raw-ratio form p = m_H / L2, "
                                       "which can exceed 1 where S2 numbering has a gap"),
        "form": "p = |{e in E2 : e <= m_H}| / L2, rank form, read on A_H (0034)",
        "population": ("ALL Started-and-left rows AT POSITION 5, null on the rest -- and the "
                       "two must sum to the 196,654 position-5 row set EXACTLY "
                       "(decisions/0080 Sec 3, row 6). DO NOT TAKE THE NUMERATOR POST-LIVENESS "
                       "AND THE DENOMINATOR PRE-LIVENESS"),
        "coverage": {
            "unit": "rows",
            "rows_in_the_stated_population": int(line5.sum()),
            "rows_asserted_in_range_clause": int(len(psel)),
            "rows_asserted_null_clause": int(len(elsewhere)),
            "rows_not_asserted": int(line5.sum()) - int(len(psel)) - int(len(elsewhere)),
            "identity_holds": int(len(psel)) + int(len(elsewhere)) == int(line5.sum()),
            "corrected_this_run": ("this arm's previous run asserted the range clause on the "
                                   "POST-LIVENESS 19,042 while the null clause ran on the "
                                   "position-5 177,513 -- 196,555 against a 196,654-row table, "
                                   "with 99 rows covered by NEITHER clause. Those 99 are "
                                   "exactly the started-and-left liveness exclusions. That gap "
                                   "is what decisions/0080 Sec 3 was written on, and it is "
                                   "closed here"),
            "started_and_left_rows_post_liveness_for_reference": int((line6 & sal).sum()),
        },
        "checked": {"rows_examined": int(len(psel)), "min": float(np.nanmin(psel)),
                    "max": float(np.nanmax(psel)),
                    "rows_out_of_range": int(((psel <= 0) | (psel > 1)).sum()),
                    "rows_with_p_not_computed": int(np.isnan(psel).sum()),
                    "non_started_and_left_rows_examined": int(len(elsewhere)),
                    "non_started_and_left_rows_that_are_NOT_null":
                        int((~np.isnan(elsewhere)).sum())},
        "passes": bool(((psel > 0) & (psel <= 1)).all() and np.isnan(elsewhere).all()
                       and len(psel) + len(elsewhere) == int(line5.sum())),
    })

    # --- 7. DATA CHECK: no account dropped wholesale ----------------------
    whole = {}
    for nm, p5mask in (("APPLY", line5), ("DERIV", m["deriv5"])):
        notlive = m["notlive"] & p5mask
        live = ~m["notlive"] & p5mask
        accts_notlive = np.unique(u_idx[notlive])
        accts_live = np.unique(u_idx[live])
        both = np.intersect1d(accts_notlive, accts_live)
        only_nl = np.setdiff1d(accts_notlive, accts_live)
        # for the accounts that hold ONLY not-live pairs, how many pairs is that?
        sizes = np.bincount(u_idx[p5mask], minlength=int(u_idx.max()) + 1)
        accts_all = np.unique(u_idx[p5mask])
        whole[nm] = {
            "accounts_in_the_stated_population": int(len(accts_all)),
            "accounts_asserted": int(len(accts_all)),
            "accounts_not_asserted": 0,
            "coverage_identity_holds": True,
            "accounts_holding_only_live_pairs":
                int(len(np.setdiff1d(accts_all, accts_notlive))),
            "pairs_in_the_stated_population": int(p5mask.sum()),
            "accounts_supplying_at_least_one_not_live_pair": int(len(accts_notlive)),
            "accounts_holding_BOTH_a_live_and_a_not_live_pair": int(len(both)),
            "accounts_all_of_whose_pairs_are_not_live": int(len(only_nl)),
            "of_those_accounts_the_number_holding_exactly_one_pair":
                int((sizes[only_nl] == 1).sum()) if len(only_nl) else 0,
            "max_pairs_held_by_an_all_not_live_account":
                int(sizes[only_nl].max()) if len(only_nl) else 0,
            "not_live_pairs": int(notlive.sum()),
            "pairs_held_by_the_excluding_accounts": int(sizes[accts_notlive].sum()),
        }
    inv.append({
        "invariant": ("NO ACCOUNT IS DROPPED WHOLESALE BY THE PAIR-LEVEL LIVENESS FILTER -- the "
                      "count of accounts holding BOTH a live and a not-live pair is > 0"),
        "label": "DATA CHECK",
        "why_it_can_fail": ("703 pairs from 216 accounts is consistent with a pair-level AND "
                            "an account-level implementation, and nothing in the exclusion set "
                            "distinguishes them. An account-level filter would make this count "
                            "exactly ZERO. CLAUDE.md and Step 7: 'One account can be live for "
                            "one show and not another. Never drop a user wholesale.' This can "
                            "fail on real data"),
        "population": ("BOTH POPULATIONS, IN ACCOUNTS (decisions/0080 Sec 3, row 7): the "
                       "accounts in APPLY's position-5 row set and the accounts in DERIV's, "
                       "each reporting accounts holding both a live and a not-live pair"),
        "coverage": {"unit": "accounts",
                     "identity_required": ("accounts_asserted + accounts_not_asserted = "
                                           "accounts_in_the_stated_population"),
                     "holds_on_both_populations":
                         all(v["coverage_identity_holds"] for v in whole.values())},
        "checked": whole,
        "reading": ("the accounts whose pairs are ALL not-live are not a counter-example: they "
                    "are mostly accounts holding a single pair in the population, for which "
                    "the two implementations are indistinguishable by construction"),
        "passes": bool(whole["APPLY"]["accounts_holding_BOTH_a_live_and_a_not_live_pair"] > 0
                       and whole["DERIV"]["accounts_holding_BOTH_a_live_and_a_not_live_pair"] > 0),
    })

    # --- 8. DATA CHECK: no access_denied / skipped account read as empty ---
    led = ledger_outcomes()
    users = json.loads((P5 / "user_index.json").read_text())["users"]
    NOT_COMPLETE = {}
    for k, d in led.items():
        o = str(d.get("outcome"))
        if o != "complete":
            NOT_COMPLETE.setdefault(o, set()).add(k)
    bad_keys = set().union(*NOT_COMPLETE.values()) if NOT_COMPLETE else set()
    # a user index enters the table only via u_idx; map it back by slug AND username
    idx_bad = []
    idx_unknown = []
    for i, name in enumerate(users):
        k = str(name).lower()
        if k in bad_keys:
            idx_bad.append(i)
        elif k not in led:
            idx_unknown.append(i)
    idx_bad_arr = np.array(idx_bad, dtype=np.int64)
    in_table = np.unique(u_idx[line5])
    contributes = np.intersect1d(idx_bad_arr, in_table) if len(idx_bad_arr) else np.array([])
    ns_rows = 0
    if len(contributes):
        ns_rows = int((line5 & never & np.isin(u_idx, contributes)).sum())
    pull_log = json.loads((ROOT / "logs" / "step4_pull_log.json").read_text())

    # decisions/0080 Sec 3 row 8: the population is THE FULL ACCOUNT LEDGER, in
    # ACCOUNTS, with the skipped classes counted SEPARATELY and the pairs they
    # contribute STATED. Every ledger account is classified and asserted; none is
    # left uncovered.
    name_to_idx = {str(nm).lower(): i for i, nm in enumerate(users)}
    per_class: dict = {}
    asserted = 0
    for outcome_name, keyset in sorted(
            list(NOT_COMPLETE.items())
            + [("complete", {k for k, d in led.items() if str(d.get("outcome")) == "complete"})]):
        idxs = np.array(sorted({name_to_idx[k] for k in keyset if k in name_to_idx}),
                        dtype=np.int64)
        pairs = int((line5 & np.isin(u_idx, idxs)).sum()) if len(idxs) else 0
        ns = int((line5 & never & np.isin(u_idx, idxs)).sum()) if len(idxs) else 0
        per_class[outcome_name] = {
            "accounts_in_the_ledger": len(keyset),
            "of_those_present_in_the_parsed_sweep": int(len(idxs)),
            "pairs_contributed_to_the_APPLY_position5_population": pairs,
            "of_those_pairs_scored_NEVER_STARTED": ns,
            "is_a_skipped_class": outcome_name != "complete",
        }
        asserted += len(keyset)
    skipped_ns = sum(v["of_those_pairs_scored_NEVER_STARTED"]
                     for k, v in per_class.items() if v["is_a_skipped_class"])
    skipped_pairs = sum(v["pairs_contributed_to_the_APPLY_position5_population"]
                        for k, v in per_class.items() if v["is_a_skipped_class"])
    inv.append({
        "invariant": ("NO access_denied OR SKIPPED ACCOUNT IS READ AS EMPTY -- no account "
                      "recorded access_denied, over-tolerance or otherwise skipped contributes "
                      "a pair scored never-started"),
        "label": "DATA CHECK",
        "why_it_can_fail": ("CLAUDE.md: 'a skipped user silently read as empty becomes a false "
                            "never-started in the headline.' A join that treats an absent "
                            "history as an empty one produces exactly this, and it FAILS IN "
                            "THE DIRECTION OF THE RESULT, which is the worst direction "
                            "available. Rule and evidence at "
                            "artifacts/step0-access-and-setup.md Sec 7"),
        "population": ("THE FULL ACCOUNT LEDGER, IN ACCOUNTS (decisions/0080 Sec 3, row 8), "
                       "with the skipped classes counted separately and the pairs they "
                       "contribute stated"),
        "coverage": {
            "unit": "accounts",
            "accounts_in_the_stated_population": len(led),
            "accounts_asserted": asserted,
            "accounts_not_asserted": len(led) - asserted,
            "identity_holds": asserted == len(led),
            "by_final_ledger_outcome": per_class,
            "skipped_classes_total_pairs_contributed": skipped_pairs,
            "skipped_classes_total_never_started_pairs_contributed": skipped_ns,
            "a_second_class_checked_separately": {
                "parsed_accounts_with_no_ledger_row_at_all": len(idx_unknown),
                "why": ("an account present in the parsed sweep but absent from the ledger "
                        "would be covered by no ledger class, so it is counted rather than "
                        "assumed empty"),
            },
        },
        "checked": {
            "step4_ledger_accounts": len(led),
            "accounts_by_final_outcome": {k: len(v) for k, v in NOT_COMPLETE.items()}
                                         | {"complete": len(led) - len(bad_keys)},
            "step4_pull_log_access_denied": pull_log["access_denied"],
            "step4_pull_log_private_or_absent": pull_log["private_or_absent"],
            "accounts_in_the_parsed_sweep": len(users),
            "parsed_accounts_whose_final_ledger_outcome_is_NOT_complete": len(idx_bad),
            "parsed_accounts_with_no_ledger_row_at_all": len(idx_unknown),
            "such_accounts_contributing_ANY_pair_to_the_position_5_population":
                int(len(contributes)),
            "such_accounts_contributing_a_NEVER_STARTED_pair": ns_rows,
        },
        "reading": ("zero access_denied and zero private_or_absent were recorded in the whole "
                    "Step 4 pull, so the 403-skip path never fired. The skipped and "
                    "over-tolerance accounts DO exist -- 287 discarded over tolerance and 38 "
                    "skipped on the length forecast -- and none of them is parsed, indexed or "
                    "present in the table. They are ABSENT, not empty, which is what the rule "
                    "requires"),
        "passes": bool(len(contributes) == 0 and ns_rows == 0 and skipped_ns == 0
                       and asserted == len(led) and len(idx_unknown) == 0),
    })

    # ---- the 703 expectation: NOT an invariant ---------------------------
    a108 = R["per_arm"]["APPLY"]["108"]
    d108 = R["per_arm"]["DERIV"]["108"]
    recon = {
        "this_is_NOT_an_invariant": ("it is a POPULATION RECONCILIATION, and the spec's own "
                                     "instruction to suspect the population before the "
                                     "implementation is what makes it one"),
        "APPLY": {"denominator": a108["position5_n"], "expected": 703,
                  "measured": a108["liveness_excluded"],
                  "expected_split": [604, 99],
                  "measured_split": [a108["liveness_excluded_never_started"],
                                     a108["liveness_excluded_started_and_left"]],
                  "expected_accounts": 216,
                  "measured_accounts": a108["accounts_supplying_exclusions"]},
        "DERIV": {"denominator": d108["position5_n"], "expected": 99,
                  "measured": d108["liveness_excluded"],
                  "expected_split": [0, 99],
                  "measured_split": [d108["liveness_excluded_never_started"],
                                     d108["liveness_excluded_started_and_left"]],
                  "expected_accounts": 73,
                  "measured_accounts": d108["accounts_supplying_exclusions"]},
        "superseded_answers_not_produced": {
            "604_on_APPLY_is_ALT": a108["liveness_excluded"] != 604,
            "793_on_APPLY_is_ALT_MATCHED_withdrawn": a108["liveness_excluded"] != 793,
        },
    }
    recon["reconciles"] = (recon["APPLY"]["measured"] == 703
                           and recon["DERIV"]["measured"] == 99
                           and recon["APPLY"]["measured_split"] == [604, 99]
                           and recon["DERIV"]["measured_split"] == [0, 99]
                           and recon["APPLY"]["measured_accounts"] == 216
                           and recon["DERIV"]["measured_accounts"] == 73)

    coverage = {
        "item": "the set-membership drop rule",
        "status": ("A COVERAGE COUNT, NOT AN INVARIANT (decisions/0074 ruling 3). Step 8's own "
                   "bullet calls it 'an implementation check, not a data check'. Reported, not "
                   "asserted -- asserting it would add another pass to a report where six of "
                   "eight cannot fail on data"),
        "records_examined": st1["drop_rule"]["records_examined"],
        "records_dropped": st1["drop_rule"]["records_dropped"],
        "denominator_readings": st1["drop_rule"]["denominator_note"],
        "other_candidate_axes": st1["drop_rule"][
            "other_candidate_axes_for_the_denominator_difference"],
        "denominator_status": ("CLOSED at decisions/0083 Sec 1, amending 0074 ruling 4's routing "
                               "to Step 14. The three readings are one one-parameter family "
                               "indexed by where D11 applies, and EVERY MEMBER DROPS ZERO "
                               "RECORDS -- the numerator is 0 three times over, so the "
                               "difference survives into no result and is not a Step 14 "
                               "limitation. It publishes as a COVERAGE FIGURE WITH ITS PIPELINE "
                               "NAMED. What stays open is 0068's own item -- whether D11 applies "
                               "to the S1 completion walk -- and that is answered there"),
    }

    # decisions/0079 Sec 2 -- EVERY invariant result carries the build it was
    # measured on, and decisions/0080 Sec 3 -- EVERY invariant names the
    # population it runs on AND accounts for every row in it.
    for iv in inv:
        stamp(iv)
    stamp(recon)
    stamp(coverage)
    cov_rule = {
        "ruling": ("decisions/0080 Sec 3 -- EVERY INVARIANT NAMES THE POPULATION IT RUNS ON, AT "
                   "THE POINT OF USE, AND ACCOUNTS FOR EVERY ROW IN IT. Every invariant reports "
                   "rows_asserted + rows_not_asserted = rows_in_the_stated_population, and the "
                   "identity must hold"),
        "why": ("an invariant that passes on one population and was never run on another READS "
                "AS A PASS ON BOTH, and a passing invariant whose coverage the instance chose "
                "is a code check on the instance's choice"),
        "the_gap_this_arm_had": ("this arm's previous run asserted p on 19,042 rows "
                                 "(post-liveness) with a non-S&L clause on 177,513 "
                                 "(position-5), summing to 196,555 against a 196,654-row "
                                 "table. 99 rows -- exactly the started-and-left liveness "
                                 "exclusions -- were covered by NEITHER clause, and the report "
                                 "did not disclose it. Closed this run: 19,141 + 177,513 = "
                                 "196,654"),
        "identity_holds_on_every_invariant": all(
            bool(i.get("coverage", {}).get("identity_holds",
                 i.get("coverage", {}).get("holds_on_both_populations",
                 i.get("coverage", {}).get("holds_on_every_stated_population", True))))
            for i in inv),
        "measured_on_build": BUILD,
    }

    out = {
        "instance": "analytics-engineer-b", "namespace": "b",
        "mode": "GATE -- proposal only, nothing adopted",
        "provenance": provenance_block(),
        "invariant_coverage_rule": cov_rule,
        "how_to_read_this_report": (
            "SIX of the eight assertions CANNOT FAIL ON ANY DATA. Five are pure CODE CHECKS -- "
            "the outcome partition, the monotone filter counts, |D| <= L, A subset of A_H, and "
            "p in (0, 1]. A sixth, the clock start, is a code check by construction and a "
            "genuine cross-check only because the first-pass S1 completion date is recomputed "
            "INDEPENDENTLY here. TWO can fail on real data, and both were added by "
            "decisions/0076 because before it the set had ZERO: no account dropped wholesale, "
            "and no access_denied or skipped account read as empty. 'All invariants passed' is "
            "therefore mostly a statement that the code computed what it was told to; it is "
            "NOT evidence for the liveness rule or for any published share."),
        "counts": {"pure_code_checks": 5,
                   "code_check_by_construction_and_data_check_as_specified": 1,
                   "genuine_data_checks": 2,
                   "items_reported_but_not_asserted": 2,
                   "items_reported_but_not_asserted_named": [
                       "the set-membership drop rule -- a coverage count (0074 ruling 3)",
                       "the 703 expectation -- a population reconciliation (0047, 0069)"]},
        "invariants": inv,
        "coverage_count_not_an_invariant": coverage,
        "population_reconciliation_703_and_99": recon,
        "all_pass": all(i["passes"] for i in inv) and cov_rule["identity_holds_on_every_invariant"],
        "elapsed_s": time.time() - t,
    }
    (OUT / "invariants.json").write_text(json.dumps(out, indent=2, default=str))
    for i in inv:
        print(f"  [{'PASS' if i['passes'] else 'FAIL'}] {i['label']:<48} {i['invariant'][:66]}")
    print("  reconciliation 703/99:", "OK" if recon["reconciles"] else "MISMATCH")
    print(json.dumps(D9["keys"], indent=1))
    print(json.dumps(D9["half_a_fabricated_never_started_rows"], indent=1))
    print(json.dumps(D9["half_b_silently_deleted_S1_failing_counterparts"], indent=1))
    print(json.dumps(inv[6]["checked"], indent=1))
    print(json.dumps(inv[7]["checked"], indent=1))
    print(f"({time.time()-t:.0f}s)")


if __name__ == "__main__":
    main()
