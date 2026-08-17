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
