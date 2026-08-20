"""The single register of Step 7 figure values. Imported by both scripts.

Human Lead ruling, 2026-08-13, from Red Team's twelfth HOLD (B3): there were TWO
hand-maintained registers -- one in the regenerator, one in the checker -- already
divergent by one entry after a single entry's use, and NEITHER contained the values that
were actually wrong. Two registers is one register plus a defect waiting.

Everything that decides whether a number is correct lives here and nowhere else.

FOUR KINDS OF ENTRY, and the distinction that matters is SCOPE:

  SUPERSEDED        wrong everywhere. Every occurrence is a defect.
  SUPERSEDED_IN     wrong in ONE file and right in another. The ratios are the case this
                    exists for: 0.509 is arm b's correct figure and arm a's wrong one,
                    because the two arms divide by different denominators.
  ADOPTED           current. The positive half requires it present on every owning surface.
  LEGITIMATE        a value that looks superseded and is not, with the reading that makes
                    it correct. Registering one DISARMS the control against it, so each
                    carries its reason.

WHOLLY_SUPERSEDED_FILES is an explicit allowlist, one line per file with a reason. It
replaces the rule that any file with SUPERSEDED in its first 45 lines was exempt in
whole -- that exempted 19 .md and 16 .json files, which was the entire Step 7 artifact
set including both OPERATIVE deliverables, and it is why a wrong ratio survived a passing
check. CLAUDE.md requires a string be named superseded AT THE POINT OF USE; a stamp 300
lines above a value is not the point of use.

PARTIALLY superseded files -- step7-liveness-bb-{a,b} -- are deliberately NOT here.
"""

# ---------------------------------------------------------------- superseded everywhere
SUPERSEDED = {
    9.6830: "S&L floor / conditional sub-interval floor, APPLY -- now 9.6372",
    0.0503: "conditional sub-interval width, APPLY -- now 0.0961",
    73.3466: "Continued value, attainable-corner floor row, APPLY -- now 73.3924",
    73.6537: "Continued ceiling, APPLY -- now 73.6995",
    11.3619: "S&L floor / sub-interval floor, DERIV -- now 11.3015",
    82.4327: "Continued ceiling, DERIV -- now 82.4930",
    0.4033: "APPLY bound width differenced from rounded endpoints -- a rounding artifact; 0.4032",
    0.4703: "arm a's S&L bound over sampling width, pre-widening -- now 0.5304",
}

# A line that carries BOTH a superseded value and the value that replaced it is
# self-declaring: it is narrating the transition, which is what a record is for. This is a
# principled marker, unlike widening the regex until narration happens to match.
SUCCESSOR = {9.6830: 9.6372, 0.0503: 0.0961, 73.3466: 73.3924, 73.6537: 73.6995,
             11.3619: 11.3015, 82.4327: 82.4930, 0.4033: 0.4032, 0.4703: 0.5304}

# ------------------------------------------------- superseded in ONE file, correct in another
# key: (file substring, value). The bound-over-sampling ratios are per-arm because the two
# arms divide by different denominators and 0058 REPORTS that divergence rather than
# reconciling it. A global register cannot express this, which is why 0.509 sat wrong in
# arm a through two reviews: it is right in arm b.
SUPERSEDED_IN = {
    ("bb-a", 0.5090): "arm b's ratio, written into arm a's file by 0057. Arm a's is 0.5304",
    ("bb-a", 0.0690): "arm a's DERIV ratio pre-widening (0.0672/0.9744). Arm a's is 0.1309",
    # B4 (Red Team 13). 0.2813 = 0.307138 / 1.092, and 1.092 is the UNDER-THE-RULE point
    # estimate's CI width -- arm b's convention. Arm a's own convention, used for its
    # started-and-left ratio, is the FLOOR ENDPOINT's CI, 1.09, giving 0.2818. Arm a was
    # running two conventions in one six-line block. 0060 takes the floor-endpoint one.
    ("bb-a", 0.2813): "computed on arm b's convention (under-the-rule CI 1.092). Arm a's is 0.2818",
}

# ------------------------------------------------------------------------------- adopted
SPEC = ["1 task-sheet", "2 ds", "3 ds-b", "4 ae", "5 ae-b"]
# ae / ae-b deliberately hold NO Step 9 bound figures (0055 SS5a), so they are not owners.
DS = SPEC[:3]
ADOPTED = {
    9.6372: DS + ["6 artifacts", "7 second-brain"],
    0.0961: DS + ["6 artifacts", "7 second-brain"],
    0.4032: DS + ["6 artifacts", "7 second-brain"],
    73.6995: DS + ["6 artifacts", "7 second-brain"],
    73.3924: ["6 artifacts"],
    11.3015: DS + ["6 artifacts", "7 second-brain"],
    82.4930: DS + ["6 artifacts"],
}
# Per-arm, so the positive half reaches this entry's OWN corrections -- which it did not,
# and that is how B1 stayed invisible to both scripts.
ADOPTED_IN = {
    # started-and-left
    ("bb-a", 0.5304): "arm a, APPLY: 0.403246 / 0.7602, its own floor-endpoint CI",
    ("bb-a", 0.1309): "arm a, DERIV: 0.127570 / 0.9744",
    ("bb-b", 0.5090): "arm b, APPLY: 0.403246 / 0.7922, the under-the-rule point estimate's CI",
    ("bb-b", 0.1310): "arm b, DERIV: 0.127570 / 0.9737",
    # never-started (B4). 0059 covered four values and all four were started-and-left.
    ("bb-a", 0.2818): "arm a, APPLY: 0.307138 / 1.09, its own floor-endpoint CI -- SAME convention "
                      "as its S&L ratio, which 0.2813 was not",
    ("bb-b", 0.2721): "arm b, APPLY: 0.307138 / 1.12872, the under-the-rule point estimate's CI",
}
# The two DERIV never-started ratios are the third and fourth of the four. Both are exactly
# 0.0, because the DERIV never-started bound is DEGENERATE -- [6.2055%, 6.2055%], width 0.0,
# zero never-started exclusions. They are NOT registered: 0.0 matches somewhere in almost
# every file, so a row for it would disarm nothing and flag everything. Stated here rather
# than left as two silently missing entries.
DERIV_NS_RATIOS_ARE_ZERO_BY_DEGENERACY = True

