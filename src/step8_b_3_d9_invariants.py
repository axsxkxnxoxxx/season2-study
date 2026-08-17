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


def _tie_report(ranked: list[tuple[str, int]]) -> dict:
    """decisions/0088 Sec 3 rules the RANKING BASIS. It does not rule the
    TIE-BREAK, and on this data the tie is occupied at the third place, so which
    name is published third is decided by a rule no surface states."""
    if len(ranked) < 3:
        return {"third_place_count": None, "keys_tied_at_it": 0,
                "coverage": "fewer than three keys; nothing to tie"}
    third = ranked[2][1]
    tied = sorted(k for k, n in ranked if n == third)
    return {
        "third_place_count": int(third),
        "keys_tied_at_the_third_place_count": len(tied),
        "tied_keys": tied[:12],
        "this_arms_tie_break": "ascending key, applied after descending count",
        "this_arms_third_name": ranked[2][0],
        "REPORTED_NOT_RECONCILED": (
            "decisions/0088 Sec 3 names the U1 top three as secondchance (8), theisland (7), "
            "maigret (6). The first two are unique at their counts and reproduce exactly. The "
            "THIRD is inside a tie, and 0088 rules the BASIS but not the TIE-BREAK -- so the "
            "third name is decided by a rule no surface states. Under ascending-key this arm "
            f"publishes `{ranked[2][0]}`; `maigret` is one of the tied keys and is equally "
            "correct under a different tie-break. This is a spec gap in the ruling that closed "
            "the previous spec gap, and it is reported rather than resolved by picking the "
            "name that matches the entry"),
    }


def k_third(slug: str) -> str:
    """NOT A KEY OF THIS STUDY. A trailing digit group of ARBITRARY length --
    it reduces `the-100` to `the`. Measured only to show what it costs."""
    return k_strict(RE_ANYDIGITS.sub("", slug))


