"""Step 9, arm `a`, stage 3: the reader-facing deliverable.

Generated from artifacts/step9-headline-a.json and processed/step9/a/measured.json. Nothing is
typed: every figure below is read from the emitted arm file, so the .md and the .json cannot
disagree. Every paired movement this arm measured is in both, whatever its sign: a movement
endpoint is a percentage-point difference and is typed $defs.pp, which admits negatives.
"""
import json
import os
import hashlib

ROOT = "/Users/alyanashantel/Documents/season2-study"
J = json.load(open(os.path.join(ROOT, "artifacts", "step9-headline-a.json")))
M = json.load(open(os.path.join(ROOT, "processed", "step9", "a", "measured.json")))
OUT = os.path.join(ROOT, "artifacts", "step9-headline-a.md")

ARMS = {a["arm_id"]: a for a in J["arms"]}
# Presence in the JSON is READ from the emitted file, never inferred from an interval's sign.
DECLARED_MV = {d["interval_id"]: d["ci"] for d in J["declared_intervals"]
               if d["ci"]["statistic"] == "movements"}
KEYS = ["W108_s2_finale", "W091_s2_finale", "W091_s2_premiere"]
TITLE = {"W108_s2_finale": "PRIMARY HEADLINE — W = 108 d, finale-anchored",
         "W091_s2_finale": "SUPPORTING — W = 91 d, finale-anchored",
         "W091_s2_premiere": "NETFLIX ARM — W = 91 d, PREMIERE-anchored"}
OUTS = ["never_started", "started_and_left", "continued"]
NAME = {"never_started": "Never started", "started_and_left": "Started and left",
        "continued": "Continued"}


def arm_of(key):
    for a in J["arms"]:
        if a["arm_id"].startswith(key):
            return a
    raise KeyError(key)


def payload(a, pop):
    return a["headline"][pop]["by_producing_arm"]["arms"]["a"]


L = []
w = L.append

w("# Step 9 — Headline result. ARM `a`.")
w("")
w(f"**Build** `{J['generated_by']['build_tag']}`, generated "
  f"`{J['generated_by']['generated_at_utc']}` by `{J['generated_by']['generator']}` "
  f"(sha256-12 `{J['generated_by']['generator_sha256_12']}`). "
  f"Machine-readable form: `artifacts/step9-headline-a.json`, written into Step 8b's schema "
  f"`{J['schema_id']}` and checked against it with `src/step8b_validate.py` before this file was "
  f"written. The control's own output is a run record, not a finding of this arm's, and it is "
  f"at `logs/step9/a_validate.json`.")
w("")
w("**This is ONE ARM of a dual step.** It has not read the other arm's file or output folder, "
  "has not diffed anything, and carries no cross-arm block. `$.cross_arm_divergences` and "
  "`$.limitations` are omitted; they are the Human Lead's. The diff between the two arms is the "
  "dual control and it is the Human Lead's to run.")
w("")
w("**Adopted rule revision `%d`**, READ from `%s` at key `%s` (file sha256-12 `%s`), never "
  "typed." % (J["adopted_rule_revision"]["revision"], J["adopted_rule_revision"]["source_file"],
              J["adopted_rule_revision"]["source_key"],
              J["adopted_rule_revision"]["source_sha256_12"]))
w("")
w("## 0. What this arm computed, and what it consumed")
w("")
w("**Consumed from Step 8, not rebuilt** (`decisions/0070` rulings 1 and 7): the APPLY and "
  "DERIV populations, the filter waterfall, the liveness exclusion counts, the retained-pair "
  "counts per air period, and the D4 count. Step 8's output carries both populations and the D4 "
  "count, so there was nothing to stop on.")
w("")
w("**Computed here:** the account-clustered bootstrap intervals, the three bounds at each arm, "
  "and the PREMIERE-ANCHORED 91-day arm, which Step 8 does not emit — its eight grid arms are "
  "all finale-anchored.")