# ------------------------------------------------------------- STEP 8 NUMERIC REGISTER
# 0101, closing R3. Until now these figures lived ONLY in second-brain's memory --
# a SECOND hand-maintained register, which is exactly the hazard 0059 B3 forbids:
# "there were TWO hand-maintained registers ... already divergent by one entry after a
# single entry's use, and NEITHER contained the values that were actually wrong."
#
# TRANSFERRED, NOT AUTHORED. Every reading below is second-brain's, carried across with
# its scope and its file citation. Re-deriving them here would have created the THIRD
# register rather than closing the second.
#
# Each row carries what CLAUDE.md requires of a legitimate reading: the reading that makes
# the figure correct, AND the use that makes it a defect. Registering a false positive
# DISARMS the control against it -- 9.6830 was registered as legitimate while superseded on
# four surfaces -- so a row with an EMPTY defect column is a blanket exemption and is
# itself the defect. second-brain found exactly that on 703 and repaired it.
#
# THE TWO COINCIDENCES ARE THE DANGEROUS ROWS. 703 and 604 each name two unrelated
# quantities that happen to be equal, and both arms flag the collision themselves.
STEP8_LEGITIMATE = {
    703: ("TWO readings, both current, and they are a COINCIDENCE. (i) ALT-BROAD's APPLY "
          "liveness exclusion count, 604 + 99 from 216 accounts. (ii) distinct S2 episodes in "
          "the SEPARATING interval [tau1, tau1+24h) on APPLY position 5 -- both arms, "
          "step8-waterfall-a.json:2095 and step8-invariants-b.json:219, 0089 SS2(a) / 0091 SS1; "
          "(ii) sits beside [tau2, tau2+24h) = 303 and the DERIV pair 595 / 261",
          "quoting (ii) as the exclusion count, or (i) as evidence about the half-open form. "
          "UNRELATED QUANTITIES THAT HAPPEN TO BE EQUAL"),
    604: ("TWO readings, both current, and they are a COINCIDENCE. (i) the never-started "
          "COMPONENT of ALT-BROAD's 703 on APPLY, 191 accounts. (ii) invariant 8's scope note, "
          "arm a: the 7 accounts skipped on one attempt but yielding data on another hold 604 "
          "position-5 pairs, 119 of them never-started -- step8-invariants-a.json:628",
          "604 as a liveness exclusion TOTAL -- that is ALT's superseded answer, and producing "
          "it at position 6 IS a divergence (0046 -> 0048)"),
    168: ("D2's max() BOTH-BIND tie count on APPLY, and it is NOT population-invariant: 168 is "
          "invariant across line 1 (220,107), position 4 (201,900), position 5 (196,654) AND "
          "post-liveness (195,951) -- step8-waterfall-a.json:1311,1320",
          "quoted without its population. 0092 SS3's premise '168 cannot be correct on both' is "
          "WITHDRAWN: both arms' differing readings would have given 168, and the agreement was "
          "INVARIANCE, not error"),
    153: ("D2's both-bind tie count on DERIV -- 147,370 and 147,271. THE COUNT IS NOT "
          "POPULATION-INVARIANT and this is the half that proves it",
          "quoted without its population, or listed among D9's numbers -- 0093 SS3(a) did that and "
          "was corrected at 0099. ALSO the ALT-MATCHED S&L component at several arms in "
          "step7-liveness-mm-* (allowlisted, history) and a 153.4 d median in step5-contamination"),
    75: ("D9's LOOSE key = the CEILING of the published bound [0, 75] on complementary pairs "
         "(0090). Also the U3 universe size",
         "75 as 'D9's result' -- NEITHER ENDPOINT IS THE POINT ESTIMATE (0090)"),
    76: ("the THIRD key's answer -- it strips a trailing digit group of arbitrary length, "
         "reducing the-100 to the. Reported as a divergence only (0076, 0078 SS3, 0090). Its "
         "half (b) is 28 against loose 27",
         "76 as the CEILING. It is NOT AN ENDPOINT -- a different key's answer"),
    46428: ("distinct SLUGGED show IDs in the parsed sweep = the U1 universe ruled at 0088 SS3, "
            "both arms -- step8-waterfall-b.md:339, step8-waterfall-a.md:477",
            "confusing it with the D9 COVERAGE PIVOT count, which is a different object"),
    46366: ("the D9 COVERAGE PIVOT's show-ID count, arm a -- a different object from U1, 62 "
            "fewer, WITHIN ONE ARM (0089 SS3, correcting 0087 SS2's '62 apart' two-arm reading). "
            "The pivot count ITSELF diverges across arms: 46,366 (a) against 45,014 (b), gate "
            "residual 4, resolvable only by reading each arm's mask",
            "labelled distinct_show_ids_in_the_sweep -- arm a published both for one label 27 "
            "lines apart, and its '0 carry no slug' clause was computed on the wrong base"),
    726102: ("arm a's D9 candidate (user, show) pairs: 435,642 + 8,834 + 281,626. Also "
             "747,478 - 21,376 S3-only",
             "treating the one-pair gap against arm b's 726,103 as the whole S3-only gap -- "
             "which is how it stayed unrecorded (0089 SS3)"),
    726103: ("arm b's D9 candidate (user, show) pairs: 435,643 + 8,834 + 281,626. A GENUINE "
             "ONE-PAIR DIVERGENCE from arm a, reported not reconciled; two classes agree exactly "
             "and the S1-only class differs by 1",
             "726,103 as 'arm b's user-show coverage ROWS' -- that was 0086 SS1 / 0087 SS2's "
             "characterisation and is SUPERSEDED (0089 SS2b)"),
    71: ("position-5 rows whose OUTCOME STATE changes under the forbidden date(ts) <= date(tau) "
         "form, APPLY: 52 at tau1 + 19 at tau2. Both arms agree to the row. A COUNTERFACTUAL, at "
         "W = 108 only (0091 SS1)",
         "as a figure that moves the published result. IT DOES NOT -- it is what makes the "
         "half-open mandate OUTCOME_DECIDING rather than vacuous. OCCUPIED_INERT is the "
         "WITHDRAWN verdict (0089 SS2a, reversed 0091 SS1)"),
    59: ("the same counterfactual on DERIV: 45 at tau1 + 14 at tau2",
         "same as 71 -- it is a counterfactual, not a published result"),
    20: ("APPLY rows with tau2 EXACTLY AT tau_pull. tau2 > tau_pull is 0, but THE BOUND IS "
         "ATTAINED -- a >= form of invariant 9 would fail (0089 SS1, 0091 SS3)",
         "reading the 0 as slack. A passing assertion AT THE BOUND and one WITH SLACK are not "
         "the same evidence"),
    17: ("the same on DERIV",
         "reading the 0 as slack -- see 20"),
}
# Every row states BOTH halves. A row whose defect column is empty is a blanket exemption,
# which is the shape second-brain found on 703 and repaired.
for _v, _r in STEP8_LEGITIMATE.items():
    assert len(_r) == 2 and _r[0].strip() and _r[1].strip(), \
        f"STEP8_LEGITIMATE[{_v}] must carry BOTH the legitimate reading and the defective use"

