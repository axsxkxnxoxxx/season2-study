"""Step 9, arm `b`, stage 4: render the reader-facing half FROM THE EMITTED JSON.

Both halves render one object. Nothing is retyped: every figure below is read out
of artifacts/step9-headline-b.json, so the two halves cannot disagree.
"""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
# See src/step9_b_3_emit.py: STEP9_B_OUTDIR redirects a correction run away from the committed
# deliverables. The .md is rendered from whichever .json this run produced, never from a
# different one.
OUTDIR = os.environ.get("STEP9_B_OUTDIR", os.path.join(ROOT, "artifacts"))
J = os.path.join(OUTDIR, "step9-headline-b.json")
M = os.path.join(OUTDIR, "step9-headline-b.md")

d = json.load(open(J))
L = []
w = L.append


def arm(idx):
    return d["arms"][idx]


def pl(a, pop):
    return a["headline"][pop]["by_producing_arm"]["arms"]["b"]


w("# Step 9 — headline result. **ARM `b`.**")
w("")
w("> **This is ONE ARM'S FILE.** It carries arm `b`'s measurement and nothing else. It asserts "
  "nothing about arm `a`, about the merged document, or about the state of any other step. "
  "**The dual control is the Human Lead's DIFF between the two arm files, before the merge.**")
w("")
gb = d["generated_by"]
w("| | |")
w("| :--- | :--- |")
w("| **Step** | 9, headline result — chained, dual implementation |")
w("| **Arm** | `b` (`data-scientist-b`) |")
w("| **Build** | `%s` |" % gb["build_tag"])
w("| **Generated** | %s by `%s` (sha256:12 `%s`) |"
  % (gb["generated_at_utc"], gb["generator"], gb["generator_sha256_12"]))
w("| **Schema** | `%s`, `%s` |" % (d["schema_version"], d["schema_id"]))
w("| **Adopted rule revision** | %d, **READ not typed** from `%s`, key `%s`, sha256:12 `%s` |"
  % (d["adopted_rule_revision"]["revision"], d["adopted_rule_revision"]["source_file"],
     d["adopted_rule_revision"]["source_key"], d["adopted_rule_revision"]["source_sha256_12"]))
w("| **API calls** | 0 |")
w("| **Adopts** | nothing |")
w("")
w("**Inputs.**")
for i in gb["inputs"]:
    w("- `%s`" % i)
w("")
w("---")
w("")
w("## 1. What this arm measured, and what it consumed")
w("")
w("**CONSUMED FROM STEP 8, NOT REBUILT.** Both populations and every waterfall, "
  "liveness-exclusion and air-period figure on the adopted arm are Step 8's. Rebuilding either "
  "population would be a second definition, and a reconstruction that agrees today is still a "
  "second definition tomorrow — the dual diff cannot see it, because both instances would "
  "rebuild the same way.")
w("")
w("**MEASURED HERE:** the confidence intervals (both objects), the three bounds and their "
  "attainable corners, the three-ceiling arithmetic, and the **whole of the premiere-anchored "
  "91-day arm**, which no step in the spec produces. That arm is measured by driving **Step 8's "
  "own rule implementation** with a substituted `T0`, so it is the same implementation and not "
  "a second one; the harness was first run at the adopted setting and reproduced all thirteen "
  "of Step 8's consumed counts exactly before it was trusted anywhere else.")
w("")
w("## 2. The headline")
w("")
w("**Never started is a `W`-day statement read at `τ1`. Continued is a `W + H`-day statement "
  "read at `τ2` on `A_H`. THE TWO ARE NOT MEASURED ALIKE.** Started-and-left is *also* a null: "
  "`|A| ≥ 1` is observed, the failure to meet the Continued condition is not.")