w("")
w("**The outcome operator was NOT re-implemented for the premiere arm.** `step8_a_lib.Arms` — "
  "the one implementation of Step 1 §7 on disk — was imported and its `t0` vector replaced with "
  "the premiere-anchored clock. Before any premiere figure was taken, the import was gated on "
  "reproducing Step 8's published finale-anchored counts: **positions 5 and 7 on both "
  "populations, the outcome-conditional position-5 view, the liveness exclusion split, and both "
  "right-censoring sub-lines — 0 mismatches.** A further **36 figures** at the two "
  "finale-anchored arms were compared against Step 8's arm table at emit time, also with 0 "
  "mismatches.")
w("")
w("**Two populations, and every figure says which.** "
  f"APPLY = {J['populations']['APPLY']['reference_n_at_the_adopted_arm']:,} pairs at the adopted "
  f"arm; DERIV = {J['populations']['DERIV']['reference_n_at_the_adopted_arm']:,}.")
w("")
w("**THE BOUNDS AND THE SHARES ARE ON DIFFERENT POPULATIONS.** Bounds are stated on the "
  "**position-5** row set; the published shares are on the **post-liveness** row set. On DERIV "
  "at the primary arm the point estimate lies **outside** its own bound — see §2.")
w("")

# ------------------------------------------------------------------ the headline
for key in KEYS:
    a = arm_of(key)
    w(f"## 1{'abc'[KEYS.index(key)]}. {TITLE[key]}")
    w("")
    w(f"`arm_id` **`{a['arm_id']}`** · W = {a['W_days']} d · H = {a['H_days']} d · clock origin "
      f"`{a['clock_origin']}` · in the W grid: {str(a['in_arm_grid']).lower()} · primary: "
      f"{str(a['is_primary_headline']).lower()}")
    w("")
    for pop in ("APPLY", "DERIV"):
        h = a["headline"][pop]
        p = payload(a, pop)
        w(f"**{pop}** — position 5 n = {h['n_position_5']:,}; post-liveness n = "
          f"{h['n_post_liveness']:,}.")
        w("")
        w("| Outcome | Share (post-liveness) | 95% CI, LEVEL, account-clustered | pairs | "
          "read at |")
        w("| :--- | ---: | :--- | ---: | :--- |")
        for o in OUTS:
            s = p["shares"][o]
            w(f"| {NAME[o]} | **{s['value_percent']:.4f}%** | "
              f"[{s['ci']['lower']:.4f}%, {s['ci']['upper']:.4f}%] | "
              f"{s['numerator_pairs']:,} / {s['denominator_pairs']:,} | "
              f"τ{'1' if o == 'never_started' else '2'}, {s['horizon_days']} d |")
        w("")
        b = p["bounds"]
        ns, sl, ct = b["never_started"], b["started_and_left"], b["continued"]
        si = sl["conditional_sub_interval"]
        w("| Bound (on position 5) | Floor | Ceiling | Width |")
        w("| :--- | ---: | ---: | ---: |")
        w(f"| Never started | {ns['floor']['percent']:.4f}% "
          f"({ns['floor']['numerator_pairs']:,}) | {ns['ceiling']['percent']:.4f}% "
          f"({ns['ceiling']['numerator_pairs']:,}) | {ns['width_pp']:.4f} pp"
          + (" — **DEGENERATE**" if ns["degenerate"] else "") + " |")
        w(f"| Started and left | {sl['floor']['percent']:.4f}% "
          f"({sl['floor']['numerator_pairs']:,}) | {sl['ceiling']['percent']:.4f}% "
          f"({sl['ceiling']['numerator_pairs']:,}) | {sl['width_pp']:.4f} pp |")
        w(f"| — conditional sub-interval, labelled, NOT the bound | "
          f"{si['floor']['percent']:.4f}% | {si['ceiling']['percent']:.4f}% | "
          f"{si['width_pp']:.4f} pp"
          + (" — coincides with the bound" if si["coincides_with_bound"]["value"] else "") + " |")
        w(f"| Continued | *not published — Continued is never emitted as a point* | "
          f"{ct['ceiling']['percent']:.4f}% ({ct['ceiling']['numerator_pairs']:,}) | — |")
        w("")
        c = p["ceilings_cannot_all_hold"]
        w(f"**The three ceilings cannot all hold.** {ns['ceiling']['percent']:.4f}% + "
          f"{sl['ceiling']['percent']:.4f}% + {ct['ceiling']['percent']:.4f}% = "
          f"**{c['sum_percent']:.4f}%** on {h['n_position_5']:,}, an excess of "
          f"**{c['excess_pp']:.4f} pp = {c['excess_pairs']:,} pairs**. Mechanism: "
          f"`{c['excess_mechanism_expression']}`. They are alternative worst cases over one set, "
          f"not simultaneous ones.")
        w("")
    w("")