# --------------------------------------------------------------------------- legitimate
LEGITIMATE = {
    0.3575: "APPLY exclusion share of population, 703 / 196,654. Superseded only as a bound WIDTH",
    0.0672: "DERIV exclusion share of population, 99 / 147,370. Superseded only as a bound WIDTH",
    19042: "post-liveness started-and-left POINT ESTIMATE on APPLY -- not the bound floor",
    16744: "post-liveness S&L count on 147,271, and the DERIV floor under extreme NONE",
    632: "frozen-D10 never-started component at W = 125",
    703: "adopted APPLY exclusion count",
}
# The two-extremes table: 0055 SS2 asked both arms for the floor under extreme NONE as well
# as extreme ALL, so the NONE column IS 9.6830 / 11.3619 / 73.6537 / 82.4327. Correct where
# labelled as that extreme; superseded wherever it stands as the adopted figure. This is a
# CONTEXT exemption, not a value exemption, and glossary row `16,744` already carries it.
# B6 (Red Team 13): this was a value table whose branch was UNREACHABLE -- the general
# DECLARE regex already contained `extreme[_ ]NONE`, so the value scoping never ran and the
# general branch disarmed the control for values the two-extremes table has nothing to do
# with. DECLARE is now per-value AND per-file, and this is the table it is built from.
#
# Load-bearing only in the verification arms' deliverables, which are the files that carry
# the two-extremes table and are deliberately not on the whole-file allowlist.
DECLARE_SCOPED = {
    "step7-deriv-floor-check": {
        9.6830: r"extreme[_ ]NONE",
        11.3619: r"extreme[_ ]NONE",
        73.6537: r"extreme[_ ]NONE",
        82.4327: r"extreme[_ ]NONE",
    },
}
# Structural markers in a JSON PATH, which is not prose and cannot carry an inline note.
# Applied to json paths only, never to text lines.
DECLARE_JSON_PATH = r"_DERIVED|_scope|superseded_strings|SUPERSEDED_computed_under|_superseded_note"