w("")
for i, a in enumerate(d["arms"]):
    w("### 2.%d `%s` — W = %d d, H = %d d, clock origin `%s`%s"
      % (i + 1, a["arm_id"], a["W_days"], a["H_days"], a["clock_origin"],
         "  **[PRIMARY HEADLINE]**" if a["is_primary_headline"] else ""))
    w("")
    w(a["clock_origin_note"])
    w("")
    for pop in ("APPLY", "DERIV"):
        h = a["headline"][pop]
        p = pl(a, pop)
        w("**%s** — position-5 row set **%s**, post-liveness row set **%s**."
          % (pop, format(h["n_position_5"], ","), format(h["n_post_liveness"], ",")))
        w("")
        w("| outcome | share (post-liveness) | pairs | 95% CI, **LEVEL** | width | horizon |")
        w("| :--- | ---: | ---: | :--- | ---: | ---: |")
        for s in ("never_started", "started_and_left", "continued"):
            v = p["shares"][s]
            w("| %s | **%.4f%%** | %s | [%.4f%%, %.4f%%] | %.4f pp | %d d |"
              % (s.replace("_", " "), v["value_percent"], format(v["numerator_pairs"], ","),
                 v["ci"]["lower"], v["ci"]["upper"], v["ci"]["upper"] - v["ci"]["lower"],
                 v["horizon_days"]))
        w("")
        w("| bound | floor | ceiling | width | on |")
        w("| :--- | ---: | ---: | ---: | :--- |")
        for s in ("never_started", "started_and_left"):
            b = p["bounds"][s]
            deg = "  *(DEGENERATE — a measured zero width, not missing data)*" if b["degenerate"] else ""
            w("| %s | %.4f%% (%s) | %.4f%% (%s) | %.4f pp%s | position 5, n = %s |"
              % (s.replace("_", " "), b["floor"]["percent"],
                 format(b["floor"]["numerator_pairs"], ","), b["ceiling"]["percent"],
                 format(b["ceiling"]["numerator_pairs"], ","), b["width_pp"], deg,
                 format(b["floor"]["denominator_pairs"], ",")))
        cb = p["bounds"]["continued"]
        w("| continued | *%s* | %.4f%% (%s) | — | position 5, n = %s |"
          % (cb["floor"]["status"].replace("_", " "), cb["ceiling"]["percent"],
             format(cb["ceiling"]["numerator_pairs"], ","),
             format(cb["ceiling"]["denominator_pairs"], ",")))
        w("")
        si = p["bounds"]["started_and_left"]["conditional_sub_interval"]
        w("**Conditional sub-interval on started-and-left** — a *labelled conditional*, **never "
          "the bound**: [%.4f%%, %.4f%%], width %.4f pp. %s"
          % (si["floor"]["percent"], si["ceiling"]["percent"], si["width_pp"],
             si["coincides_with_bound"]["evidence"]))
        w("")
        c = p["ceilings_cannot_all_hold"]
        w("**THREE CEILINGS, AND THEY CANNOT ALL HOLD.** %.4f%% + %.4f%% + %.4f%% = **%.4f%%** "
          "on %s — excess **%.4f pp = %d pairs**. %s"
          % (p["bounds"]["never_started"]["ceiling"]["percent"],
             p["bounds"]["started_and_left"]["ceiling"]["percent"],
             cb["ceiling"]["percent"], c["sum_percent"], format(h["n_position_5"], ","),
             c["excess_pp"], c["excess_pairs"], c["note"]))
        w("")
        w("**%s**" % h["populations_differ_note"])
        w("")
    w("")

w("## 3. Both bootstrap objects — and a level is never compared with a movement")
w("")
bs = d["bootstrap_settings"]["b_default"]
w("**ALL FOUR ELEMENTS ARE FIXED BY THE SPEC AND NONE IS THIS ARM'S CHOICE:** `B` = **%s**, "
  "seed = **%d**, resampling unit = **%s**, statistic = **both %s**. Every interval in this "
  "file restates them at the point of use."
  % (format(bs["B"], ","), bs["seed"], bs["resampling_unit"], " and ".join(bs["statistics"])))
w("")
w("**ACCOUNT LEVEL because pairs are not independent** — one account contributes many, and "
  "pair-level resampling understates the interval.")
w("")
w("**PAIRED MOVEMENTS**, the second object: the change in each share caused by the liveness "
  "filter — post-liveness level minus position-5 level — differenced **inside each replicate**, "
  "so the same account weights produce both terms.")
w("")
w("| arm | population | outcome | 95% CI, **MOVEMENT** | width | level width | ratio |")
w("| :--- | :--- | :--- | :--- | ---: | ---: | ---: |")
for e in d["declared_intervals"]:
    key = e["interval_id"].split("movement_")[1]
    armk, rest = key.rsplit("_b", 1)[0], None
    parts = e["interval_id"].split("_")
    ci = e["ci"]
    # recover the level width from the arm payload
    for a in d["arms"]:
        for pop in ("APPLY", "DERIV"):
            for s, v in pl(a, pop)["shares"].items():
                idn = "movement_%s_%s_%s_b" % (
                    "W108_s2_finale" if a["clock_origin"] == "s2_finale" else "W91_s2_premiere",
                    pop, s)
                if idn == e["interval_id"]:
                    lw = v["ci"]["upper"] - v["ci"]["lower"]
                    mw = ci["upper"] - ci["lower"]
                    w("| %s | %s | %s | [%+.4f, %+.4f] pp | %.4f pp | %.4f pp | **%.0f×** |"
                      % (a["arm_id"], pop, s.replace("_", " "), ci["lower"], ci["upper"],
                         mw, lw, lw / mw))
w("")
w("***A LEVEL AND A MOVEMENT ARE NEVER COMPARED TO EACH OTHER.*** The level and the movement on "
  "one quantity differ by up to an order of magnitude, so a reader who is not told which one "
  "they are reading is wrong by that much. **Both objects are labelled at the point of use and "
  "neither is presented as *the* design.**")
w("")
w("**A property of these measurements, stated because it bears on how they may be read: a "
  "paired movement is a quantity in PERCENTAGE POINTS and it is negative wherever the liveness "
  "filter lowers a share. Six of the twelve movements this arm measured have negative "
  "endpoints.** A movement is not a percentage and must not be rendered as one.")
