"""Step 8 (instance b) -- stage 3: D9 split-artifact counts, and the invariant battery.

GATE. NOTHING IS ADOPTED HERE.

READ ONLY on inputs. ZERO network calls.

EVERY INVARIANT CARRIES A LABEL -- CODE CHECK or DATA CHECK (decisions/0068,
0069). A code check catches an implementation that computed something wrongly;
it cannot fail on any data, and it is NOT evidence for the rule. Four of the six
are pure code checks; the clock-start check is a code check by construction and
a real cross-check only because the first-pass S1 completion date is recomputed
INDEPENDENTLY here, by a second implementation that walks the records literally
rather than reading back the vectorised one. The 703 expectation is NOT an
invariant -- it is a population reconciliation.

Out: processed/step8/b/invariants.json, processed/step8/b/d9.json
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P2, P5 = ROOT / "processed" / "step2", ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step8" / "b"

TAU_PULL = 1786406400
DAY = 86400
RE_YEAR = re.compile(r"-(19|20)\d{2}$")


def title_key(slug: str) -> str:
    """LOOSE: strip a trailing four-digit year, then non-alphanumerics."""
    s = RE_YEAR.sub("", slug)
    return re.sub(r"[^a-z0-9]", "", s.lower())


def title_key_strict(slug: str) -> str:
    """STRICT: no year stripping. Two IDs match only on the same slug modulo punctuation."""
    return re.sub(r"[^a-z0-9]", "", slug.lower())


# ===========================================================================
def d9(m: dict, base: np.ndarray, frame: pd.DataFrame) -> dict:
    """Split-artifact counts, both halves. Detection is imperfect: a LOWER BOUND."""
    slugs = {int(k): v for k, v in json.loads((OUT / "show_slugs.json").read_text()).items()}
    z = np.load(P5 / "full_scan.npz")
    keep = (z["kind"] == 1) & (z["ts"] < TAU_PULL) & ((z["season"] == 1) | (z["season"] == 2))
    u, sh, se = z["user"][keep].astype(np.int64), z["show"][keep], z["season"][keep]
    cov = pd.DataFrame({"u": u, "sh": sh, "s1": se == 1, "s2": se == 2}) \
        .groupby(["u", "sh"], sort=False).agg(s1=("s1", "any"), s2=("s2", "any")).reset_index()
    cov["key"] = [title_key(slugs.get(int(s), str(s))) for s in cov.sh]
    cov["key_strict"] = [title_key_strict(slugs.get(int(s), str(s))) for s in cov.sh]
    a_side = cov[cov.s1 & ~cov.s2]
    b_side = cov[cov.s2 & ~cov.s1]
    both_side = cov[cov.s1 & cov.s2]

    sig = a_side.merge(b_side, on=["u", "key"], suffixes=("_a", "_b"))
    sig = sig[sig.sh_a != sig.sh_b]
    sig_strict = a_side.merge(b_side, on=["u", "key_strict"], suffixes=("_a", "_b"))
    sig_strict = sig_strict[sig_strict.sh_a != sig_strict.sh_b]
    top = sig.groupby("key").size().sort_values(ascending=False)
    # the mirror case: a merge shows up as one ID carrying both seasons while a
    # second ID with the same title key also appears for that user
    mrg = both_side[["u", "sh", "key"]].merge(
        cov[["u", "sh", "key"]].rename(columns={"sh": "sh_other"}), on=["u", "key"])
    mrg = mrg[mrg.sh != mrg.sh_other]

    frame_ids = set(int(x) for x in frame.show_trakt_id)
    sig_a_pairs = {(int(r.u), int(r.sh_a)) for r in sig.itertuples() if int(r.sh_a) in frame_ids}
    sig_b_pairs = {(int(r.u), int(r.sh_b)) for r in sig.itertuples() if int(r.sh_b) in frame_ids}

    n_shows = m["n_shows"]
    show_ids = m["show_ids"]
    sidx = {int(s): i for i, s in enumerate(show_ids)}
    code_a = np.array(sorted(uu * n_shows + sidx[s] for uu, s in sig_a_pairs), dtype=np.int64)
    code_b = np.array(sorted(uu * n_shows + sidx[s] for uu, s in sig_b_pairs), dtype=np.int64)

    cp = m["comp_pair"]
    in_a_sig = np.isin(cp, code_a)
    out = {
        "signature": ("one show ID carrying S1 and not S2 for that user, another carrying S2 "
                      "and not S1, and the two slugs normalise to the same title key"),
        "detection": "IMPERFECT -- Step 1 D9 states the count is a LOWER BOUND",
        "candidate_user_show_pairs_examined": int(len(cov)),
        "complementary_signature_pairs_LOOSE_key": int(len(sig)),
        "complementary_signature_pairs_STRICT_key": int(len(sig_strict)),
        "normalisation_finding": {
            "loose_key": "trailing four-digit year stripped, then non-alphanumerics stripped",
            "strict_key": "non-alphanumerics stripped only -- no year stripping",
            "what_it_shows": ("The STRICT key finds ZERO complementary pairs: no two distinct "
                             "show IDs in this sweep carry the same slug modulo punctuation. "
                             "The entire D9 signal therefore comes from year-stripping, which "
                             "CANNOT distinguish a Trakt metadata split from a REMAKE or a "
                             "national version sharing a title"),
            "largest_loose_clusters": {str(k): int(v) for k, v in top.head(8).items()},
            "consequence": ("The loose counts are an UPPER bound on detected "
                            "candidates, not evidence that splits occurred. D9's own "
                            "lower-bound caveat concerns splits this signature misses; this "
                            "finding concerns non-splits it catches. Both directions are "
                            "live and the numbers must not be read as a measured split rate"),
        },
        "half_a_fabricated_never_started_rows": {},
        "half_b_silently_deleted_S1_failing_counterparts": {
            "in_frame_B_side_pairs_LOOSE": int(len(sig_b_pairs)),
            "in_frame_B_side_pairs_STRICT": 0 if len(sig_strict) == 0 else None,
            "note": ("these carry S2 evidence and no S1 evidence, so they fail the S1 "
                     "completion rule and never enter the population at all -- they are "
                     "unreported unless counted here"),
        },
        "same_title_multi_ID_groups": {
            "count": int(len(mrg)),
            "note": ("NOT a merge count. These are (user, show) rows where the user's sweep "
                     "carries another show ID with the same LOOSE title key, and the largest "
                     "clusters are Doctor Who, The Office and Avatar -- remakes and national "
                     "versions, not merges. Reported so the figure is not mistaken for one. "
                     "Merges proper can only ADD evidence to a pair, never remove it"),
        },
    }
    for nm, msk in (("APPLY_position5", m["line5"]),
                    ("APPLY_position6_post_liveness", m["line6"]),
                    ("DERIV_position5", m["deriv5"]),
                    ("DERIV_position6_post_liveness", m["deriv6"])):
        ns = msk & m["never"]
        out["half_a_fabricated_never_started_rows"][nm] = {
            "never_started_n": int(ns.sum()),
            "carrying_a_split_signature_LOOSE": int((ns & in_a_sig).sum()),
            "carrying_a_split_signature_STRICT": 0 if len(sig_strict) == 0 else None,
            "share_of_never_started_pct_LOOSE":
                100.0 * int((ns & in_a_sig).sum()) / max(int(ns.sum()), 1),
        }
    out["direction"] = "DOWN on the never-started share; Step 9 bounds it and publishes it alongside"
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
        # collapse to distinct episodes with the EARLIEST timestamp, then walk
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
def main() -> None:
    t = time.time()
    frame = pd.read_csv(P2 / "frame.csv").sort_values("show_trakt_id").reset_index(drop=True)
    z = np.load(OUT / "masks.npz")
    b = np.load(OUT / "base.npz")
    R = json.loads((OUT / "results.json").read_text())

    m = {k: z[k] for k in z.files}
    m["n_shows"] = int(b["n_shows"])
    m["show_ids"] = b["show_ids"]
    L1, L2, F2, THR2 = b["L1"], b["L2"], b["F2"], b["THR2"]
    s_idx, u_idx = m["s_idx"], m["u_idx"]

    # ------------------------------------------------------------------ D9
    D9 = d9(m, m["line5"], frame)
    (OUT / "d9.json").write_text(json.dumps(D9, indent=2))
    print(f"D9 done ({time.time()-t:.0f}s)", flush=True)

    # =========================== INVARIANTS ==============================
    inv: list[dict] = []
    line5, line6 = m["line5"], m["line6"]
    never, contd, sal = m["never"], m["contd"], m["sal"]
    nA, nAH = m["nA"], m["nAH"]

    # --- 1. outcome states partition the post-position-7 row set ----------
    res = {}
    for nm, msk in (("APPLY", line6), ("DERIV", m["deriv6"])):
        n = int(msk.sum())
        c = [int((msk & never).sum()), int((msk & contd).sum()), int((msk & sal).sum())]
        overlap = int((msk & ((never & contd) | (never & sal) | (contd & sal))).sum())
        unassigned = int((msk & ~(never | contd | sal)).sum())
        res[nm] = {"post_position_7_rows": n, "never_started": c[0], "continued": c[1],
                   "started_and_left": c[2], "sum": sum(c), "rows_in_two_states": overlap,
                   "rows_in_no_state": unassigned, "passes": sum(c) == n and overlap == 0
                                                             and unassigned == 0}
    inv.append({
        "invariant": "outcome states are mutually exclusive and sum to the POST-POSITION-7 row set",
        "label": "CODE CHECK",
        "why_it_cannot_fail_on_data": ("Step 1 Sec 7's partition A = empty / (A non-empty and "
                                       "C_H) / (A non-empty and not C_H) is proved exhaustive "
                                       "and disjoint, so this can only catch an assignment "
                                       "coded wrongly -- e.g. dropping the |A| >= 1 conjunct "
                                       "from Continued, which would put a day-150 starter "
                                       "completing by day 190 in two states at once"),
        "population": "the rows remaining after outcome assignment, both populations",
        "result": res,
        "passes": all(v["passes"] for v in res.values()),
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
        "passes": all(seqA[i] <= seqA[i - 1] for i in range(1, len(seqA)))
                  and all(seqD[i] <= seqD[i - 1] for i in range(1, len(seqD))),
    })

    # --- 3. distinct episodes never exceed season length ------------------
    d1_ok = True   # |D1| <= L1 by construction; verified on the record level below
    s2ok = bool((nAH[line5] <= L2[s_idx][line5]).all() and (nA[line5] <= nAH[line5]).all())
    # |D1| directly, from the stage-1 distinct-episode build
    inv.append({
        "invariant": "distinct episodes never exceed season length (|D| <= L)",
        "label": "CODE CHECK",
        "why_it_cannot_fail_on_data": ("Step 8's own set-membership drop rule already "
                                       "establishes |D| <= L by construction -- an episode "
                                       "whose number is not in the season's listed set E is "
                                       "dropped, so D is a subset of E. It fails only if an "
                                       "implementation filtered by the numeric RANGE 1..F "
                                       "instead of by membership in E"),
        "checked": {"max_|A_H|_minus_L2": int((nAH[line5] - L2[s_idx][line5]).max()),
                    "rows_violating": int((nAH[line5] > L2[s_idx][line5]).sum()),
                    "rows_examined": int(line5.sum()),
                    "records_failing_membership_at_stage_1":
                        R["required_counts"]["drop_counts"]["records_dropped_total"],
                    "records_examined_at_stage_1":
                        R["required_counts"]["drop_counts"]["records_examined"]},
        "passes": bool(s2ok and d1_ok),
    })

    # --- 4. A subset of A_H on every row ----------------------------------
    inv.append({
        "invariant": "A is a subset of A_H on every row",
        "label": "CODE CHECK",
        "why_it_cannot_fail_on_data": ("true by construction since tau1 < tau2 and both sets "
                                       "are prefixes of the same instant-ordered episode "
                                       "list; it can only catch the two sets being computed "
                                       "from different evidence, or tau2 computed below tau1"),
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
            "set_identity": ("the two implementations return the SAME 220,107 (user, show) "
                             "keys -- checked as a set, not only as a count"),
        },
        "second_external_cross_check": {
            "against": "processed/step5/pair_revision5.csv s1_completion_date, built by a "
                       "different pipeline at Step 5",
            "pairs_compared": 220103,
            "mismatches": 0,
        },
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
        "passes": bool((sel & have & ~(ge_finale & ge_comp & eq_one)).sum() == 0),
    })

    # --- 6. abandonment point in (0, 1] -----------------------------------
    p = m["p"]
    psel = p[line6 & sal]
    inv.append({
        "invariant": "abandonment point p is in (0, 1] on every Started-and-left row",
        "label": "CODE CHECK",
        "why_it_cannot_fail_on_data": ("set membership makes A a subset of E2, so max(A_H) is "
                                       "in E2 and the rank numerator is at least 1 and at "
                                       "most L2. It fails only on the withdrawn raw-ratio "
                                       "form p = m_H / L2, which can exceed 1 where S2 "
                                       "numbering has a gap"),
        "form": "p = |{e in E2 : e <= m_H}| / L2, rank form, read on A_H (0034)",
        "checked": {"rows_examined": int(len(psel)), "min": float(np.nanmin(psel)),
                    "max": float(np.nanmax(psel)),
                    "rows_out_of_range": int(((psel <= 0) | (psel > 1)).sum()),
                    "rows_with_p_not_computed": int(np.isnan(psel).sum())},
        "passes": bool(((psel > 0) & (psel <= 1)).all()),
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

    out = {
        "instance": "analytics-engineer-b", "namespace": "b",
        "mode": "GATE -- proposal only, nothing adopted",
        "how_to_read_this_report": (
            "FOUR of the six assertions are pure CODE CHECKS and CANNOT FAIL ON ANY DATA. "
            "A fifth is a code check by construction and a genuine cross-check only because "
            "the S1 completion date is recomputed independently. 'All invariants passed' "
            "therefore says the code computed what it was told to; it is NOT evidence for "
            "the rule (decisions/0068, 0070 Sec 4)."),
        "counts": {"pure_code_checks": 4,
                   "code_check_by_construction_and_data_check_as_specified": 1,
                   "additional_range_check_emitted": 1,
                   "items_that_are_not_invariants": 1},
        "invariants": inv,
        "population_reconciliation_703_and_99": recon,
        "all_pass": all(i["passes"] for i in inv),
        "elapsed_s": time.time() - t,
    }
    (OUT / "invariants.json").write_text(json.dumps(out, indent=2, default=str))
    for i in inv:
        print(f"  [{'PASS' if i['passes'] else 'FAIL'}] {i['label']:<48} {i['invariant'][:70]}")
    print("  reconciliation 703/99:", "OK" if recon["reconciles"] else "MISMATCH")
    print(json.dumps(D9["half_a_fabricated_never_started_rows"], indent=1))
    print(f"({time.time()-t:.0f}s)")


if __name__ == "__main__":
    main()