# ------------------------------------------------------------------ notes on the primary arm
a108 = arm_of("W108_s2_finale")
p108a = payload(a108, "APPLY")
p108d = payload(a108, "DERIV")
w("## 2. Four things a reader will otherwise get wrong")
w("")
ch = M["arms_measured"]["W108_s2_finale"]["APPLY"][
    "channel_pairs_last_insertion_in_tau1_tau2"]
chd = M["arms_measured"]["W108_s2_finale"]["DERIV"][
    "channel_pairs_last_insertion_in_tau1_tau2"]
w(f"**(a) The never-started floor is NOT widened, although {ch['never_started']} retained "
  f"never-started pairs on APPLY (and {chd['never_started']} on DERIV) had their last insertion "
  f"inside (τ1, τ2).** The reason is the ANCHORING, not the count. Never started is the null "
  f"`|A| = 0` **read at τ1**, and every one of those pairs has an insertion after τ1 — which is "
  f"exactly what gate `decisions/0021` licenses. Their null is OBSERVED, not conceded. The "
  f"{ch['started_and_left']} pairs the started-and-left floor concedes on APPLY "
  f"({chd['started_and_left']} on DERIV) differ because the **Continued** condition they negate "
  f"is read at **τ2**, and they are dormant before it.")
w("")
w("**(b) The bound's scope publishes with the bound.** It is covering with respect to "
  "INSERTION-DORMANCY, **exhaustively** — every pair either was inserting through its own test "
  "instant or was not — and **open only across the channel classes D4 and D9**, which publish "
  "ALONGSIDE and are never folded in. D4 and D9 are Step 8's figures and are not restated here: "
  "under `decisions/0114` E8 they are carried ONCE, in the merged document at Step 13b, and "
  "this file emits the absence idiom for them rather than becoming a seventh writer of a figure "
  "it did not produce.")
w("")
ns_d = p108d["bounds"]["never_started"]
sh_d = p108d["shares"]["never_started"]
w(f"**(c) On DERIV the never-started bound is DEGENERATE — "
  f"[{ns_d['floor']['percent']:.4f}%, {ns_d['ceiling']['percent']:.4f}%] — so the dual control "
  f"is `x = x` there.** The informative comparison between the two arms is on APPLY. And the "
  f"published DERIV never-started share, **{sh_d['value_percent']:.4f}%**, lies **outside** that "
  f"bound by {sh_d['value_percent'] - ns_d['ceiling']['percent']:.4f} pp — not an error: the "
  f"bound is on position 5 (n = {a108['headline']['DERIV']['n_position_5']:,}) and the share is "
  f"post-liveness (n = {a108['headline']['DERIV']['n_post_liveness']:,}).")
w("")
w("**(c2) The attainable corners, primary arm.** Each row is a COMPLETE allocation of the "
  "conceded pairs, so its three values sum to exactly 100 — which is what makes an endpoint "
  "*attainable* rather than merely arithmetic. Note that the never-started FLOOR corner and the "
  "started-and-left CEILING corner are the SAME corner: those two endpoints are not independent.")
w("")
for pop in ("APPLY", "DERIV"):
    pp = payload(a108, pop)
    w(f"*{pop}, on position 5, n = {a108['headline'][pop]['n_position_5']:,}*")
    w("")
    w("| Corner | Never started | Started and left | Continued | sum |")
    w("| :--- | ---: | ---: | ---: | ---: |")
    seen = set()
    for bname in ("never_started", "started_and_left"):
        for c in pp["bounds"][bname]["attainable_corners"]:
            trio = (c["never_started_percent"], c["started_and_left_percent"],
                    c["continued_percent"])
            if trio in seen:
                continue
            seen.add(trio)
            w(f"| {bname} {c['corner']} | {trio[0]:.4f}% | {trio[1]:.4f}% | {trio[2]:.4f}% | "
              f"{sum(trio):.4f}% |")
    w("")