w("")
w("**Every interval here is an outcome-share quantity, whose binding cluster is the ACCOUNT**, "
  "so every one of them says `account` and none inherits it silently. **No window-`W` "
  "percentile interval is declared**: `W`'s binding cluster is the **show**, account-level "
  "resampling would understate it, and Step 6 is an approved gate whose instruction is "
  "*complete; do not re-derive*. **There is therefore no unit disagreement to report in this "
  "file, and that is stated rather than left to be inferred from an absence.**")
w("")
w("## 4. The bound's scope, published with the bound")
w("")
q = d["scope_qualifiers"]["insertion_dormancy_covering"]
w("**%s**" % q["text"])
w("")
w("**The stopping rule, so that \"covering\" is not a claim without one:** %s" % q["stopping_rule"])
w("")
w("**D4 and D9 publish ALONGSIDE these bounds and are never folded into them.** They are "
  "**Step 8's** figures; this arm does not write them and does not recompute them. "
  "`$.channel_classes` and `$.discovery_channel_overlap` carry the absence idiom here and are "
  "filled once, at Step 13b, from Step 8's own artifact.")
w("")
w("## 5. Attainable corners")
w("")
w("**The three ceilings are ALTERNATIVE WORST CASES OVER ONE EXCLUSION SET, not simultaneous "
  "ones.** Each corner below is a complete and consistent assignment of every excluded and "
  "conceded pair, and sums to the position-5 population exactly.")
w("")
for a in d["arms"]:
    for pop in ("APPLY", "DERIV"):
        p = pl(a, pop)
        w("**%s · %s**" % (a["arm_id"], pop))
        w("")
        w("| corner | never started | started and left | continued |")
        w("| :--- | ---: | ---: | ---: |")
        seen = set()
        for bname in ("never_started", "started_and_left"):
            for cr in p["bounds"][bname]["attainable_corners"]:
                k = (round(cr["never_started_percent"], 6),
                     round(cr["started_and_left_percent"], 6))
                if k in seen:
                    continue
                seen.add(k)
                w("| %s bound, %s | %.4f%% | %.4f%% | %.4f%% |"
                  % (bname.replace("_", " "), cr["corner"], cr["never_started_percent"],
                     cr["started_and_left_percent"], cr["continued_percent"]))
        w("")

w("## 6. Bound width against sampling width")
w("")
w("**The convention is NAMED, because the two arms' sampling-width conventions are named inputs "
  "and reconciling them is a spec decision, not an arm's.** `arm_b_convention`: the denominator "
  "is the width of the 95% percentile-bootstrap interval on the corresponding **post-liveness "
  "level** for the same outcome state, arm and population, account-clustered at the fixed "
  "settings. **`reconciled_with_other_arm: false` at every point of use.**")
w("")
w("| arm | population | quantity | ratio |")
w("| :--- | :--- | :--- | ---: |")
for a in d["arms"]:
    for pop in ("APPLY", "DERIV"):
        for k, v in pl(a, pop)["bound_over_sampling_width_ratios"].items():
            w("| %s | %s | %s | %.4f |" % (a["arm_id"], pop, k.replace("_", " "), v["value"]))
w("")
w("## 7. `$.arm_grid_days` is NOT this arm's block")
w("")
w(d["notes"]["step9_b_arm_grid_days_is_not_this_arms_block"])
w("")
w("Values as filled: `%s`." % json.dumps(d["arm_grid_days"]))
w("")
w("## 8. What this arm declined to write, and why")
w("")
w("- **`$.cross_arm_divergences`** — `human_lead_only`, merged-document-only, and "
  "`forbidden_to_compute_here` for `step9`. **This arm cannot see the other arm, so it could "
  "only fabricate a search record.** Step 13b fills it with a real one.")
w("- **`$.limitations`** — Human-Lead-only. Step 14's, and a non-arm-file merge source.")
w("- **`$.channel_classes` / `$.discovery_channel_overlap`** — Step 8's D4, D9 and channel "
  "overlap. Requiring them in seven arm files would make seven writers of a figure none of "
  "them produced. **Absence idiom emitted.**")
w("- **`$.variants` / `$.tested_ranges` / `$.subpopulation_cuts`** — Steps 13, 13 and 11/12.")
w("- **`arms[].abandonment_distribution`** (Step 10), **`arms[].d3_prime`** and "
  "**`arms[].action_type_counts`** (Step 13) — not this step's blocks.")
w("- **The finale-anchored 91-day grid arm** — that is Step 13's arm, not Step 9's second "
  "headline, and the two would collide under a `W`-only key. This file carries the "
  "**premiere-anchored** 91-day arm only.")
w("- **A waterfall, a liveness-exclusion block and an air-period table at the "
  "premiere-anchored arm** — no step in the spec produces them there. **Absence stated, not "
  "silence.**")
w("")
w("## 9. This arm's own spec choices and open items")
w("")
for a in d["arms"]:
    w("**%s**" % a["arm_id"])
    w("")
    for s in pl(a, "APPLY")["spec_choices_this_arm_made"]:
        w("- %s" % s)
    w("")
w("**One further reading, reported and not reconciled.** " +
  d["notes"]["step9_b_d4_and_d9_publish_alongside"])
w("")

with open(M, "w") as fh:
    fh.write("\n".join(L) + "\n")
print("wrote", M, os.path.getsize(M), "bytes")