# WITHDRAWN CLAIMS -- prose, not numbers. Added 2026-08-13 (0061).
#
# B8: a withdrawn sentence was struck in the three places a human had typed it and left in the
# one place a SCRIPT typed it, so the generator wrote it back to all four operative files on
# every run. Both controls were structurally blind: the .md form carries NO NUMBERS, and the
# .json form is a STRING under _DERIVED, which verify() skips by key. A numeric control cannot
# see a withdrawn claim, and this chain withdraws claims as often as it corrects figures.
#
# So the register now holds phrases as well as values. Each is a fragment of a claim that has
# been withdrawn; every occurrence outside a strikethrough or a withdrawal note is a defect.
WITHDRAWN_PHRASES = {
    "can still be a different set of rows": (
        "arm a's symmetric-difference-0 warrant, published as strictly stronger than the "
        "unchanged exclusion total. FALSE on this counterfactual: the perturbation is "
        "monotone, so an unchanged total already forces set equality. Withdrawn 0094 SS2"),
    "reached surface 1 and no other": (
        "arm a's hardcoded propagation reading, published beside live counts that a rerun "
        "can contradict -- and did. Now derived per surface with both halves. Withdrawn 0094 SS1"),

    "which is the proof": (
        "cited the never-started ratio (a 0.2813, b 0.27211) as proof that reconciling the "
        "started-and-left conventions was wrong. FALSE: 0.2813 is 0.307138/1.092, arm b's "
        "convention, so the pair was one convention on two bootstraps. Withdrawn 0060 SS2"),
    "retained in place above and marked superseded": (
        "a hard-coded literal that nothing checked and that was false; replaced by an assertion "
        "in check_ratios_written(). Withdrawn from the JSON half at 0059 and still emitted into "
        "the .md half -- Red Team 14, B10"),
    # H1, reviewer-engineering on v1.6.0. THE EIGHT-SURFACE HALF of the statistic control.
    # scan_statistic_declaration() reads TWO surfaces, and the only defect of this class ever
    # found -- 0119 SS2, analytics-engineer{,-b}.md:583 -- sat in files it does not open, contradicting
    # all four fixed elements while both copies stayed byte-identical. Byte-identity cannot see a
    # claim made OUTSIDE the block or made IDENTICALLY IN BOTH copies; a phrase scan can, on all
    # eight surfaces, with the strikethrough/withdrawal exemption the other phrases already use.
    "the spec fixes none of them": (
        "the bootstrap's three elements declared unfixed. ALL FOUR are fixed and identical for "
        "both arms: B = 10,000, seed 20260818, unit = account (0103), statistic = BOTH levels "
        "and paired movements (0118). Withdrawn 0118, and the instance at "
        "analytics-engineer{,-b}.md:583 found by the arm at 0119 SS2"),
    "levels-vs-movements is still unfixed": (
        "0104's reading, true when written and closed by 0118. Withdrawn 0120"),
    "levels-vs-movements remains unfixed": (
        "same claim in the other tense; both forms were live on different surfaces. "
        "Withdrawn 0120"),
    "statistic (levels vs movements)": (
        "the generator's fields_not_fixed_in_spec entry, v1.5.0. The statistic is FIXED and the "
        "list is empty with its universe declared. Withdrawn 0119 SS1"),

    # F7, reviewer-engineering on v1.8.0: the E6 retirements were withdrawn in the artifacts and
    # registered NOWHERE, so the sentences could be written back onto any of the eight surfaces and
    # nothing would fire. Registering them was blocked until v1.9.0 because the retirement notes
    # QUOTED the sentences without carrying a STRUCK token -- "WAS ALREADY FALSE" is not "was false"
    # and there is no colon after FALSE -- so a registration would have failed three artifacts on
    # their own withdrawal notes. The generator now carries the retired text under a
    # `withdrawn_sentences` key, where THE KEY IS THE MARKER (0094), and the replacing paragraphs
    # no longer quote them. Registered with the arm's live probe behind it, both directions.
    "checks s40 and s41 do not branch on which step wrote the file": (
        "spec choice #29's claim about the controls, FALSIFIED by the v1.7.0 change that made S41 "
        "branch on the producing step for the Step 12 exemption -- and already false when written, "
        "the step-level exemption in the same paragraph being exactly such a branch. Withdrawn 0121"),
    "s40 and s41 gain a producing-step guard": (
        "spec choice #29's if_ruled_otherwise, offering as a COUNTERFACTUAL a remedy that is "
        "half-implemented in the build it ships with. A counterfactual that describes the current "
        "build is not a counterfactual -- the disposition if_ruled_otherwise already took at "
        "v1.6.0 for the same reason. Withdrawn 0121"),

    "everything else in this file stands": (
        "a stamp that affirmatively certified superseded figures. Withdrawn 0056 SS4"),
    "cannot enter the list": (
        "the LIVE_ELSEWHERE mechanism, which never fired. Withdrawn 0059"),
    "unreconciled and now specified": (
        "0052 SS6's claim about the bootstrap spec; it was never specified. Struck 0056 SS8"),
    "means two different things about viewers": (
        "0082 SS2's MOTIVE for p_at_bound: 'a distribution with a spike at 1.0 means two "
        "different things about viewers and the column cannot say which.' FALSE on the adopted "
        "rank form -- set membership puts m_H in E2, so the numerator is L2 iff m_H = max(E2) "
        "= F2, and the two clauses are coextensive by construction. The spike means ONE thing "
        "and the FALSE class is empty. Withdrawn 0083 SS2"),
}