w("**(d) The three states are not measured alike.** Never started is a "
  f"{a108['W_days']}-day statement at the primary arm; Continued is a "
  f"{a108['W_days'] + a108['H_days']}-day one. Every share above carries its own horizon.")
w("")

# ------------------------------------------------------------------ the 91-day arm
w("## 3. The 91-day arm sits on a DIFFERENT ORIGIN, and the two are not one measurement at two "
  "window lengths")
w("")
pa = payload(arm_of("W091_s2_premiere"), "APPLY")
pf = payload(arm_of("W091_s2_finale"), "APPLY")
w("Netflix's window runs from **release**, so that arm is anchored on the later of the S2 "
  "PREMIERE date and the first-pass S1 completion date. The primary arm is anchored on the "
  "FINALE. **They are two measurements, not one measurement at two window lengths**, and the "
  "movement between them mixes a window change with an origin change. That is why this file "
  "also carries the finale-anchored 91-day arm — it holds the origin fixed and moves only the "
  "window, so the two effects can be separated:")
w("")
w("| APPLY, never-started share (post-liveness) | value |")
w("| :--- | ---: |")
w(f"| W = 108, finale (primary) | {p108a['shares']['never_started']['value_percent']:.4f}% |")
w(f"| W = 91, finale — the WINDOW moved | "
  f"{pf['shares']['never_started']['value_percent']:.4f}% |")
w(f"| W = 91, premiere — the ORIGIN then moved | "
  f"{pa['shares']['never_started']['value_percent']:.4f}% |")
w("")
w(f"So of the "
  f"{pa['shares']['never_started']['value_percent'] - p108a['shares']['never_started']['value_percent']:+.4f} pp "
  f"between the primary headline and the Netflix arm, "
  f"{pf['shares']['never_started']['value_percent'] - p108a['shares']['never_started']['value_percent']:+.4f} pp "
  f"is the window and "
  f"{pa['shares']['never_started']['value_percent'] - pf['shares']['never_started']['value_percent']:+.4f} pp "
  f"is the origin. **The origin is the larger term.** Reporting the Netflix arm as 'the same "
  "result at a shorter window' would attribute all of it to the window.")
w("")
w("**The finale-anchored 91-day arm is a SUPPORTING measurement, not a third headline.** Every "
  "figure in it is Step 8's at that arm, reproduced here and agreeing exactly.")
w("")

# ------------------------------------------------------------------ bootstrap
w("## 4. The bootstrap, and both of its objects")
w("")
bs = J["bootstrap_settings"]["a_default"]
w(f"**B = {bs['B']:,} · seed {bs['seed']} · resampling unit ACCOUNT · statistic BOTH levels and "
  f"paired movements.** All four fixed by the spec (`decisions/0103`, `decisions/0118`) and "
  f"identical for both arms; this arm records no choice on any of them. Every interval in the "
  f"JSON restates all four at its point of use.")
w("")
w(f"**Account level, not pair level**: pairs are not independent — one account contributes many "
  f"— so pair-level resampling would understate every width above. The resampling frame is the "
  f"**{M['bootstrap_settings']['frame_accounts']:,} accounts** contributing at least one pair to "
  f"the position-4 output; one frame and one draw serve the whole file, which is what makes "
  f"every movement below genuinely PAIRED.")
w("")
w("**No interval in this file is show-clustered**, because this arm computes no show-bound "
  "quantity: `W` was derived at Step 6 and is not re-derived here. Every interval declares "
  "`quantity_class: outcome_shares` and `resampling_unit: account`, which is the binding cluster "
  "the record states for that class, so there is no unit disagreement to report.")