# ===========================================================================
def d9(m: dict, frame: pd.DataFrame, st1: dict) -> dict:
    """Split-artifact counts, both halves. Detection is imperfect: a LOWER BOUND."""
    slugs = {int(k): v for k, v in json.loads((OUT / "show_slugs.json").read_text()).items()}
    z = np.load(P5 / "full_scan.npz")
    _s12 = (z["kind"] == 1) & ((z["season"] == 1) | (z["season"] == 2))
    keep = _s12 & (z["ts"] < TAU_PULL)
    # decisions/0088 Sec 1(b) -- D9's coverage rows are a named D11 SITE and the
    # count belongs at the site, not once and about the rest.
    d11_site = {
        "site": "D9 coverage rows",
        "d11_applied": True,
        "unit": "S1/S2 episode records, ALL shows in the sweep, not only frame shows",
        "records_in_the_sites_input_universe": int(_s12.sum()),
        "records_excluded_by_D11": int((_s12 & ~keep).sum()),
        "records_used": int(keep.sum()),
        "assertion": "no record dated at or after tau_pull participates in the D9 coverage pivot",
        "assertion_holds": bool(int(z["ts"][keep].max()) < TAU_PULL),
        "latest_watched_at_used_utc": str(np.datetime64(int(z["ts"][keep].max()), "s")),
        "note": ("the universe here is WIDER than the in-frame S1/S2 slice the waterfall uses, "
                 "because a split puts S1 under one show ID and S2 under another and only one "
                 "of the two need be in the frame"),
    }
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

    # ---- B1 (decisions/0085 Sec 2): NAME THE UNIVERSE THE CLUSTERING RUNS
    # OVER, AT THE POINT OF USE.  The two arms published DISJOINT cluster lists
    # on IDENTICAL counts -- no shared member, maxima 8 against 10 -- while
    # every count around them reconciled. That is not a counting difference: it
    # is a difference in WHICH SET OF SHOWS IS BEING CLUSTERED, and the spec
    # never said which.  The cluster examples are the EVIDENCE for the loose
    # key's only warrant (that it bounds how wrong strict could be), so two arms
    # giving different evidence for one warrant makes the warrant irreproducible
    # while the deliverables read otherwise.
    #
    # THE DIVERGENCE IS REPORTED, NOT RECONCILED. No universe is ruled. So all
    # THREE candidate universes the ruling names are measured here and each is
    # labelled, and the one this instance PUBLISHES as its headline list is
    # named explicitly rather than left to be inferred from a number.
    top = sig_loose.groupby("k_loose").size().sort_values(ascending=False)

    def cluster_over_show_ids(ids: list[int]) -> dict:
        """Cluster DISTINCT SHOW IDs by the loose key.

        TWO ranking bases, and decisions/0088 Sec 3 rules WHICH: DISTINCT STRICT
        KEYS MERGED -- how many separate metadata entries the loose key collapsed
        into one. It was unstated and it REORDERS THE LIST ON ITS OWN: the same
        universe under the same key, ranked by distinct show IDs instead,
        displaces `maigret` with `blackout`. Both are emitted, the ruled basis is
        named, and neither is left to be inferred from a number.
        """
        by: dict[str, set[int]] = {}
        bystrict: dict[str, set[str]] = {}
        for sid in ids:
            s = slugs.get(int(sid), str(sid))
            lk = k_loose(s)
            by.setdefault(lk, set()).add(int(sid))
            bystrict.setdefault(lk, set()).add(k_strict(s))
        rank_strict = sorted(((k, len(bystrict[k])) for k in by), key=lambda kv: (-kv[1], kv[0]))
        rank_ids = sorted(((k, len(v)) for k, v in by.items()), key=lambda kv: (-kv[1], kv[0]))
        return {
            "unit": "distinct show IDs sharing one LOOSE key",
            "RANK_BASIS_RULED": ("DISTINCT STRICT KEYS MERGED (decisions/0088 Sec 3) -- how "
                                 "many separate metadata entries the loose key collapsed into "
                                 "one. Named at the point of use; a list without it is not "
                                 "reproducible"),
            "members_examined": len(ids),
            "distinct_loose_keys": len(by),
            "keys_merging_two_or_more_show_ids": sum(1 for _, n in rank_ids if n > 1),
            "keys_merging_two_or_more_STRICT_keys": sum(1 for _, n in rank_strict if n > 1),
            "largest_clusters": {k: n for k, n in rank_strict[:8]},
            "max_cluster_size": rank_strict[0][1] if rank_strict else 0,
            # 0088 Sec 3 rules the BASIS. It does not rule the TIE-BREAK, and the
            # tie is occupied: several keys share the third-place count, so which
            # name appears third depends on an unspecified rule. Reported.
            "THE_TIE_BREAK_IS_NOT_RULED": _tie_report(rank_strict),
            "ALTERNATE_BASIS_ranked_by_distinct_show_IDs": {
                "largest_clusters": {k: n for k, n in rank_ids[:8]},
                "max_cluster_size": rank_ids[0][1] if rank_ids else 0,
                "why_emitted": ("0088 Sec 3 records that the basis reorders the list on its "
                                "own. Emitting both is what lets a reader see that the "
                                "reordering is the basis and not a counting difference"),
            },
            "the_two_bases_agree_on_the_top_key":
                bool(rank_strict and rank_ids and rank_strict[0][0] == rank_ids[0][0]),
        }

    slugged_ids = sorted(slugs)
    frame_ids_sorted = sorted(frame_ids)
    clustering = {
        "ruling": ("decisions/0088 Sec 3 -- THE D9 CLUSTERING UNIVERSE IS U1, ALL SLUGGED SWEEP "
                   "SHOW IDs, RANKED BY DISTINCT STRICT KEYS MERGED. It closes the gap "
                   "0085 Sec 2 (Red Team B1) opened and 0086 Sec 1 located: the two arms "
                   "published DISJOINT cluster lists on IDENTICAL counts, sharing no member, "
                   "with maxima 8 against 10, while every count around them reconciled -- a "
                   "difference in WHICH SET OF SHOWS IS CLUSTERED, which the spec never said"),
        "status": ("RULED. 0085 left it REPORTED-NOT-RECONCILED and 0088 Sec 3 rules it: BOTH "
                   "ARMS CLUSTER THE SAME OBJECT. All three candidate universes are still "
                   "measured and labelled here, so an arm on another universe stays diffable "
                   "without a rerun, but the PUBLISHED list is U1"),
        "PUBLISHED_UNIVERSE": "U1_all_sweep_show_ids_carrying_a_slug",
        "CHANGED_FROM_THIS_ARMS_PREVIOUS_BUILD": (
            "the r3 build published U3, the D9 candidate complementary pairs, on the "
            "ground that the loose key's warrant concerns exactly the pairs the two keys "
            "disagree about. 0088 Sec 3 rules otherwise and gives the reason: the artifact D9 "
            "hunts is a history splitting across two metadata entries, and THAT CAN OCCUR "
            "ANYWHERE IN A HISTORY, not only among shows that survived the frame filters -- a "
            "narrow universe finds only splits where both sides made the cut, and a bound "
            "computed on a narrow slice bounds very little. NO COUNT MOVES WITH IT: the "
            "strict and loose complementary-pair counts are unchanged, because D9's SEARCH "
            "already ran on the whole sweep in this arm. What moves is which clusters are "
            "ILLUSTRATED"),
        "why_that_one": ("0088 Sec 3's ground, not this instance's: the split can occur "
                         "anywhere in a history, so a frame-restricted universe finds only the "
                         "narrowest case. task-sheet.md's former illustration -- The Twilight "
                         "Zone, The Traitors, Manhunt -- was U3 and is SUPERSEDED as the "
                         "example. Those three names are not wrong; they are another "
                         "universe's answer, which is why it needed ruling"),
        "universes": {
            "U1_all_sweep_show_ids_carrying_a_slug": dict(
                cluster_over_show_ids(slugged_ids),
                definition=("every show ID appearing anywhere in the Step 4 parsed sweep that "
                            "carries a slug -- processed/step8/b/show_slugs.json"),
            ),
            "U2_the_frame_shows": dict(
                cluster_over_show_ids(frame_ids_sorted),
                definition="the Step 2 frame shows only",
            ),
            "U3_D9_candidate_complementary_pairs": {
                "status": ("NOT THE PUBLISHED UNIVERSE (decisions/0088 Sec 3). It is the "
                           "narrowest of the three and it is what task-sheet.md's former "
                           "illustration was measured over"),
                "unit": ("complementary signature ROWS (user, S1-side show, S2-side show) "
                         "sharing one LOOSE key -- NOT distinct show IDs"),
                "rank_basis": ("complementary signature rows per loose key. NOT the ruled "
                               "basis, which is distinct strict keys merged and applies to the "
                               "show-ID universes"),
                "definition": ("the complementary signature pairs the LOOSE key finds: one "
                               "show ID carrying S1 and not S2 for that user, another "
                               "carrying S2 and not S1, both normalising to the same loose "
                               "key. This is the set STRICT and LOOSE disagree about"),
                "members_examined": int(len(sig_loose)),
                "distinct_loose_keys": int(sig_loose.k_loose.nunique()),
                "largest_clusters": {str(k): int(v) for k, v in top.head(8).items()},
                "max_cluster_size": int(top.iloc[0]) if len(top) else 0,
            },
        },
        "coverage": ("three universes measured, none of them an empty look: "
                     f"{len(slugged_ids):,} slugged sweep show IDs, {len(frame_ids_sorted):,} "
                     f"frame shows, {len(sig_loose):,} candidate complementary pairs"),
        "WHAT_NAMING_THE_UNIVERSE_LOCATES": {
            "finding": ("BOTH cluster lists decisions/0085 Sec 2 quotes are reproduced by THIS "
                        "SINGLE BUILD, from two different universes. U1 (all slugged sweep "
                        "show IDs), on the RULED basis of distinct strict keys merged, gives "
                        "secondchance 8 and theisland 7 -- both unique at their counts -- with "
                        "a maximum of 8, and a SIX-WAY TIE at 6 that contains maigret; U3 (the "
                        "D9 candidate complementary pairs) gives thetwilightzone 10, "
                        "thetraitors 7, manhunt 5 with a maximum of 10. Those are the two "
                        "quoted lists and the two quoted maxima, with the one qualification "
                        "that 0088's third U1 name sits inside a tie the ruling does not break "
                        "-- see THE_TIE_BREAK_IS_NOT_RULED"),
            "what_it_means": ("the divergence was located ON THE UNIVERSE AXIS and not in the "
                              "counting -- consistent with 0085's own observation that every "
                              "count around the lists reconciled. Neither arm miscounted, and "
                              "0088 Sec 3 then ruled the universe so both arms cluster one "
                              "defined object"),
            "and_the_basis_matters_too": ("0088 Sec 3 also rules the RANKING BASIS, because it "
                                          "reorders the list on its own: U1 ranked by distinct "
                                          "SHOW IDS instead of distinct STRICT KEYS displaces "
                                          "maigret with blackout. Both rankings are emitted "
                                          "under each show-ID universe"),
            "quoted_lists_source": ("decisions/0085 Sec 2, 0088 Sec 3 and task-sheet.md Step 8's "
                                    "D9 bullet -- spec surfaces this instance is required to "
                                    "read. No other arm's output folder was read"),
            "reproduced_U1_max": None,      # filled below, measured not typed
            "reproduced_U3_max": None,
        },
        "note_the_unit_differs_between_universes": (
            "U1 and U2 count DISTINCT SHOW IDS per key; U3 counts complementary signature "
            "ROWS per key. A cluster size from one is not comparable to a cluster size from "
            "another, which is a second reason the universe has to be named rather than the "
            "number quoted"),
    }
    _w = clustering["WHAT_NAMING_THE_UNIVERSE_LOCATES"]
    _w["reproduced_U1_max"] = clustering["universes"][
        "U1_all_sweep_show_ids_carrying_a_slug"]["max_cluster_size"]
    _w["reproduced_U3_max"] = clustering["universes"][
        "U3_D9_candidate_complementary_pairs"]["max_cluster_size"]

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

    # =====================================================================
    # decisions/0090 -- D9 PUBLISHES AS A BOUND. STRICT IS THE FLOOR, LOOSE IS
    # THE CEILING, BOTH LABELLED, AND NEITHER IS THE POINT ESTIMATE. This
    # SUPERSEDES 0074 ruling 5's framing ("use the strict key and report the
    # loose count alongside"), under which STRICT WAS THE ANSWER and loose was
    # context. Direction is part of the label and it is not symmetric: strict
    # matches only slugs identical modulo punctuation so it CANNOT OVER-COUNT;
    # loose strips a trailing year and MERGES GENUINELY DIFFERENT SHOWS, so it
    # cannot under-count. The bound applies to EVERY D9 quantity with both
    # forms, because applying it to one and not the others is the defect
    # 0078 Sec 3 corrected.
    # =====================================================================
    def _bound(name: str, floor: int, ceiling: int, unit: str, coverage: dict) -> dict:
        return {
            "quantity": name,
            "unit": unit,
            "BOUND": [int(floor), int(ceiling)],
            "floor_STRICT": int(floor),
            "ceiling_LOOSE": int(ceiling),
            "width": int(ceiling) - int(floor),
            "point_estimate": None,
            "point_estimate_note": ("NONE. decisions/0090 -- neither endpoint may be quoted as "
                                    "D9's result. The interval is the result"),
            "direction": ("STRICT is the FLOOR: it matches only slugs identical modulo "
                          "punctuation, so it cannot over-count. LOOSE is the CEILING: "
                          "year-stripping merges remakes and national versions, so it cannot "
                          "under-count. The error runs OPPOSITE to D9's own lower-bound caveat"),
            "COVERAGE_BESIDE_THE_FLOOR": coverage,
            "why_the_coverage_is_here": ("decisions/0090 -- a zero floor is not an absence of "
                                         "evidence. 0 is a MEASURED floor on a stated coverage, "
                                         "and a bound whose floor is 0 with the coverage unstated "
                                         "is indistinguishable from a check that looked nowhere"),
        }

    _cov_common = {
        "candidate_user_show_pairs_examined": int(len(cov)),
        "distinct_show_ids_appearing_in_a_coverage_row": int(cov.sh.nunique()),
        "S1_not_S2_pairs": int(len(a_side)),
        "S2_not_S1_pairs": int(len(b_side)),
        "records_used_after_D11": int(d11_site["records_used"]),
        "universe": ("the WHOLE PULLED SWEEP, not the frame -- a split puts S1 under one show "
                     "ID and S2 under another and only one of the two need be in the frame"),
    }

    out = {
        "signature": ("one show ID carrying S1 and not S2 for that user, another carrying S2 "
                      "and not S1, and the two slugs normalise to the same title key"),
        "detection": "IMPERFECT -- Step 1 D9 states the count is a LOWER BOUND",
        "PUBLICATION_FORM_decisions_0090": {
            "ruling": ("D9 PUBLISHES AS A BOUND. STRICT IS THE FLOOR, LOOSE IS THE CEILING, both "
                       "labelled, and NEITHER IS THE POINT ESTIMATE. Neither endpoint may be "
                       "quoted as 'D9's result'"),
            "supersedes": ("decisions/0074 ruling 5's framing, 'USE THE STRICT KEY AND REPORT "
                           "THE LOOSE COUNT ALONGSIDE', under which STRICT WAS THE ANSWER and "
                           "loose was context. The keys themselves are unchanged (0076 Sec 3)"),
            "ground": ("0074 ruling 5's own reason carried through: the loose count publishes "
                       "BECAUSE IT BOUNDS HOW WRONG STRICT COULD BE, and a quantity published to "
                       "bound another is an ENDPOINT, not a footnote. 0078 Sec 3 already ran "
                       "this argument once, to extend loose to half (b)"),
            "applies_to_every_quantity_with_both_forms": (
                "complementary signature pairs, half (a) and half (b) -- applying it to one and "
                "not the others is the defect 0078 Sec 3 corrected"),
            "THE_THIRD_KEY_IS_NOT_AN_ENDPOINT": (
                "a trailing digit group of arbitrary length reduces `the-100` to `the`. Its "
                "count is a DIFFERENT KEY'S ANSWER, reported as a divergence and never as the "
                "ceiling (0090, 0076, 0078 Sec 3)"),
            "NO_COUNT_MOVES_WITH_THIS_RULING": ("0090 Sec 4 -- D9's own numbers do not change. "
                                                "What changes is which of them is presented as "
                                                "the answer, and this arm's r4 build presented "
                                                "strict as the ruled key"),
            "bounds": {
                "complementary_signature_pairs": _bound(
                    "complementary signature pairs", len(sig_strict), len(sig_loose),
                    "(user, S1-side show, S2-side show) complementary signature rows",
                    dict(_cov_common)),
            },
        },
        "ruled_key": ("BOTH -- decisions/0090 publishes D9 as the BOUND [STRICT, LOOSE]. "
                      "SUPERSEDED: 'STRICT (decisions/0074 ruling 5), with the LOOSE count "
                      "reported alongside', under which strict was the answer"),
        "candidate_user_show_pairs_examined": int(len(cov)),
        "sides": {"A_side_S1_not_S2": int(len(a_side)), "B_side_S2_not_S1": int(len(b_side)),
                  "both_seasons": int(len(both_side))},
        # decisions/0088 Sec 2(b) -- NAME WHAT EACH COVERAGE FIGURE COUNTS, AT THE
        # POINT OF USE. 747,478 and 726,103 are DIFFERENT OBJECTS and both correct:
        # a user-show carrying two seasons contributes TWO ROWS AND ONE PAIR.
        # Reconciling them would collapse two real quantities into one.
        "COVERAGE_QUANTITIES_EACH_NAMED": {
            "ruling": ("decisions/0088 Sec 2 -- one name over two quantities is not a "
                       "divergence, and reconciling would collapse two real objects into one. "
                       "Each quantity below states what it counts and over what"),
            "THIS_ARM_PUBLISHES_AS_ITS_HEADLINE": "distinct_candidate_user_show_PAIRS",
            "distinct_candidate_user_show_PAIRS": {
                "value": int(len(cov)),
                "counts": ("distinct (user, show) PAIRS carrying at least one S1 or S2 episode "
                           "record after D11, across the WHOLE SWEEP -- not the frame"),
                "decomposition": [int(len(a_side)), int(len(both_side)), int(len(b_side))],
                "decomposition_note": "S1-not-S2 + both + S2-not-S1, which sums to the value",
            },
            "undeduplicated_user_show_SEASON_COVERAGE_ROWS": {
                "value": int(len(a_side) + len(b_side) + 2 * len(both_side)),
                "counts": ("(user, show, season) rows over the same universe -- a user-show "
                           "carrying both seasons contributes TWO rows and ONE pair"),
                "why_emitted": ("0088 Sec 2(b) names this as a DIFFERENT OBJECT from the pair "
                                "count, both correct. It is measured here so this arm's own "
                                "value of the object exists and is not inferred from the "
                                "other's"),
                "NOT_COMPARABLE_WITHOUT_ITS_MASK": ("this value is over the D11-filtered S1/S2 "
                                                    "episode records only; a season-coverage "
                                                    "row count taken over all seasons, or "
                                                    "before D11, is a third object again"),
            },
            "distinct_show_IDs_APPEARING_IN_A_D9_COVERAGE_ROW": {
                "value": int(cov.sh.nunique()),
                "counts": ("show IDs that appear in at least one coverage row -- i.e. that some "
                           "user in the sweep has an S1 or S2 record on"),
                "IS_NOT_THE_SWEEP": ("decisions/0088 Sec 2(a) -- this quantity was published by "
                                     "one arm mislabelled `distinct_show_ids_in_the_sweep`. It "
                                     "is a pivot-side count and it is labelled here for what it "
                                     "is. This arm's slug map is a separate object and is "
                                     "reported next"),
            },
            "distinct_SLUGGED_SHOW_IDS_IN_THE_PARSED_SWEEP_the_U1_universe": {
                "value": int(len(slugs)),
                "counts": ("one row per show ID seen anywhere in processed/step4/parsed/ "
                           "carrying a `show_slug` field -- the U1 universe decisions/0088 "
                           "Sec 3 rules the clustering runs over"),
                "of_which_the_slug_string_is_empty":
                    int(sum(1 for v in slugs.values() if not str(v).strip())),
                "source_file": "processed/step8/b/show_slugs.json",
                "NAMED_AS_AN_OBJECT": ("0088 Sec 2(c) -- the two arms' slugged-ID sets stood 62 "
                                       "apart while both were called U1. A shared label over "
                                       "two sets is the defect; the sets themselves may both be "
                                       "right. This is THIS arm's set, with its construction "
                                       "named"),
            },
        },
        "D11_site": d11_site,
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
            "largest_loose_clusters": dict(
                clustering["universes"]["U1_all_sweep_show_ids_carrying_a_slug"][
                    "largest_clusters"]),
            "THE_UNIVERSE_THIS_LIST_IS_MEASURED_OVER": (
                "U1, ALL SLUGGED SWEEP SHOW IDS -- every distinct show ID appearing anywhere in "
                "the pulled sweep that carries a slug, deduplicated to one row per show ID. "
                "RANKED BY DISTINCT STRICT KEYS MERGED. Both are ruled by decisions/0088 Sec 3 "
                "and named here at the point of use; the two other candidate universes are "
                "measured alongside under clustering_universes"),
            "THE_LIST_THIS_REPLACES": (
                "the r3 build published U3's list -- thetwilightzone 10, thetraitors 7, "
                "manhunt 5 -- which is also task-sheet.md's former illustration. SUPERSEDED as "
                "the example by 0088 Sec 3. Those names are not wrong; they are another "
                "universe's answer, and both lists are still emitted side by side in the "
                "universe table"),
            "clustering_universes": clustering,
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
            # decisions/0090 -- the bound, not a point estimate, on this population
            "BOUND_decisions_0090": _bound(
                f"half (a) fabricated never-started rows, {nm}",
                int((ns & in_a_strict).sum()), int((ns & in_a_loose).sum()),
                "never-started rows carrying a split signature on the A side",
                {**_cov_common, "never_started_rows_examined": n,
                 "population": nm}),
            "BOUND_as_a_share_of_never_started_pct": [
                100.0 * int((ns & in_a_strict).sum()) / max(n, 1),
                100.0 * int((ns & in_a_loose).sum()) / max(n, 1)],
        }
    # decisions/0090 -- half (b) publishes as a bound too, on both of its
    # quantities. 0078 Sec 3 already extended the loose count to this half; 0090
    # makes the pair an interval rather than an answer plus a footnote.
    hb["BOUND_decisions_0090"] = {
        "B_side_pairs_in_frame": _bound(
            "half (b) B-side pairs in frame",
            hb["STRICT"]["B_side_pairs_in_frame"], hb["LOOSE"]["B_side_pairs_in_frame"],
            "(user, show) pairs on the S2-not-S1 side of a complementary signature, in frame",
            {**_cov_common,
             "position3_drop_set_pairs": hb["position3_drop_set_pairs"],
             "of_which_carry_S2_and_no_S1": hb["of_which_carry_S2_evidence_and_NO_S1_evidence"]}),
        "present_in_the_retained_position3_drop_set": _bound(
            "half (b) B-side pairs present in position 3's retained drop set",
            hb["STRICT"]["of_those_present_in_the_retained_position3_drop_set"],
            hb["LOOSE"]["of_those_present_in_the_retained_position3_drop_set"],
            "pairs the S1 completion rule removed that carry a split signature",
            {**_cov_common,
             "position3_drop_set_pairs": hb["position3_drop_set_pairs"],
             "of_which_carry_S2_and_no_S1": hb["of_which_carry_S2_evidence_and_NO_S1_evidence"]}),
        "in_the_S2_and_no_S1_subset": _bound(
            "half (b) B-side pairs in the S2-evidence-and-no-S1-evidence subset",
            hb["STRICT"]["of_those_in_the_S2_evidence_and_NO_S1_evidence_subset"],
            hb["LOOSE"]["of_those_in_the_S2_evidence_and_NO_S1_evidence_subset"],
            "pairs invisible to the analysis population entirely",
            {**_cov_common,
             "position3_drop_set_pairs": hb["position3_drop_set_pairs"],
             "of_which_carry_S2_and_no_S1": hb["of_which_carry_S2_evidence_and_NO_S1_evidence"]}),
    }
    out["PUBLICATION_FORM_decisions_0090"]["bounds"]["half_a_APPLY_position5"] = \
        out["half_a_fabricated_never_started_rows"]["APPLY_position5"]["BOUND_decisions_0090"]
    out["PUBLICATION_FORM_decisions_0090"]["bounds"]["half_b_present_in_the_position3_drop_set"] = \
        hb["BOUND_decisions_0090"]["present_in_the_retained_position3_drop_set"]
    out["PUBLICATION_FORM_decisions_0090"]["THE_THIRD_KEYS_ANSWER_NOT_AN_ENDPOINT"] = {
        "complementary_signature_pairs": int(len(sig_third)),
        "status": ("a DIFFERENT KEY'S answer. Reported as a divergence, never as the ceiling "
                   "(decisions/0090, 0076 Sec 3). One instance used it and published 76 against "
                   "the other's 75; that divergence is REPORTED, NOT RECONCILED"),
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
def _independent_identity(iv: dict) -> bool:
    """True iff this invariant's coverage identity compares two INDEPENDENTLY
    SOURCED quantities -- either directly, or on every sub-population it holds."""
    c = iv.get("coverage", {})
    if c.get("sides_are_independent_expressions") is True:
        sub = c.get("per_population")
        if isinstance(sub, dict):
            return all(v.get("sides_are_independent_expressions") is True
                       for v in sub.values())
        return True
    return False


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

    # ------------------------------------------------------------------
    # BACKFILL THE D9 ROW OF THE PER-SITE D11 TABLE.
    #
    # decisions/0088 Sec 1(b): D11 is "asserted at EACH site, not once and about
    # the rest". This arm's -r4 build published `records_excluded_by_D11: null`
    # and `assertion_holds: null` on the `D9 coverage rows` row of the PUBLISHED
    # table while counting that site among the 12 where D11 is applied -- a row
    # simultaneously listed as asserted and carrying no assertion. The number
    # was sitting in d9.json the whole time and never reached the table.
    #
    # Stage 2 cannot compute it (the coverage pivot is built here), so stage 2
    # writes a visible sentinel and this block replaces it. The assertion is
    # made HERE, at the site, and the replacement is asserted rather than
    # assumed -- if the sentinel survives, the run stops.
    _ds = D9["D11_site"]
    _tab_b3 = R["B3_the_two_unasserted_mandates"]["b_per_site_D11_table"]
    _hit = [s for s in _tab_b3["sites"] if s["site"] == "D9 coverage rows"]
    assert len(_hit) == 1, "the D9 row is not where the backfill expects it"
    _row = _hit[0]
    # Idempotent: stage 3 rewrites results.json, so a stage-3-only re-run sees
    # its own backfill rather than stage 2's sentinel. Either state is accepted,
    # but an already-filled row must carry EXACTLY what this run measures --
    # otherwise it is a stale value from an earlier build and the run stops.
    assert (_row["records_excluded_by_D11"] == "PENDING_STAGE_3_BACKFILL"
            or _row["records_excluded_by_D11"] == _ds["records_excluded_by_D11"]), (
        "the D9 row carries a value that is neither stage 2's sentinel nor this run's "
        f"measurement ({_ds['records_excluded_by_D11']}) -- a stale backfill from an "
        "earlier build")
    _row.update({
        "records_excluded_by_D11": _ds["records_excluded_by_D11"],
        "records_counted_at_this_site": _ds["records_in_the_sites_input_universe"],
        "records_examined_at_this_site": _ds["records_in_the_sites_input_universe"],
        "records_used": _ds["records_used"],
        "unit": _ds["unit"],
        "assertion": _ds["assertion"],
        "assertion_holds": _ds["assertion_holds"],
        "assertion_is_VACUOUS_zero_coverage": (
            _ds["records_in_the_sites_input_universe"] == 0),
        "latest_watched_at_used_utc": _ds["latest_watched_at_used_utc"],
        "note": _ds["note"],
        "BACKFILLED_AT_STAGE_3": (
            "computed where the D9 coverage pivot is built and written into the published table "
            "here. The -r4 build left this row null in results.json while d9.json carried the "
            "number -- an unasserted site inside the table decisions/0088 Sec 1(b) created so "
            "that mandates would stop being self-reported"),
    })
    assert isinstance(_row["assertion_holds"], bool) and _row["assertion_holds"], (
        "the D9 site's D11 assertion does not hold, or is not a boolean")
    assert _row["records_examined_at_this_site"] > 0, (
        "the D9 site examined nothing -- a pass here would be a check that looked nowhere")
    _tab_b3["sites_deferred_to_another_stage"] = [
        s["site"] for s in _tab_b3["sites"]
        if s["assertion_holds"] is None or s["assertion_holds"] == "PENDING_STAGE_3_BACKFILL"]
    _tab_b3["sites_with_NO_assertion_at_all"] = [
        s["site"] for s in _tab_b3["sites"] if s["assertion_holds"] is None]
    _tab_b3["EVERY_SITE_CARRIES_A_BOOLEAN_ASSERTION_AND_AN_EXAMINED_COUNT"] = {
        "sites": len(_tab_b3["sites"]),
        "sites_with_a_boolean_assertion": sum(
            1 for s in _tab_b3["sites"] if isinstance(s["assertion_holds"], bool)),
        "sites_with_an_examined_count": sum(
            1 for s in _tab_b3["sites"]
            if isinstance(s.get("records_examined_at_this_site"), int)),
        "sites_whose_pass_is_VACUOUS_zero_coverage": [
            s["site"] for s in _tab_b3["sites"]
            if s.get("assertion_is_VACUOUS_zero_coverage")],
        "why": ("CLAUDE.md -- a check that finds nothing because it looked nowhere must FAIL, "
                "not pass, and every path that can return 'nothing found' states whether it "
                "found nothing or looked at nothing. The examined count was printed at every "
                "site on the previous build; what was missing is (i) any assertion at the D9 "
                "site and (ii) any marking that a pass on an EMPTY site is vacuous"),
    }
    assert _tab_b3["EVERY_SITE_CARRIES_A_BOOLEAN_ASSERTION_AND_AN_EXAMINED_COUNT"][
        "sites_with_a_boolean_assertion"] == len(_tab_b3["sites"]), (
        "a site in the per-site D11 table carries no boolean assertion")
    assert _tab_b3["EVERY_SITE_CARRIES_A_BOOLEAN_ASSERTION_AND_AN_EXAMINED_COUNT"][
        "sites_with_an_examined_count"] == len(_tab_b3["sites"]), (
        "a site in the per-site D11 table carries no examined count")
    (OUT / "results.json").write_text(json.dumps(R, indent=2, default=str))

    # =========================== INVARIANTS ==============================
    inv: list[dict] = []
    line5, line6 = m["line5"], m["line6"]
    never, contd, sal = m["never"], m["contd"], m["sal"]
    nA, nAH = m["nA"], m["nAH"]

    # ------------------------------------------------------------------
    # THE COVERAGE IDENTITIES ARE REBUILT SO THEY CAN FAIL.
    #
    # decisions/0088 Sec 2(d) strikes "a report that omitted a population could
    # not be written by this pipeline" as A CONTROL ASSERTED TO EXIST, on the
    # ground that most coverage identities have the population size and the
    # asserted count as THE SAME EXPRESSION. Checked in this arm and TRUE HERE
    # TOO, and worse in one respect: the r3 build HARDCODED
    # `identity_holds: True` at invariants 2, 4 and 7, and its aggregate chained
    # `.get(..., .get(..., .get(..., True)))`, so AN INVARIANT WITH NO COVERAGE
    # KEY AT ALL CONTRIBUTED A PASS.
    #
    # Fixed two ways, and both are needed:
    #   1. NO IDENTITY IS A LITERAL. Every one is arithmetic on measured counts.
    #   2. THE POPULATION SIZE COMES FROM A DIFFERENT SOURCE THAN THE ASSERTED
    #      COUNT -- from the EMITTED analysis table on disk, from the Step 4
    #      ledger file, from stage 1's own pair count, or from a spec constant --
    #      while the asserted count comes from the invariant's own arrays. An
    #      invariant run on the wrong population then FAILS its identity, which
    #      is the failure the apparatus was built for and could not detect.
    # Where a side genuinely cannot be sourced independently, the row says so
    # rather than implying otherwise.
    # ------------------------------------------------------------------
    _tab = pd.read_csv(OUT / "analysis_table.csv.gz",
                       usecols=["user_idx", "live", "in_deriv"])
    _lv = _tab.live.astype(bool).values
    _dv = _tab.in_deriv.astype(bool).values
    _ui = _tab.user_idx.values
    POP = {
        "APPLY_position5": int(len(_tab)),
        "APPLY_post_liveness": int(_lv.sum()),
        "DERIV_position5": int(_dv.sum()),
        "DERIV_post_liveness": int((_dv & _lv).sum()),
        "APPLY_accounts_position5": int(pd.unique(_ui).size),
        "DERIV_accounts_position5": int(pd.unique(_ui[_dv]).size),
    }
    POP_SRC = ("read back off the EMITTED deliverable, processed/step8/b/analysis_table.csv.gz "
               "-- a different expression and a different file from the mask arrays the "
               "assertions run over, so an invariant run on the wrong population fails its "
               "identity instead of reporting one")
    _ledger_keys = set()
    for _l in open(P4 / "pull_ledger.jsonl"):
        _d = json.loads(_l)
        _ledger_keys.add(str(_d.get("slug") or _d.get("username")).lower())
    POP["ledger_accounts"] = len(_ledger_keys)

    def cover(unit: str, n_pop: int, pop_source: str, asserted: int, not_asserted: int,
              independent: bool, why_not_independent: str = "", **extra) -> dict:
        """One coverage block. THE IDENTITY IS ARITHMETIC, NEVER A LITERAL."""
        d = {
            "unit": unit,
            f"{unit}_in_the_stated_population": int(n_pop),
            "population_size_source": pop_source,
            f"{unit}_asserted": int(asserted),
            f"{unit}_not_asserted": int(not_asserted),
            "identity_required": (f"{unit}_asserted + {unit}_not_asserted = "
                                  f"{unit}_in_the_stated_population"),
            "identity_holds": bool(int(asserted) + int(not_asserted) == int(n_pop)),
            "identity_arithmetic": f"{int(asserted)} + {int(not_asserted)} = {int(n_pop)}",
            "sides_are_independent_expressions": bool(independent),
        }
        if not independent:
            d["why_the_sides_are_not_independent"] = why_not_independent
        d.update(extra)
        return d

    def cover_ok(c: dict) -> bool:
        """A coverage block passes only if it CARRIES the key. No default."""
        return isinstance(c, dict) and c.get("identity_holds") is True

    # --- 1. outcome states partition the post-position-7 row set ----------
    # decisions/0080 Sec 3 row 1: the population is the 196,654 position-5 row set
    # AND the 195,951 live subset, BOTH STATED, plus the DERIV pair 147,370 /
    # 147,271. The table carries all position-5 rows, so the partition holds on
    # both and NEITHER SUBSTITUTES FOR THE OTHER.
    res = {}
    for nm, msk, popkey in (("APPLY_position5_row_set", line5, "APPLY_position5"),
                            ("APPLY_post_position_7_live_subset", line6, "APPLY_post_liveness"),
                            ("DERIV_position5_row_set", m["deriv5"], "DERIV_position5"),
                            ("DERIV_post_position_7_live_subset", m["deriv6"],
                             "DERIV_post_liveness")):
        n = int(msk.sum())
        c = [int((msk & never).sum()), int((msk & contd).sum()), int((msk & sal).sum())]
        overlap = int((msk & ((never & contd) | (never & sal) | (contd & sal))).sum())
        unassigned = int((msk & ~(never | contd | sal)).sum())
        # ASSERTED = rows that landed in EXACTLY ONE state, counted from the state
        # masks. NOT ASSERTED = rows in none or in more than one, counted
        # separately. Neither is the population size, and the population size is
        # read off the emitted table.
        exactly_one = n - overlap - unassigned
        cov = cover("rows", POP[popkey], POP_SRC, exactly_one, overlap + unassigned,
                    independent=True,
                    rows_asserted_note=("rows landing in EXACTLY ONE outcome state; the "
                                        "complement is counted from the overlap and "
                                        "unassigned masks, not subtracted"),
                    mask_population_for_comparison=n)
        res[nm] = {"rows_in_the_stated_population": cov["rows_in_the_stated_population"],
                   "never_started": c[0], "continued": c[1], "started_and_left": c[2],
                   "sum": sum(c), "rows_in_two_states": overlap, "rows_in_no_state": unassigned,
                   "rows_asserted": cov["rows_asserted"],
                   "rows_not_asserted": cov["rows_not_asserted"],
                   "coverage": cov,
                   "coverage_identity_holds": cov["identity_holds"],
                   "passes": bool(sum(c) == n and overlap == 0 and unassigned == 0
                                  and cov["identity_holds"])}
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
                                           "rows_in_the_stated_population, ON EACH OF THE FOUR "
                                           "STATED POPULATIONS"),
                     "population_size_source": POP_SRC,
                     "sides_are_independent_expressions": True,
                     "populations_covered": len(res),
                     "per_population": {k: v["coverage"] for k, v in res.items()},
                     "identity_holds":
                         bool(len(res) == 4
                              and all(v["coverage"]["identity_holds"] for v in res.values()))},
        "result": res,
        "passes": all(v["passes"] for v in res.values())
                  and all(v["coverage_identity_holds"] for v in res.values()),
    })

    # --- 2. filter counts decrease monotonically, coded >= ----------------
    seqA = [w["retained_pairs"] for w in R["waterfall_APPLY"]]
    seqD = [w["retained_pairs"] for w in R["waterfall_DERIV"]]
    # transitions actually COMPARED, counted in the loop that compares them --
    # not len(seq) - 1 asserted about the loop.
    _okA: list[bool] = []
    for _i in range(1, len(seqA)):
        _okA.append(seqA[_i] <= seqA[_i - 1])
    _okD: list[bool] = []
    for _i in range(1, len(seqD)):
        _okD.append(seqD[_i] <= seqD[_i - 1])
    n_trans_A, n_trans_D = len(_okA), len(_okD)
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
        "coverage": {
            "unit": "filter positions",
            "identity_required": ("transitions_asserted + transitions_not_asserted = "
                                  "the mandated chain length minus one, ON BOTH CHAINS"),
            "population_size_source": ("the MANDATED FILTER ORDER -- 7 positions, fixed by "
                                       "decisions/0029 and task-sheet.md Step 8. A spec "
                                       "constant, not a length read off the chain being "
                                       "checked, so a chain that lost or gained a position "
                                       "FAILS this identity"),
            "sides_are_independent_expressions": True,
            "populations_covered": 2,
            "per_population": {
                "APPLY": cover("transitions", 7 - 1,
                               "the mandated 7-position order, minus one",
                               n_trans_A, max(0, (7 - 1) - n_trans_A), True,
                               positions_in_the_chain=len(seqA),
                               chain_length_matches_the_mandated_order=bool(len(seqA) == 7)),
                "DERIV": cover("transitions", 7 - 1,
                               "the mandated 7-position order, minus one",
                               n_trans_D, max(0, (7 - 1) - n_trans_D), True,
                               positions_in_the_chain=len(seqD),
                               chain_length_matches_the_mandated_order=bool(len(seqD) == 7)),
            },
            "identity_holds": bool(n_trans_A == 6 and n_trans_D == 6
                                   and len(seqA) == 7 and len(seqD) == 7)},
        "passes": bool(all(_okA) and all(_okD) and len(seqA) == 7 and len(seqD) == 7
                       and n_trans_A == 6 and n_trans_D == 6),
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
    # asserted = pairs this invariant walks, counted from the array it walks;
    # not_asserted = pairs in the evidence universe carrying no in-E episode on
    # either season. The POPULATION SIZE comes from stage 1's own pair count in
    # stage1.json, so running this invariant on the NARROWER reading 0080 Sec 3
    # forbids -- S2 only, on the 196,654 table rows -- would fail the identity
    # rather than report a coverage of 196,654 as though it were the population.
    n_ev_asserted = int(len(ev_pairs))
    n_ev_neither = int(((ev_s1 == 0) & (ev_s2 == 0)).sum())
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
        "coverage": dict(
            cover("pairs",
                  int(st1["position3_drop_set"][
                      "in_frame_pairs_with_ANY_in_E_S1_or_S2_distinct_episode"]),
                  ("stage 1's own count of in-frame pairs carrying any in-E S1 or S2 distinct "
                   "episode, read back from processed/step8/b/stage1.json -- a different "
                   "computation and a different file from the ev_pairs array this invariant "
                   "walks"),
                  n_ev_asserted, n_ev_neither, independent=True,
                  pairs_asserted_S1=n_ev, pairs_asserted_S2=n_ev,
                  asserted_note=("every pair in the evidence universe is asserted on BOTH "
                                 "seasons; a pair carrying no S1 and no S2 distinct episode "
                                 "would be in the population and asserted on neither, and is "
                                 "counted as not_asserted"),
                  records_examined_by_the_set_membership_rule=st1["drop_rule"][
                      "records_examined"],
                  pairs_examined_by_the_set_membership_rule=st1["drop_rule"]["pairs_examined"],
                  records_dropped=st1["drop_rule"]["records_dropped"])),
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
        "coverage": cover(
            "rows", POP["APPLY_position5"], POP_SRC,
            int(line5.sum()), int((line5 & ~np.isfinite(nA.astype(float))).sum()),
            independent=True,
            rows_asserted_note=("rows the comparison |A| <= |A_H| was evaluated on, counted "
                                "from the mask it was evaluated over; not_asserted counts rows "
                                "in the population where |A| is not a finite count, which is a "
                                "state that cannot arise and is measured rather than assumed")),
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
        "coverage": cover(
            "rows", POP["APPLY_position5"], POP_SRC,
            int((sel & have).sum()), int((sel & ~have).sum()), independent=True,
            rows_not_asserted_reason=("rows the INDEPENDENT walk does not complete; if this is "
                                      "non-zero the two implementations disagree on the "
                                      "completer SET and that disagreement is itself the "
                                      "finding, which is why it is counted and not subtracted")),
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
            "POPULATION_OF_THAT_COUNT": ("the APPLY position-5 row set, "
                                         f"{int(sel.sum()):,} rows -- STATED AT THE POINT OF USE "
                                         "(Red Team seventh pass, finding 2, against this arm: "
                                         "the -r4 build published this integer here and the same "
                                         "integer on waterfall LINE 1 in the other deliverable, "
                                         "23,453 pairs apart, with neither naming its "
                                         "population)"),
            "unit": "rows of the stated population",
            "on_every_population": {
                nm: int((msk & tie).sum())
                for nm, msk in (("line1_220107", m["line1"]),
                                ("position4_201900", m["line4"]),
                                ("APPLY_position5_196654", line5),
                                ("APPLY_position6_post_liveness_195951", m["line6"]),
                                ("DERIV_position5_147370", m["deriv5"]),
                                ("DERIV_position6_post_liveness_147271", m["deriv6"]))},
            "CROSS_CHECK_against_the_pipelines_own_label": {
                "what": ("this count is formed from the INDEPENDENTLY recomputed S1 completion "
                         "date; the waterfall's D2 section forms it from the pipeline's own "
                         "`binds` label. Two implementations, one quantity -- so agreement is "
                         "evidence and not a restatement"),
                "independent_here": int((sel & tie).sum()),
                "pipeline_label_there": int(R["required_counts"]["D2_negative_lag"][
                    "THE_168_MEASURED_ON_EVERY_POPULATION"]["by_population"][
                    "APPLY_position5_196654"]),
                "agree": bool(int((sel & tie).sum()) == int(
                    R["required_counts"]["D2_negative_lag"][
                        "THE_168_MEASURED_ON_EVERY_POPULATION"]["by_population"][
                        "APPLY_position5_196654"])),
            },
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
        "coverage": dict(
            cover("rows", POP["APPLY_position5"], POP_SRC,
                  int(len(psel)) + int(len(elsewhere)), 0, independent=True,
                  rows_asserted_in_range_clause=int(len(psel)),
                  rows_asserted_null_clause=int(len(elsewhere)),
                  rows_asserted_note=("the two clauses are asserted on disjoint row sets and "
                                      "their sizes are measured separately; the sum is compared "
                                      "against the EMITTED table's row count, which is where "
                                      "the r3 gap would have shown")),
            **{
            "corrected_this_run": ("this arm's previous run asserted the range clause on the "
                                   "POST-LIVENESS 19,042 while the null clause ran on the "
                                   "position-5 177,513 -- 196,555 against a 196,654-row table, "
                                   "with 99 rows covered by NEITHER clause. Those 99 are "
                                   "exactly the started-and-left liveness exclusions. That gap "
                                   "is what decisions/0080 Sec 3 was written on, and it is "
                                   "closed here"),
            "started_and_left_rows_post_liveness_for_reference": int((line6 & sal).sum()),
        }),
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
        # asserted = accounts classified into one of the three exhaustive classes
        # (all-live / mixed / all-not-live), counted from the class arrays;
        # not_asserted = accounts in the population that fell into none. The
        # POPULATION SIZE is the distinct user_idx count read off the EMITTED
        # table, not len(accts_all).
        _classified = (int(len(np.setdiff1d(accts_all, accts_notlive)))
                       + int(len(both)) + int(len(only_nl)))
        _covk = cover("accounts", POP[nm + "_accounts_position5"], POP_SRC,
                      _classified, int(len(accts_all)) - _classified, independent=True,
                      classes=["all pairs live", "mixed", "all pairs not live"],
                      accounts_asserted_note=("accounts falling into one of the three "
                                              "exhaustive classes, counted from the class "
                                              "arrays; the population size is the distinct "
                                              "user_idx count in the emitted table"))
        whole[nm] = {
            "accounts_in_the_stated_population": _covk["accounts_in_the_stated_population"],
            "accounts_asserted": _covk["accounts_asserted"],
            "accounts_not_asserted": _covk["accounts_not_asserted"],
            "coverage": _covk,
            "coverage_identity_holds": _covk["identity_holds"],
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
                                           "accounts_in_the_stated_population, ON BOTH "
                                           "POPULATIONS"),
                     "population_size_source": POP_SRC,
                     "sides_are_independent_expressions": True,
                     "populations_covered": len(whole),
                     "per_population": {k: v["coverage"] for k, v in whole.items()},
                     "identity_holds": bool(len(whole) == 2 and all(
                         v["coverage"]["identity_holds"] for v in whole.values()))},
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
        "coverage": dict(cover(
            "accounts", POP["ledger_accounts"],
            ("processed/step4/pull_ledger.jsonl, counted by a SECOND pass over the file that "
             "keys on slug-or-username and is independent of the outcome classification this "
             "invariant sums over"),
            asserted, len(led) - asserted, independent=True,
            by_final_ledger_outcome=per_class,
            skipped_classes_total_pairs_contributed=skipped_pairs,
            skipped_classes_total_never_started_pairs_contributed=skipped_ns,
            a_second_class_checked_separately={
                "parsed_accounts_with_no_ledger_row_at_all": len(idx_unknown),
                "why": ("an account present in the parsed sweep but absent from the ledger "
                        "would be covered by no ledger class, so it is counted rather than "
                        "assumed empty"),
            })),
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

    # --- 9. CODE CHECK: no position-5 row has tau2 > tau_pull -------------
    # decisions/0088 Sec 1(c) -- PROMOTE THE EXISTING ASSERTION. It already ran
    # inside the pipeline but sat OUTSIDE the published invariant set, so no
    # reader of the deliverable could see it. Published here, labelled CODE
    # CHECK. NOTE: this takes the assertion set to NINE members. task-sheet.md's
    # own count sentence still says the set has eight; that is a count the
    # ruling moved and the sentence has not caught up, and it is reported as a
    # spec observation rather than silently reconciled.
    pr = R["B3_the_two_unasserted_mandates"]["c_the_promoted_assertion"]
    inv.append({
        "invariant": "no position-5 row has tau2 > tau_pull",
        "label": "CODE CHECK",
        "why_it_cannot_fail_on_data": ("D10 defines position 5 as [T0] + (max(W, 91) + H) x 24h "
                                       "<= tau_pull, and at W = 108 that expression IS tau2. It "
                                       "can only catch tau2 or the right-censoring bound "
                                       "computed wrongly -- for instance H dropped from the "
                                       "censoring term while tau2 kept it"),
        "ruling": pr["ruling"],
        "population": ("BOTH POPULATIONS: the 196,654 APPLY position-5 row set and the 147,370 "
                       "DERIV position-5 row set, every row of each"),
        "coverage": {
            "unit": "rows",
            "identity_required": ("rows_asserted + rows_not_asserted = "
                                  "rows_in_the_stated_population, ON BOTH POPULATIONS"),
            "population_size_source": POP_SRC,
            "sides_are_independent_expressions": True,
            "populations_covered": 2,
            "per_population": {
                "APPLY_position5": cover(
                    "rows", POP["APPLY_position5"], POP_SRC,
                    int(pr["by_population"]["APPLY_position5"]["rows_examined"]), 0, True),
                "DERIV_position5": cover(
                    "rows", POP["DERIV_position5"], POP_SRC,
                    int(pr["by_population"]["DERIV_position5"]["rows_examined"]), 0, True),
            },
            "identity_holds": bool(
                pr["by_population"]["APPLY_position5"]["rows_examined"] == POP["APPLY_position5"]
                and pr["by_population"]["DERIV_position5"]["rows_examined"]
                == POP["DERIV_position5"]),
        },
        "checked": pr["by_population"],
        "reading": pr["the_bound_is_ATTAINED_not_slack"],
        "passes": bool(pr["passes"]),
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

    _n_pure = sum(1 for i in inv if i["label"] == "CODE CHECK")
    coverage = {
        "item": "the set-membership drop rule",
        "status": ("A COVERAGE COUNT, NOT AN INVARIANT (decisions/0074 ruling 3). Step 8's own "
                   "bullet calls it 'an implementation check, not a data check'. Reported, not "
                   f"asserted -- asserting it would add another pass to a report where "
                   f"{_n_pure} of {len(inv)} already cannot fail on data"),
        "SUPERSEDED_PHRASING_CORRECTED_THIS_RUN": (
            "this arm's -r5 build wrote 'a report where six of EIGHT cannot fail on data' HERE, "
            "in the body of a deliverable whose head states the set is NINE and whose surface "
            "check concludes no surface still states the old count. Red Team seventh pass, "
            "finding 1. The surface check opened task-sheet.md, this arm's definition file and "
            "specs/step8-readback.md -- IT DID NOT OPEN artifacts/, WHICH IS PROPAGATION "
            "SURFACE 6 AND IS WHERE THE STRING WAS. The count is now derived from len(inv) and "
            "the label field, and a self-check over this arm's own emitted artifacts runs at "
            "stage 4"),
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

    # =====================================================================
    # THE NEGATIVE CONTROL IS RUN, NOT DESCRIBED.
    #
    # This arm's r4 build published a field called `what_a_failure_would_look_
    # like` -- a SENTENCE describing the failure the rebuilt coverage apparatus
    # would catch. decisions/0089 Sec 1 then recorded it as "demonstrating
    # failing". IT WAS NOT DEMONSTRATED; it was described. CLAUDE.md's own words:
    # "a control asserted to exist is not a control", and the same file records
    # a withdrawn property whose "mechanism never fired" -- found by reading the
    # code rather than the claim.
    #
    # So the failure is EXECUTED here, through the SAME cover(), cover_ok() and
    # _independent_identity() the real invariants go through -- not a re-
    # implementation, which would prove only that a second copy behaves. Four
    # injected defects, each the shape of a real one this chain has hit, and
    # each ASSERTED to be caught. If any control passes the bad input the run
    # dies here.
    # =====================================================================
    _neg_cases = []

    # 1. the r3 gap at invariant 6 exactly: asserted on the post-liveness row
    #    set while NAMING the position-5 population.
    _bad_pop = cover("rows", POP["APPLY_position5"], POP_SRC,
                     int(line6.sum()), 0, True)
    _neg_cases.append({
        "case": "invariant asserted on the post-liveness row set while naming position 5",
        "the_real_defect_it_reproduces": ("this arm's r3 build asserted p on 19,042 post-liveness "
                                          "rows with a position-5 non-S&L clause of 177,513, "
                                          "summing to 196,555 against a 196,654-row table"),
        "identity_arithmetic": _bad_pop["identity_arithmetic"],
        "cover_ok_returned": cover_ok(_bad_pop),
        "expected": False,
        "control_caught_it": cover_ok(_bad_pop) is False,
    })

    # 2. the r3 aggregate bug: an invariant carrying NO coverage key at all,
    #    which the chained .get(..., True) default turned into a pass.
    _neg_cases.append({
        "case": "invariant carrying no coverage key at all",
        "the_real_defect_it_reproduces": ("the r3 aggregate chained .get(..., .get(..., True)), "
                                          "so an invariant with no coverage key CONTRIBUTED A "
                                          "PASS -- a control that could not see the thing it was "
                                          "built to see"),
        "cover_ok_returned": cover_ok({}),
        "expected": False,
        "control_caught_it": cover_ok({}) is False,
    })

    # 3. a hardcoded literal identity -- what invariants 2, 4 and 7 carried on r3.
    _neg_cases.append({
        "case": "identity_holds hardcoded True with no arithmetic behind it",
        "the_real_defect_it_reproduces": ("the r3 build HARDCODED identity_holds: True at "
                                          "invariants 2, 4 and 7"),
        "cover_ok_returned": cover_ok({"identity_holds": True}),
        "expected": True,
        "note": ("cover_ok CANNOT catch this one -- a literal True is indistinguishable from a "
                 "computed True at that interface, which is why the SEPARATE audit counter "
                 "`identities_that_are_literals` exists and is reported below. STATED RATHER "
                 "THAN LEFT AS AN IMPLIED PASS"),
        "control_caught_it": None,
        "caught_by_instead": "identities_that_are_literals, which must be 0",
    })

    # 4. decisions/0088 Sec 2(d)'s own finding: an identity whose two sides are
    #    the same expression cannot detect a wrong population.
    _same_expr = cover("rows", int(line6.sum()), "the asserted count itself",
                       int(line6.sum()), 0, False,
                       "both sides are the same expression -- 0088 Sec 2(d)")
    _neg_cases.append({
        "case": "identity whose population size and asserted count are the SAME expression",
        "the_real_defect_it_reproduces": ("decisions/0088 Sec 2(d): 8 of 13 coverage identities "
                                          "in one arm were cover(unit, pop, N, N), so they could "
                                          "not detect an invariant run on a population other "
                                          "than the one named"),
        "identity_arithmetic": _same_expr["identity_arithmetic"],
        "cover_ok_returned": cover_ok(_same_expr),
        "expected": True,
        "note": ("it PASSES, and that is the point -- the identity is vacuous. It is caught by "
                 "_independent_identity, not by cover_ok"),
        "independent_identity_returned": _independent_identity({"coverage": _same_expr}),
        "control_caught_it": _independent_identity({"coverage": _same_expr}) is False,
    })

    # 5. the aggregate itself, run over a corrupted copy of the REAL invariant
    #    list, so what is exercised is the published aggregate expression.
    _corrupt = [dict(i) for i in inv]
    _corrupt[0] = dict(_corrupt[0], coverage=_bad_pop)
    _agg_corrupt = bool(len(_corrupt) > 0
                        and all(cover_ok(i.get("coverage", {})) for i in _corrupt))
    _corrupt2 = [dict(i) for i in inv]
    _corrupt2[0] = {k: v for k, v in _corrupt2[0].items() if k != "coverage"}
    _agg_corrupt2 = bool(len(_corrupt2) > 0
                         and all(cover_ok(i.get("coverage", {})) for i in _corrupt2))
    _neg_cases.append({
        "case": "the PUBLISHED aggregate expression, run over the real invariant list with one "
                "invariant's coverage swapped for the wrong-population block from case 1",
        "invariants_in_the_corrupted_list": len(_corrupt),
        "aggregate_returned": _agg_corrupt,
        "expected": False,
        "control_caught_it": _agg_corrupt is False,
    })
    _neg_cases.append({
        "case": "the PUBLISHED aggregate expression, run over the real invariant list with one "
                "invariant's coverage key DELETED",
        "invariants_in_the_corrupted_list": len(_corrupt2),
        "aggregate_returned": _agg_corrupt2,
        "expected": False,
        "control_caught_it": _agg_corrupt2 is False,
    })

    _checkable = [c for c in _neg_cases if c["control_caught_it"] is not None]
    neg = {
        "why_this_block_exists": (
            "this arm's r4 build published `what_a_failure_would_look_like` -- a DESCRIPTION of "
            "the failure the apparatus would catch -- and decisions/0089 Sec 1 recorded it as "
            "'demonstrating failing'. It was not demonstrated. CLAUDE.md: a control asserted to "
            "exist is not a control. The failures are EXECUTED here"),
        "run_through": ("the SAME cover(), cover_ok() and _independent_identity() the published "
                        "invariants go through, and for the aggregate, the same expression the "
                        "published `identity_holds_on_every_invariant` uses. Not a "
                        "re-implementation, which would prove only that a second copy behaves"),
        "cases": _neg_cases,
        "cases_run": len(_neg_cases),
        "cases_whose_control_is_checkable": len(_checkable),
        "cases_caught": sum(1 for c in _checkable if c["control_caught_it"]),
        "cases_NOT_caught": [c["case"] for c in _checkable if not c["control_caught_it"]],
        "two_cases_PASS_BY_DESIGN_and_are_named": [
            c["case"] for c in _neg_cases if c["control_caught_it"] is None],
        "coverage_note": ("this block reports the number of cases it ran. A negative-control "
                          "block that ran zero cases and reported clean is the failure "
                          "CLAUDE.md's standing rule exists to prevent"),
    }
    neg["all_checkable_cases_caught"] = bool(
        len(_checkable) > 0 and all(c["control_caught_it"] for c in _checkable))
    # a control that cannot fail is not a control: if any injected defect got
    # through, this run does not produce a deliverable.
    assert neg["all_checkable_cases_caught"], neg["cases_NOT_caught"]

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
        # NO DEFAULT. An invariant without a coverage identity FAILS this
        # aggregate; it does not inherit a pass.
        "invariants_carrying_a_coverage_identity": sum(1 for i in inv if cover_ok(i["coverage"])),
        "invariants_total": len(inv),
        "invariants_missing_a_coverage_identity": [
            i["invariant"][:60] for i in inv if "identity_holds" not in i.get("coverage", {})],
        "identity_holds_on_every_invariant": bool(
            len(inv) > 0 and all(cover_ok(i.get("coverage", {})) for i in inv)),
        "how_the_aggregate_is_computed": (
            "every invariant must CARRY coverage.identity_holds and it must be True. The r3 "
            "build chained .get(..., .get(..., .get(..., True))), so an invariant with no "
            "coverage key contributed a PASS -- a control that could not see the thing it was "
            "built to see. There is no default here"),
        "AUDIT_can_each_identity_actually_fail": {
            "why_this_block_exists": (
                "decisions/0088 Sec 2(d) strikes 'a report that omitted a population could not "
                "be written by this pipeline' as A CONTROL ASSERTED TO EXIST, on the ground "
                "that most coverage identities have the population size and the asserted count "
                "as THE SAME EXPRESSION. That was true in this arm too, and worse: three "
                "identities were HARDCODED literals. Rebuilt this run so each identity compares "
                "a count measured from the invariant's own arrays against a population size "
                "sourced from a DIFFERENT FILE -- the emitted analysis table, the Step 4 "
                "ledger, stage 1's own pair count, or the mandated 7-position order"),
            "identities_whose_two_sides_are_independent_expressions": sum(
                1 for i in inv if _independent_identity(i)),
            "identities_that_are_literals": sum(
                1 for i in inv if isinstance(i.get("coverage", {}).get("identity_holds"), bool)
                and "identity_arithmetic" not in i.get("coverage", {})
                and "per_population" not in i.get("coverage", {})),
            "population_size_sources_used": sorted({
                str(i.get("coverage", {}).get("population_size_source", ""))[:60]
                for i in inv if i.get("coverage", {}).get("population_size_source")}),
            "THE_FAILURE_IS_EXECUTED_NOT_DESCRIBED": neg,
            "STRUCK_SENTENCE": (
                "'The run asserts this, so a report that omitted a population could not be "
                "written by this pipeline' -- STRUCK by decisions/0088 Sec 2(d), whatever else "
                "is ruled. This arm did not publish that sentence, and it is recorded here so "
                "the strike is visible on this surface rather than only in the decision log"),
        },
        "measured_on_build": BUILD,
    }

    # the r4 build TYPED a claim about task-sheet.md's and this arm's definition
    # file's assertion-set count. decisions/0089 Sec 3 moved both. Read live at
    # stage 2 and carried here as the MEASUREMENT, not as the previous prose.
    _sc5 = R["analysis_table"]["column_set_is_ENUMERATED"][
        "residuals_this_arm_reported_last_run_RE_MEASURED"][
        "c_surface_claims_this_arm_published_last_run_RE_READ"][
        "item_5_the_assertion_set_count_on_the_spec_surfaces"]

    # ------------------------------------------------------------------
    # THE LABEL COUNTS ARE DERIVED FROM THE LABELS, NOT TYPED.
    #
    # Red Team seventh pass, finding 3, against THIS arm: the -r4 prose said
    # "SEVEN of the nine assertions CANNOT FAIL ON ANY DATA" and then described
    # one of the seven as a genuine cross-check BECAUSE a value is recomputed
    # independently. If the recomputation gives it force, it can fail on data --
    # the sentence contradicted itself. It contradicted the `counts` block two
    # lines below it as well, which already said 6 / 1 / 2.
    #
    # The fix is structural rather than textual: every count below is computed
    # from the `label` field of the invariants actually emitted, and the prose
    # interpolates those numbers. A relabelled or added invariant moves the
    # sentence with it. A TYPED count is exactly what went wrong.
    _pure = [i for i in inv if i["label"] == "CODE CHECK"]
    _bycon = [i for i in inv if i["label"].startswith("CODE CHECK BY CONSTRUCTION")]
    _data = [i for i in inv if i["label"] == "DATA CHECK"]
    assert len(_pure) + len(_bycon) + len(_data) == len(inv), (
        "an invariant carries a label this block does not classify -- the count would be "
        "wrong and silent, which is the defect being corrected")
    _LB = {
        "assertions_total": len(inv),
        "pure_code_checks": len(_pure),
        "pure_code_check_names": [i["invariant"] for i in _pure],
        "code_check_by_construction_and_data_check_as_specified": len(_bycon),
        "genuine_data_checks": len(_data),
        "cannot_fail_on_any_data": len(_pure),
        "can_fail_on_data_as_specified": len(_bycon) + len(_data),
        "can_fail_on_data_as_specified_names": [i["invariant"] for i in _bycon + _data],
        "DERIVED_NOT_TYPED": (
            "every number in this block is computed from the `label` field of the emitted "
            "invariants. decisions/0089 Sec 3 and Red Team seventh pass finding 3 both landed "
            "on a TYPED count that had drifted from the set it described"),
        "the_clock_start_is_counted_as_ABLE_TO_FAIL": (
            "it is CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED. Counting it among the "
            "unable-to-fail contradicts the reason it is kept: task-sheet.md requires the "
            "first-pass S1 completion date to be RECOMPUTED INDEPENDENTLY, and a disagreement "
            "between two implementations on real records is a real finding. Read back rather "
            "than recomputed it would degrade to a pure code check -- and then the count would "
            f"be {len(_pure) + len(_bycon)} unable and {len(_data)} able"),
    }

    out = {
        "instance": "analytics-engineer-b", "namespace": "b",
        "mode": "GATE -- proposal only, nothing adopted",
        "provenance": provenance_block(),
        "invariant_coverage_rule": cov_rule,
        "how_to_read_this_report": (
            f"{_LB['pure_code_checks']} of the {_LB['assertions_total']} assertions CANNOT FAIL "
            "ON ANY DATA. They are the pure CODE CHECKS -- "
            + ", ".join(_LB["pure_code_check_names"]) + ". "
            f"{_LB['can_fail_on_data_as_specified']} CAN fail on data AS SPECIFIED. "
            f"{_LB['genuine_data_checks']} of those are the genuine DATA CHECKS, both added by "
            "decisions/0076 because before it the set had ZERO: no account dropped wholesale, "
            "and no access_denied or skipped account read as empty. THE THIRD IS THE CLOCK "
            "START, and it is counted here as ABLE TO FAIL rather than as unable: it is a code "
            "check BY CONSTRUCTION -- T0 = max() makes all three clauses true of any correct "
            "max() -- but AS SPECIFIED (task-sheet.md; decisions/0068) it recomputes the "
            "first-pass S1 completion date INDEPENDENTLY, and two implementations can disagree "
            "on real records. THAT IS WHAT GIVES IT FORCE, AND A CHECK WITH FORCE IS A CHECK "
            "THAT CAN FAIL. "
            "***CORRECTED THIS RUN, Red Team seventh pass, finding 3: this arm's -r5 build "
            "published 'SEVEN of the nine assertions CANNOT FAIL ON ANY DATA' and then, in the "
            "same sentence, called the seventh a genuine cross-check BECAUSE a value is "
            "recomputed independently. Those cannot both hold -- if the recomputation gives it "
            "force it can fail on data. The count is now DERIVED FROM THE LABELS rather than "
            "typed, so the sentence and the label set cannot diverge again.*** "
            "'All invariants passed' is therefore mostly a statement that the code computed "
            "what it was told to; it is NOT evidence for the liveness rule or for any "
            "published share."),
        "counts": {**_LB,
                   "the_set_moved_from_EIGHT_to_NINE_at_0088": (
                       "decisions/0088 Sec 1(c) PROMOTES the tau2 <= tau_pull assertion into "
                       "the published set. It already ran; it was invisible to a reader of the "
                       "deliverable"),
                   "the_surface_count_this_arm_reported_last_run_IS_RE_READ_NOT_CARRIED": _sc5,
                   "items_reported_but_not_asserted": 2,
                   "items_reported_but_not_asserted_named": [
                       "the set-membership drop rule -- a coverage count (0074 ruling 3)",
                       "the 703 expectation -- a population reconciliation (0047, 0069)"]},
        "B3_the_two_unasserted_mandates": R["B3_the_two_unasserted_mandates"],
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