# GROUND WITHDRAWALS -- CLAUDE.md's THIRD BLINDNESS CLASS, which no control sees.
# A withdrawn ARGUMENT built from CORRECT statistics has no superseded number for the numeric
# half and no stable string for the phrase half. The register's obligation (0065 SS3) is to
# name the statistics that remain TRUE but are no longer load-bearing, so a later reader can
# recognise the argument by what it claims.
GROUNDS_WITHDRAWN = {
    # 0100. The two second-brain listed as CANDIDATES and correctly declined to add itself --
    # "extending my human half past the source would be the two-registers defect committed by me."
    # Added HERE, in the single register, which is where they belong.
    "0091 SS1": {
        "argument": "line 6 does not move under the counterfactual BECAUSE the silence test reads "
                    "an insertion clock rather than an episode timestamp",
        "still_true": [703, 99, 55, 45],
        "why_not_load_bearing": "STRUCTURALLY WRONG. The liveness rule is conjunct 1 AND conjunct 2, "
                                "and conjunct 2 is NOT Continued -- an episode-timestamp computation "
                                "that moves on 55 APPLY and 45 DERIV rows under this very "
                                "counterfactual. A property of conjunct 1 cannot explain the "
                                "invariance of the conjunction. The counts are correct and the "
                                "invariance is real; the REASON given for it was not. Withdrawn "
                                "0091 SS1, Red Team sixth pass",
    },
    "0089 SS2a": {
        "argument": "exactly 1 episode falls at tau1, SO 0068's strictness ruling moves a real row",
        "still_true": [1],
        "why_not_load_bearing": "WRONG OBJECT. 0068 is about INSERTION INSTANTS in the silence test; "
                                "the 1 is a distinct S2 episode by canonical watched_at -- a "
                                "different axis. The ruling's own quantity is 0 pairs and 0 accounts "
                                "on both populations, both arms, so 0068's strictness ruling is "
                                "VACUOUS on this data. The 1 is a true count of the wrong thing. "
                                "Withdrawn 0089 SS2(a), Red Team sixth pass",
    },

    "0094 SS2": {
        "argument": "arm a's symmetric-difference-0 published as strictly stronger evidence than "
                    "the unchanged exclusion total -- 'a total that does not move can still be a "
                    "different set of rows, and that is what the symmetric difference rules out'",
        "still_true": [0, 703, 99, 55, 45],
        "why_not_load_bearing": "TRUE of an arbitrary perturbation, FALSE of this one. Relaxing "
                                "either bound only ADDS episodes to A and A_H, and both Continued "
                                "conjuncts are monotone in A_H, so a row can only LEAVE the "
                                "exclusion set and never enter it -- measured: |A| decreased on 0 "
                                "rows, |A_H| on 0, m_H on 0, m_H > F2 on 0, Continued turned off on "
                                "0. An unchanged total therefore ALREADY forces set equality. The "
                                "symmetric difference confirms the arithmetic; it is not "
                                "independent evidence. Withdrawn 0094 SS2, Red Team eighth pass F8",
    },

    "0106 SS7.3": {
        "argument": "the decision log 'disagrees with itself' on arm a's bootstrap seed, "
                    "because 0052 SS122 records 20260813 and 0053 SS107 records 20260815 -- "
                    "therefore arm a's configuration cannot be taken from decisions/",
        "still_true": [20260813, 20260814, 20260815],
        "why_not_load_bearing": "ALL THREE SEEDS ARE CORRECT WHERE THEY APPEAR, and the two "
                                "entries were never in conflict: they label two DIFFERENT RUNS "
                                "and neither says which. 0053 SS107's pair (20260813, 20260815) "
                                "is the mm / ALT-MATCHED run -- mm_a at 4000/20260813, mm_b at "
                                "4000/20260815, both confirmed on disk, and git log -S puts "
                                "20260815's first appearance in fafb443, the same commit that "
                                "created step7-liveness-mm-b.json and 0053 itself. 0052 SS122 / "
                                "0055 SS288 / 0056 SS150 describe the bb / ALT-BROAD gate-closing "
                                "run, where bb_b is 2000/20260814. The real defect is an "
                                "UNLABELLED RUN, not a contradiction. Also withdrawn with it: "
                                "'20260815 appears exactly once in the repository' -- it appears "
                                "8 times. The surviving true claim is that ZERO namespace-a files "
                                "carry it. Withdrawn 0106 SS7.3, verified against disk "
                                "2026-08-18. NOTE: the paired claim at 0116 SS5 -- that "
                                "'A: movements, B: levels' exists in decisions/ and not in arm "
                                "a's deliverable -- STANDS and is unaffected",
    },

    "0055 SS2": {
        "argument": "the widened S&L floor is warranted because the 90 channel pairs had "
                    "full opportunity to produce evidence (p5 margin 1.7 days, minimum 0.13)",
        "still_true": [1.7, 0.13, 1.6552, 44.5272, 44.5],
        "why_not_load_bearing": "cherry-picked the tail -- the same 90 have median 44.5. A "
                                "floor is a worst case; admissibility sets the endpoint and "
                                "plausibility does not enter. The correct ground carries NO "
                                "margin statistic at all",
    },
    "0083 SS2": {
        "argument": "p_at_bound decomposes the p = 1.0 spike, evidenced by the 1,246 and "
                    "1,230 totals 'splitting' into two classes",
        "still_true": [1246, 1230],
        "why_not_load_bearing": "both are correct counts and both arms reproduce them, but "
                                "they are ONE class counted twice, not two classes summed. "
                                "The FALSE class is empty by construction, so the column "
                                "separates nothing on any data the adopted rank form admits. "
                                "Citing the totals as separation evidence is the withdrawn "
                                "argument; citing them as p = 1.0 TOTALS is correct",
        "CAUTION_TWO_FALSE_CLASSES": (
            "0099, found by second-brain. The phrase 'the FALSE class is empty' is SAFE only "
            "for CLASS 1, the coextensivity gap, which is 0 on all four populations. CLASS 2 is "
            "the COLUMN's own FALSE value and is 17,895 / 17,812 / 15,771 / 15,688. Step 8b is "
            "unblocked and is exactly the consumer: a reader who takes the unqualified sentence "
            "and provisions a two-valued column is wrong by 17,895 rows on APPLY position 5. "
            "Never restate this sentence without naming which class."),
},
}

