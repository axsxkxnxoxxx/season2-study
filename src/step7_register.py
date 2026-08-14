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
    ("bb-a", 0.5304): "arm a, APPLY: 0.403246 / 0.7602, its own floor-endpoint CI",
    ("bb-a", 0.1309): "arm a, DERIV: 0.127570 / 0.9744",
    ("bb-b", 0.5090): "arm b, APPLY: 0.403246 / 0.7922, the under-the-rule point estimate's CI",
    ("bb-b", 0.1310): "arm b, DERIV: 0.127570 / 0.9737",
}

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
EXTREME_NONE_READINGS = {9.6830, 11.3619, 73.6537, 82.4327}

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