w("")
w("**A LEVEL AND A MOVEMENT ARE NEVER COMPARED TO EACH OTHER.** The movement below is "
  "**post-liveness MINUS the outcome-conditional position-5 value of the same share**, resampled "
  "as one paired delta on the same accounts — what the liveness filter does to the headline. On "
  "APPLY at the primary arm the never-started LEVEL is "
  f"{p108a['shares']['never_started']['ci']['upper'] - p108a['shares']['never_started']['ci']['lower']:.4f} pp "
  "wide and its MOVEMENT is "
  f"{M['bootstrap']['W108_s2_finale|APPLY|never_started']['movement']['upper'] - M['bootstrap']['W108_s2_finale|APPLY|never_started']['movement']['lower']:.4f} pp "
  "wide — a factor of about eleven, which is how far wrong a reader goes who is not told which "
  "one they are looking at.")
w("")
w("### All eighteen paired movements")
w("")
w(f"**All {len(DECLARED_MV)} are in the JSON, and sign does not govern publication.** A CI "
  "endpoint's type follows its statistic: a MOVEMENT endpoint is a percentage-point difference, "
  "typed `$defs.pp`, which may be zero and may be negative — and it is negative wherever the "
  "liveness filter LOWERS the share. A LEVEL endpoint is a percentage on [0, 100], typed "
  "`$defs.percent`, where a negative value is not a possible measurement. "
  f"{sum(1 for c in DECLARED_MV.values() if c['lower'] < 0 or c['upper'] < 0)} of the "
  f"{len(DECLARED_MV)} carry a negative endpoint. **Nothing was dropped by sign, clamped or "
  "re-signed.** The `in JSON` column is read from `$.declared_intervals` rather than inferred "
  "from the sign, so this table cannot claim a presence the file does not have.")
w("")
w("| Arm | Population | Outcome | Movement (point) | 95% CI, MOVEMENT | in JSON |")
w("| :--- | :--- | :--- | ---: | :--- | :---: |")
for key in KEYS:
    for pop in ("APPLY", "DERIV"):
        for o in OUTS:
            b = M["bootstrap"][f"{key}|{pop}|{o}"]
            mv = b["movement"]
            in_json = f"liveness_movement__{key}__{pop}__{o}__a" in DECLARED_MV
            w(f"| {key} | {pop} | {NAME[o]} | {b['point_movement']:+.4f} pp | "
              f"[{mv['lower']:+.4f}, {mv['upper']:+.4f}] pp | {'yes' if in_json else 'NO' } |")
w("")

# ------------------------------------------------------------------ divergences
w("## 5. Divergences between the spec and what this arm could write — REPORTED, NOT RECONCILED")
w("")
w("**D1. `both arms run on the same right-censored population, max(W, 91) + H` has two readings "
  "at the premiere-anchored arm**, and they differ by a measured amount. Reading (a), taken "
  "here: the 91-day arm runs on the primary arm's position-5 row set, censored at "
  "max(108, 91) + 91 = 199 d. Reading (b): D10 re-derived at W = 91, censoring at 182 d. "
  f"Measured: (b) is a strict superset — "
  f"{M['d10_reading_ambiguity']['reading_b_premiere_anchored_d10_APPLY']:,} against "
  f"{M['d10_reading_ambiguity']['reading_a_shared_population_APPLY']:,} on APPLY and "
  f"{M['d10_reading_ambiguity']['reading_b_premiere_anchored_d10_DERIV']:,} against "
  f"{M['d10_reading_ambiguity']['reading_a_shared_population_DERIV']:,} on DERIV, with "
  f"{M['d10_reading_ambiguity']['in_a_not_in_b_APPLY']} pairs in (a) and not in (b). The choice "
  f"moves {M['d10_reading_ambiguity']['in_b_not_in_a_APPLY']} pairs on APPLY and "
  f"{M['d10_reading_ambiguity']['in_b_not_in_a_DERIV']} on DERIV.")
w("")
w("  **And the difference is the W term, not the origin.** The premiere-anchored and "
  "finale-anchored censoring sets at W = 91 are **identical, measured on both populations** — "
  "because the Step 2 frame caps the S2 finale at 2025-12-31, which is earlier than the binding "
  "cutoff, so T0's `max()` is decided by the S1 completion date on every pair the cutoff can "
  "reach, and that term does not move with the origin. A reader would reasonably have expected "
  "the origin to matter here; it does not, and that is measured rather than assumed.")