# ============================================================================
# SUPERSEDED STRING NEEDLES -- the TEXTUAL half, for propagation SURFACE 6.
#
# Added 2026-08-16 by analytics-engineer-b, on Red Team's eighth pass, F2.
#
# THIS EXISTS HERE AND NOT IN AN ARM'S SCRIPT BECAUSE CLAUDE.md SAYS SO:
# "One register, in src/step7_register.py, imported by every script that
# checks. Two hand-maintained copies diverged by an entry after a single use,
# and neither held the values that were wrong."
# The -r6 build of step8_b_4_artifacts.py held a SECOND hand-maintained
# register of exactly this kind in its own module, which is the arrangement
# that rule was written against. It now imports these.
#
# AND THE MATCHING IS CASE-INSENSITIVE, which is the defect that occasioned
# the move. The -r6 register's needle was the lower-case `six of eight`; the
# string actually present in that arm's deliverables, three times, is
# `six of EIGHT`. The one needle written against the very defect that
# motivated the control could not see it, and its hits table showed no row
# for that needle at all -- indistinguishable from a clean pass.
#
# Each row is (needle, what it is, what replaces it).
SUPERSEDED_STRINGS = [
    ("six of eight", "the pre-0088 assertion-set count in prose",
     "the count derived from len(inv) and the label field"),
    ("of eight cannot fail", "the pre-0088 assertion-set count in prose",
     "N of 9, derived"),
    ("assertion set now has eight", "the pre-0088 assertion-set count",
     "NINE (0088 Sec 1c)"),
    ("seven of the nine", "the self-contradicting cannot-fail count",
     "six cannot fail; three can fail as specified"),
    ("even though strict is ruled", "0074 ruling 5's framing",
     "0090 -- strict is the floor of a published bound"),
    ("strict is ruled", "0074 ruling 5's framing",
     "0090 -- strict is the floor of a published bound"),
    ("the ruled key is strict", "0074 ruling 5's framing", "0090 -- a bound"),
    ("88 columns", "the pre-0082 column count", "89 names, enumerated"),
    ("97.6%", "the position-3 censoring share (0033)", "97.40% on position 4 (0070 r8)"),
    ("793", "ALT-MATCHED's withdrawn liveness answer", "703 on APPLY"),
    ("1,293", "a deleted liveness threshold (0042)", "the rule is parameter-free"),
    ("95.98%", "D3prime on the uncensored estimation sample (0034)",
     "99.53% on Step 8's right-censored APPLY (0075)"),
    ("91.34%", "D3prime on the uncensored estimation sample (0034)",
     "97.73% at W = 213 on APPLY (0075)"),
    # Red Team eighth pass, F1 -- 0089 Sec 2(b) corrected 0088 Sec 2(b)'s AXIS,
    # and one arm republished the superseded characterisation for two entries
    # while its own table contradicted it six lines below. 747,478 is a PAIR
    # count, not a season-coverage ROW count.
    ("747,478 and 726,103 are different objects",
     "0088 Sec 2(b)'s characterisation, corrected by 0089 Sec 2(b)",
     "747,478 is DISTINCT (user, show) PAIRS; the axis was wrong, not the conclusion"),
]
# A SUBSTRING NEEDLE CANNOT EXPRESS THE 747,478 DEFECT ON ITS OWN.
# The superseded claim is an ATTRIBUTION -- "747,478 is a season-coverage ROW
# count" -- and it survives any rewording, any markdown emphasis inside the
# sentence, and any reordering. A needle for one phrasing would sit at zero
# forever while the claim reappeared in another. So the substring needle above
# covers the exact -r6 sentence, and the ATTRIBUTION is covered by a line-local
# co-occurrence control asserted by the importing script:
#
#   every line containing `747,478` must EITHER be marked as superseded OR
#   characterise the figure as PAIRS -- never as rows.
#
# Named here so the register states what covers the defect, per CLAUDE.md's
# rule that a withdrawn or unexpressible needle names the stronger control.
SURFACE6_LINE_LOCAL_CONTROLS = {
    "747478_is_a_PAIR_count_not_a_ROW_count": {
        "rule": ("every line mentioning 747,478 must be marked as superseded, or must "
                 "characterise it as distinct (user, show) PAIRS. A line calling it "
                 "season-coverage ROWS, or mentioning it with no characterisation at all, "
                 "fails"),
        "ruling": "decisions/0089 Sec 2(b), correcting 0088 Sec 2(b)'s axis",
        "why_not_a_needle": ("the defect is an ATTRIBUTION, not a phrasing. A substring needle "
                             "covers one wording and sits at zero while the claim returns in "
                             "another"),
        "needle": "747,478",
        "must_contain_one_of": ("pair", "pairs"),
        "must_not_contain": ("season-coverage row", "season coverage row", "coverage rows"),
    },
}

# Needles TRIED AND WITHDRAWN. CLAUDE.md: "Registering a string as a false
# positive disarms the control against it. Do it only when the legitimate
# reading is verified live under the ADOPTED rule, and withdraw the row the
# moment it stops being." So each names the STRONGER control that covers it,
# and the importing script asserts that control live rather than citing it.
NEEDLES_WITHDRAWN = {
    "f2_in_A_H": {
        "why_it_fired": ("every occurrence in Step 8's artifacts is a line EXPLAINING that the "
                         "column is dropped as derivable -- which the spec requires be stated. "
                         "The string is supposed to be present"),
        "covered_instead_by": ("a SET assertion on the emitted table: "
                               "`assert set(tab.columns) == set(COLUMNS_89)`, plus the "
                               "emitted-order check. 0077's own words: 'Matching a count is not "
                               "matching a set -- assert on the names.' A name assertion is "
                               "strictly stronger than a substring grep"),
        "verified_live_this_run": "column_set_is_asserted_on_NAMES_not_on_a_count",
    },
    "thetwilightzone": {
        "why_it_fired": ("the U3 cluster list is EMITTED ON PURPOSE, beside U1 and U2, so an arm "
                         "on another universe is diffable without a rerun. 0088 Sec 3 supersedes "
                         "it as THE ILLUSTRATION, not as a measurement"),
        "covered_instead_by": ("an assertion that the PUBLISHED illustration is U1's ranked list "
                               "and that its universe and ranking basis are named at the point "
                               "of use. A line-local string test cannot express 'which list is "
                               "the illustration', which is what 0088 Sec 3 rules"),
        "verified_live_this_run": "ruled_illustration_is_U1",
    },
}

# A hit is LEGITIMATE if its line names the string as superseded, withdrawn,
# corrected, struck, or attributes it to a previous build -- CLAUDE.md's "a grep
# hit is not a defect until you read the line", and "except where a string is
# explicitly named as superseded at the point of use".
#
# COMPARED CASE-INSENSITIVELY, like the needles. The marker list previously held
# both cases of several words for that reason; the duplicates are gone because
# the comparison, not the list, is what handles case.
SURFACE6_MARKERS = (
    "superseded", "supersede", "withdrawn", "~~", "-r4", "-r5", "-r6",
    "r4 build", "r5 build", "r6 build", "r4 claim", "r4_claim", "struck",
    "corrected", "no longer true", "no longer", "previous build",
    "was measured on the wrong", "another universe's answer", "dropped",
    "not produced", "not an endpoint", "deleted", "never produced", "red team",
    "defect", "replaces", "former", "pre-", "old ", "this arm's own defect",
)


def surface6_needle_count(line, needle):
    """Count occurrences of `needle` in `line`, CASE-INSENSITIVELY, with a digit
    boundary on numeric needles.

    The digit boundary was found by this control on its own first run: `793`
    matched inside `"retained_pct": 95.86793198892843`. CLAUDE.md records the
    general shape -- textual grep cannot see the JSONs, which is why the study's
    numeric control matches numerically at a tolerance. This is the textual
    half's minimum defence. It NARROWS THE MATCH RULE and disarms no string.
    """
    low, nd = line.lower(), needle.lower()
    n = low.count(nd)
    if not n or not nd[0].isdigit():
        return n
    kept, start = 0, 0
    while True:
        j = low.find(nd, start)
        if j < 0:
            return kept
        before = low[j - 1] if j else ""
        after = low[j + len(nd)] if j + len(nd) < len(low) else ""
        if not (before.isdigit() or before == "." or after.isdigit()):
            kept += 1
        start = j + 1


def surface6_line_is_marked(line):
    """True if the line names its own string as superseded, case-insensitively."""
    low = line.lower()
    return any(mk in low for mk in SURFACE6_MARKERS)


# KNOWN LIMIT, recorded 2026-08-13 (0060), found by Red Team on review 13.
# Both controls walk NUMERIC LEAVES only. A superseded figure written inside a JSON STRING
# -- a narrative field, a note, an estimand description -- is invisible to json_numbers()
# and to verify().
#
# AMENDED 2026-08-13 (0061): this was recorded as "not a defect today". It was ALREADY a defect
# on the day it was recorded -- B8 was live in a .json string under _DERIVED and in .md prose
# carrying no numbers, in all four operative deliverables, at the moment the limit was written
# down as hypothetical. Recording a gap as harmless is not the same as checking whether it is.
#
# PARTIALLY CLOSED: WITHDRAWN_PHRASES above is checked against .md text AND against JSON string
# values. Still open: a superseded NUMBER inside a JSON string is invisible to the numeric half.
JSON_STRING_FIELDS_ARE_NOT_NUMERICALLY_CHECKED = True