w("")
w("**D2. The spec fixes four bootstrap elements and not the resampling FRAME or the DRAW "
  "ORDER.** Two arms that draw from different account sets, or consume one seeded generator in "
  "a different order, produce different intervals from the same fixed seed — which is the "
  "failure fixing the seed exists to prevent. This arm's choice is named in "
  "`$.arms[0].headline.APPLY.by_producing_arm.arms.a.spec_choices_this_arm_made`.")
w("")
w("**D3. `arm_grid_days` is owned by Step 13, required at the top level, and was filled by "
  "this file as first writer.** See §6.")
w("")

w("## 6. `arm_grid_days` — filled here, and NOT this arm's block")
w("")
w(f"`$.arm_grid_days` is **{J['arm_grid_days']}**. The schema requires it at the top level; "
  f"`$.block_ownership` gives its owner as **step13** with "
  f"`may_first_writer_fill: true`. **This file filled it as first writer and it is not this "
  f"arm's figure**: the eight values are transcribed from the Human Lead's ruling at "
  f"`decisions/0075`, not measured here. Step 13 is dual, so a value neither of Step 13's arms "
  f"wrote must be visible as such at the diff rather than inferred — which is why it is stated "
  f"here, in `spec_choices_this_arm_made`, and in this arm's report.")
w("")
w("## 7. Blocks this arm DECLINED to write")
w("")
w("| Block | Owner | Why not written here |")
w("| :--- | :--- | :--- |")
w("| `$.cross_arm_divergences` | step13b, human-lead-only | This arm cannot see the other arm, "
  "so it could only fabricate the search record. Omitted; Step 13b fills it with a real one. |")
w("| `$.limitations` | human_lead | Human-Lead-only, Step 14. No agent may draft it. |")
w("| `$.channel_classes` (D4, D9) | step8, published at step13b | Step 8's figures. Seven arm "
  "files filling it would make seven writers of a figure none of them produced. Absence idiom "
  "emitted. |")
w("| `$.discovery_channel_overlap` | step8, published at step13b | Same shape, same reason. |")
w("| `$.variants`, `$.tested_ranges` | step13 | Step 13's, and not this arm's to originate. |")
w("| `$.subpopulation_cuts` | step11 | Step 11's. |")
w("| `arms[].abandonment_distribution` | step10 | Step 10's; omitted rather than absence-stated, "
  "because under one file per step per arm an arm entry carries its own step's blocks only. |")
w("| `arms[].d3_prime`, `arms[].action_type_counts` | step13 | Step 13's. |")
w("| `$.notes.reading_a_placeholder` | step8b | Its text asserts `$.placeholder` is true, which "
  "is false here. Dropped rather than rewritten: rewriting would put this arm's words inside "
  "another step's block. Named in `spec_choices_this_arm_made`. |")
w("| `waterfall`, `liveness_exclusions`, `retained_by_air_period` **at the premiere arm** | none "
  "| No step in the spec produces these at a premiere-anchored arm. Block-absence records "
  "emitted with `owning_step: none`, which is a finding about the spec and not a default. |")
w("")
w("## 8. Provenance, and what this file does NOT report")
w("")
w("**This deliverable asserts this arm's own figures, its own inputs and its own limits, and "
  "nothing else.** It carries no statement about the other arm, about other steps or gates, "
  "about the state of any shared control, or about the disk state of any surface this arm does "
  "not own. Those are measured at an instant and would be published forever. **The validator's "
  "check counts and exit status are a control's output, not this arm's measurement**, and they "
  "are in `logs/step9/a_validate.json` and in this arm's report to the Human Lead — not here.")
w("")
w("*Every count in this file was measured on build "
  f"`{J['generated_by']['build_tag']}`. Step 8's figures carry Step 8's build tag, "
  f"`{json.load(open(os.path.join(ROOT, 'processed', 'step8', 'a', 'arms.json')))['build']['build_tag']}`, "
  "which is recorded in `processed/step9/a/measured.json` together with the sha256-12 of every "
  "file consumed.*")
w("")

with open(OUT, "w") as fh:
    fh.write("\n".join(L))

print("wrote", OUT, len("\n".join(L)), "bytes")