# ----------------------------------------------------- wholly superseded, one line each
WHOLLY_SUPERSEDED_FILES = {
    # 0097, Red Team eleventh pass F1. Historical read-backs of 2026-08-14 with NO producing
    # pipeline, so 0092 cannot correct them by rerunning an arm. FOUR statements in them expired:
    # seven-vs-eight propagation surfaces, adopted_rule.json's pre-0074 figures, Step 7's
    # pre-approval header, and Step 0's pre-amendment 403 rule. Stale STATEMENTS built from
    # once-true readings -- the third blindness class, invisible to every numeric and phrase half,
    # which is why eleven passes did not catch them. Named here because CLAUDE.md requires a
    # wholly superseded file be exempted BY NAME with a reason; the head stamp declares status and
    # does not exempt.
    "step8-readback-a": "historical read-back of 2026-08-14; four statements expired, named in its stamp (0097)",
    "step8-readback-b": "historical read-back of 2026-08-14; four statements expired, named in its stamp (0097)",

    "step7-liveness-mm-a": "the REVERTED ALT-MATCHED rule (0052, reverted 0054); retained as its record",
    "step7-liveness-mm-b": "the REVERTED ALT-MATCHED rule; retained as its record",
    "step7-liveness-alt-a": "the ALT rule, superseded by ALT-BROAD (0048)",
    "step7-liveness-alt-b": "the ALT rule, superseded by ALT-BROAD (0048)",
    "step7-alt-rule-a": "the ALT rule proposal generation",
    "step7-alt-rule-b": "the ALT rule proposal generation",
    "step7-sensitivity-a": "sensitivity run against the DELETED numeric threshold (0042)",
    "step7-sensitivity-b": "sensitivity run against the DELETED numeric threshold (0042)",
    **{f"step7-liveness-{a}{n}": "a pre-ALT-BROAD rule generation (PF-LIMIT / thresholded)"
       for a in "ab" for n in ("", "2", "3", "4")},
}

# Files whose every number is superseded BY PURPOSE, not by generation.
BY_PURPOSE = {
    "withdrawn-claims-register": "its entire content is claims that were withdrawn",
}

# Surface 8 (0074). processed/ holds two different kinds of thing and they need different treatment.
#
#   - PER-ARM WORKING OUTPUT. processed/step7/<ns>/ is what one instance computed under the rule
#     generation it ran. Those figures are the RECORD of that run and are superseded by definition,
#     exactly like the stamped artifacts. Allowlisted by name, with the arm and reason.
#   - SPEC-BEARING METADATA. adopted_rule.json and its kind state what the APPROVED rule is, and an
#     implementation reads them. Those are NOT exemptible -- that is the whole reason surface 8 exists.
PROCESSED_WORKING_DIRS = {
    "processed/step7/bb_a/": "arm a's ALT-BROAD working output -- the record of that run",
    "processed/step7/bb_b/": "arm b's ALT-BROAD working output -- the record of that run",
    "processed/step7/mm_a/": "arm a's REVERTED ALT-MATCHED working output",
    "processed/step7/mm_b/": "arm b's REVERTED ALT-MATCHED working output",
    "processed/step7/alt_a/": "the superseded ALT rule's working output",
    "processed/step7/alt_b/": "the superseded ALT rule's working output",
    "processed/step7/df_a/": "arm a's DERIV-floor verification -- the two-extremes table by design",
    "processed/step7/df_b/": "arm b's DERIV-floor verification -- the two-extremes table by design",
    "processed/step7/query/": "one-off measurement outputs, including the two-extremes table",
}
# NOT exemptible on surface 8, in code rather than by remembering: the files that state the rule.
PROCESSED_NEVER_EXEMPT = ("adopted_rule.json",)


def processed_is_working_output(path):
    p = str(path)
    if any(n in p for n in PROCESSED_NEVER_EXEMPT):
        return None
    for frag, why in PROCESSED_WORKING_DIRS.items():
        if frag in p:
            return why
    return None

# NOT exempt, deliberately: step7-liveness-bb-{a,b}.{md,json} are the OPERATIVE deliverables
# and are only PARTIALLY superseded. Exempting them in whole is what let a wrong ratio pass.
OPERATIVE = ("step7-liveness-bb-a", "step7-liveness-bb-b")


def file_is_wholly_superseded(path):
    name = str(path)
    if any(o in name for o in OPERATIVE):
        return None
    for key, why in {**WHOLLY_SUPERSEDED_FILES, **BY_PURPOSE}.items():
        if key in name:
            return why
    return None


def scoped(table, path, value, tol=5e-5):
    """Return the reason if (file, value) is in a scoped table."""
    for (frag, v), why in table.items():
        if frag in str(path) and abs(float(value) - v) < tol:
            return why
    return None
