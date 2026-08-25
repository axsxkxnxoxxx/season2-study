"""Step 9, arm `a`, stage 5: the emitted replicate set, checked.

decisions/0125 makes BIT-IDENTICAL REPLICATE SETS the test of whether the bootstrap spec is
complete, and requires arm `a` to EMIT its set as evidence. `step9_a_1_compute.py` emits it.
This script checks the emitted file is what it claims to be, and -- the part that matters --
that it is the set BEHIND THE PUBLISHED INTERVALS rather than a fresh draw at the same seed.

It performs NO cross-arm comparison. The completeness test is the Human Lead's (0125 SS5).

Five checks, each with a NEGATIVE CONTROL, because decisions/0123 SS3 rules that a precondition
which cannot fail on the vector it polices is not a check:

  C1  structural  -- shape, dtype, row sums, digest against the manifest
  C2  conformance -- an INDEPENDENT redraw using 0125's exact call, at a DIFFERENT chunk,
                     is bit-identical to the emitted matrix
  C3  reproduction-- weights @ C, percentiled, reproduces EVERY raw endpoint in
                     processed/step9/a/measured.json bit-exactly
  C4  publication -- every rendering of those endpoints in artifacts/step9-headline-a.json
                     (6 dp) and artifacts/step9-headline-a.md (4 dp) is reproduced, AND both
                     files carry every measured quantity
  C5  coverage    -- every check states how many rows it looked at; a zero count FAILS,
                     because an empty result and a clean result are the same value

NO EXPECTED COUNT IN THIS FILE IS TYPED. They are derived from measured.json, which says what
this arm measured; see the note above CI_LEVEL for what a typed one did here.

Zero API calls. Writes logs/step9/a_weights_selftest.json. Writes nothing to artifacts/.
"""
import hashlib
import json
import os
import re
import sys

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed", "step9", "a")
LOGS = os.path.join(ROOT, "logs", "step9")
os.makedirs(LOGS, exist_ok=True)

results = {}
failures = []


def check(name, ok, detail):
    results[name] = {"pass": bool(ok), **detail}
    if not ok:
        failures.append(name)
    print(("PASS  " if ok else "FAIL  ") + name + "  " + json.dumps(detail)[:200])


# ---------------------------------------------------------------------------------------------
# load
# ---------------------------------------------------------------------------------------------
wz = np.load(os.path.join(OUT, "boot_weights.npz"))
Wm = wz["weights"]
n_frame = int(wz["n_frame"])
B = int(wz["B"])
SEED = int(wz["seed"])
cz = np.load(os.path.join(OUT, "boot_columns.npz"))
C = cz["C"]
COLS = [str(c) for c in cz["cols"]]
MAN = json.load(open(os.path.join(OUT, "boot_weights_manifest.json")))
MEAS = json.load(open(os.path.join(OUT, "measured.json")))

# ---------------------------------------------------------------------------------------------
# EVERY EXPECTED COUNT BELOW IS DERIVED FROM A FILE. NONE IS TYPED.
#
# This was not a style preference. C4a expected 54 endpoint values because 54 was what the
# publication happened to contain on the day the check was written -- nine movement intervals
# were being withheld by sign at the time. When the nine were published the check FAILED WITH
# ZERO MISMATCHES: 72 checked, 72 reproduced, and an exit code of 1 produced entirely by a typed
# constant. A retyped count does not test the file; it tests whether the file still looks like
# it did when someone last looked at it, and it fails LOUDEST exactly when a defect is FIXED.
#
# The anchor is `measured.json`: it says what this arm MEASURED, and every publication is
# required to carry all of it. That is an external anchor rather than a self-comparison -- the
# count cannot be satisfied by a publication that quietly drops intervals, which is the failure
# the accommodation hid. C4a and C4b each carry a negative control that removes one published
# interval and requires the count leg to REJECT, so the completeness leg is shown failing before
# it is trusted passing (decisions/0123 SS3).
#
# The arm keys, populations and outcomes are read the same way, out of the measured bootstrap's
# own key strings, so a fourth arm or a renamed outcome cannot slip past a typed list.
# ---------------------------------------------------------------------------------------------
CI_LEVEL = MEAS["bootstrap_settings"]["ci_level_pct"]
LO, HI = (100 - CI_LEVEL) / 2, 100 - (100 - CI_LEVEL) / 2

BOOT_KEYS = list(MEAS["bootstrap"])                      # "<arm>|<population>|<outcome>"
TRIPLES = [tuple(k.split("|")) for k in BOOT_KEYS]


def _ordered_unique(values):
    seen, out = set(), []
    for v in values:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


ARM_KEYS = _ordered_unique(t[0] for t in TRIPLES)
POPS = _ordered_unique(t[1] for t in TRIPLES)
OUTCOMES = _ordered_unique(t[2] for t in TRIPLES)

N_TRIPLES = len(TRIPLES)                                 # quantities measured
N_STATS = 2                                              # levels and movements (decisions/0118)
N_ENDS = 2                                               # lower and upper
N_ENDPOINTS = N_TRIPLES * N_STATS * N_ENDS               # raw endpoints this arm measured

# The product must BE the measured key list, in order. If it is not, the derived lists have
# reordered or dropped something and every ordinal-keyed check below would be reading the wrong
# quantity -- so this is asserted rather than assumed.
_product = [(a, p, o) for a in ARM_KEYS for p in POPS for o in OUTCOMES]
if _product != TRIPLES:
    print("FAIL  derived_arm_pop_outcome_product_matches_measured_keys")
    sys.exit(1)
if N_TRIPLES == 0:
    print("FAIL  measured.json declares no bootstrap quantities: a check over nothing")
    sys.exit(1)

# ---------------------------------------------------------------------------------------------
# C1 structural
# ---------------------------------------------------------------------------------------------
digest = hashlib.sha256(np.ascontiguousarray(Wm).tobytes()).hexdigest()
rows = Wm.shape[0]
c1 = (Wm.shape == (B, n_frame) and str(Wm.dtype) == "uint16"
      and bool((Wm.sum(axis=1, dtype=np.int64) == n_frame).all())
      and digest == MAN["digest_sha256_of_matrix_bytes_C_order_uint16"]
      and MAN["seed"] == SEED and MAN["B"] == B and MAN["n_frame"] == n_frame
      and rows > 0)
check("C1_structural", c1, {"shape": list(Wm.shape), "dtype": str(Wm.dtype),
                            "rows_checked": rows, "digest_matches_manifest":
                            digest == MAN["digest_sha256_of_matrix_bytes_C_order_uint16"],
                            "max_weight": int(Wm.max()),
                            "row_sums_all_eq_n_frame":
                                bool((Wm.sum(axis=1, dtype=np.int64) == n_frame).all())})
# C1 negative control: a matrix with one cell moved must fail the row-sum invariant.
bad = Wm.copy()
bad[0, 0] += 1
check("C1_negative_control", not bool((bad.sum(axis=1, dtype=np.int64) == n_frame).all()),
      {"perturbation": "boot_w[0,0] += 1", "invariant_rejects_it": True, "rows_checked": rows})


# ---------------------------------------------------------------------------------------------
# C2 conformance: redraw with 0125's exact call, at a DIFFERENT chunk, no dtype kwarg
# ---------------------------------------------------------------------------------------------
def redraw(seed, chunk):
    rng = np.random.default_rng(seed)
    out = np.empty((B, n_frame), dtype=np.uint16)
    off = (np.arange(chunk, dtype=np.int64) * n_frame)[:, None]
    for s in range(0, B, chunk):
        m = min(chunk, B - s)
        idx = rng.integers(0, n_frame, size=(m, n_frame))          # 0125's call, no dtype kwarg
        out[s:s + m] = np.bincount((idx.astype(np.int64) + off[:m]).ravel(),
                                   minlength=m * n_frame).reshape(m, n_frame)
    return out


# The redraw chunk must DIFFER from the emitting one, or C2 measures nothing about chunk
# independence while looking as though it does. Derived from the manifest and asserted, rather
# than typed and hoped for.
REDRAW_CHUNK = 10 * int(MAN["chunk_used_here"])
if REDRAW_CHUNK == int(MAN["chunk_used_here"]) or REDRAW_CHUNK <= 0:
    print("FAIL  C2 redraw chunk does not differ from the emitting chunk: the conformance "
          "redraw would not test chunk independence")
    sys.exit(1)

R = redraw(SEED, REDRAW_CHUNK)
check("C2_conformance_redraw", bool(np.array_equal(R, Wm)),
      {"generator": "numpy.random.default_rng", "seed": SEED,
       "call": "rng.integers(0, n_frame, size=(m, n_frame))  [no dtype kwarg]",
       "emitting_chunk": MAN["chunk_used_here"], "redraw_chunk": REDRAW_CHUNK,
       "cells_compared": int(Wm.size), "rows_checked": rows,
       "note": "different chunk, so this also measures 0125 SS3's chunk-independence"})
# C2 negative control: the neighbouring seed must NOT reproduce it.
check("C2_negative_control",
      not bool(np.array_equal(redraw(SEED + 1, REDRAW_CHUNK), Wm)),
      {"perturbation": f"seed {SEED + 1}", "redraw_rejected": True, "rows_checked": rows})

# ---------------------------------------------------------------------------------------------
# C3 reproduction of the 72 raw endpoints from the EMITTED matrix
# ---------------------------------------------------------------------------------------------
colidx = {c: i for i, c in enumerate(COLS)}
sums = Wm.astype(np.float64) @ C


def share_draws(arm, pop, pos, outcome):
    num = sums[:, colidx[f"{arm}|{pop}|{pos}|{outcome}"]]
    den = sums[:, colidx[f"{arm}|{pop}|{pos}|total"]]
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, 100.0 * num / den, np.nan)


def endpoints_from(sums_mat):
    """All 72 endpoints, from an arbitrary (B, n_frame) weight matrix's column sums."""
    def draws(arm, pop, pos, outcome):
        num = sums_mat[:, colidx[f"{arm}|{pop}|{pos}|{outcome}"]]
        den = sums_mat[:, colidx[f"{arm}|{pop}|{pos}|total"]]
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(den > 0, 100.0 * num / den, np.nan)

    out = {}
    for arm in ARM_KEYS:
        for pop in POPS:
            for outcome in OUTCOMES:
                lev = draws(arm, pop, "p7", outcome)
                mov = lev - draws(arm, pop, "p5", outcome)
                out[f"{arm}|{pop}|{outcome}"] = {
                    "level": {"lower": float(np.nanpercentile(lev, LO)),
                              "upper": float(np.nanpercentile(lev, HI))},
                    "movement": {"lower": float(np.nanpercentile(mov, LO)),
                                 "upper": float(np.nanpercentile(mov, HI))}}
    return out


def n_endpoints_matching(cand):
    n = 0
    for k, blk in cand.items():
        for stat in ("level", "movement"):
            for end in ("lower", "upper"):
                n += int(blk[stat][end] == MEAS["bootstrap"][k][stat][end])
    return n


recomputed = endpoints_from(sums)

exact, checked, worst = 0, 0, 0.0
diffs = []
for k, blk in recomputed.items():
    for stat in ("level", "movement"):
        for end in ("lower", "upper"):
            pub = MEAS["bootstrap"][k][stat][end]
            mine = blk[stat][end]
            checked += 1
            if mine == pub:                       # float64 identity, not a tolerance
                exact += 1
            else:
                d = abs(mine - pub)
                worst = max(worst, d)
                diffs.append({"key": k, "stat": stat, "end": end,
                              "published": pub, "recomputed": mine, "abs_diff": d})
check("C3_reproduction_raw_endpoints", exact == checked == N_ENDPOINTS,
      {"endpoints_checked": checked, "bit_exact": exact,
       "endpoints_expected": N_ENDPOINTS,
       "expected_derived_from": ("len(measured.json $.bootstrap) x 2 statistics x 2 endpoints; "
                                 "no count in this file is typed"),
       "tolerance": "NONE -- float64 equality, ==",
       "max_abs_diff_on_any_mismatch": worst, "mismatches": diffs, "rows_checked": checked,
       "source": "processed/step9/a/measured.json $.bootstrap"})
# C3 NEGATIVE CONTROLS. The claim under test is "THESE weights, not merely SOME valid weights",
# so each control substitutes a DIFFERENT but equally valid replicate set and requires the
# published endpoints NOT to come back.
#
# A first attempt nudged one account's weight in replicate 0 by +1. It could not reject, and the
# reason is instructive rather than incidental: replicate 0 sits at rank 1,051 of 10,000 on the
# quantity measured, 801 ranks from the 2.5th percentile, so a one-cell change in it cannot reach
# the endpoint. That is a control probing a place the statistic is structurally deaf to
# (decisions/0123 SS3). It is REPLACED, not softened.
m_seed = n_endpoints_matching(
    endpoints_from(redraw(SEED + 1, REDRAW_CHUNK).astype(np.float64) @ C))
check("C3_negative_control_different_seed", m_seed == 0,
      {"substitution": f"a full valid replicate set drawn at seed {SEED + 1}",
       "endpoints_that_still_matched": m_seed, "of": N_ENDPOINTS,
       "rows_checked": N_ENDPOINTS,
       "note": ("0 of the measured endpoints must come back, or the endpoints are "
                "insensitive to the draw")})

# The mechanism control, which is 0125's own finding measured on this build: `multinomial` is a
# different sampler over the SAME distribution and consumes the stream differently.
rng_m = np.random.default_rng(SEED)
p_uniform = np.full(n_frame, 1.0 / n_frame)
W_multi = rng_m.multinomial(n_frame, p_uniform, size=B)
m_mech = n_endpoints_matching(endpoints_from(W_multi.astype(np.float64) @ C))
check("C3_negative_control_different_mechanism", m_mech == 0,
      {"substitution": "rng.multinomial(n_frame, uniform, size=B) at the SAME seed",
       "endpoints_that_still_matched": m_mech, "of": N_ENDPOINTS,
       "row_sums_still_exactly_n_frame":
           bool((W_multi.sum(axis=1) == n_frame).all()),
       "identical_to_the_emitted_matrix": bool(np.array_equal(W_multi, Wm)),
       "rows_checked": N_ENDPOINTS,
       "note": ("decisions/0125 SS2, measured here: same seed, same frame, same B, a valid "
                "replicate set with correct row sums -- and NOT the same realisation, so NOT "
                "the same endpoints. This is why the mechanism had to be named.")})


def r6(x):
    return round(float(x), 6)


def r4(x):
    return round(float(x), 4)


# ---------------------------------------------------------------------------------------------
# C4a published JSON renderings (6 dp)
# ---------------------------------------------------------------------------------------------
HJ = json.load(open(os.path.join(ROOT, "artifacts", "step9-headline-a.json")))
found = []


def walk(o, p):
    if isinstance(o, dict):
        if o.get("statistic") in ("levels", "movements") and "lower" in o:
            found.append((p, o))
        for k, v in o.items():
            walk(v, p + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, p + f"[{i}]")


walk(HJ, "$")
# map each published CI object back to its (arm, pop, outcome) by PATH, never by value
arm_order = [a["arm_id"].split("__")[0] for a in HJ["arms"]]

# EVERY MEASURED QUANTITY, IN BOTH OBJECTS. This is the completeness anchor, derived from
# measured.json: the publication must carry all of it, and a publication that withholds
# intervals -- by sign or by anything else -- fails on the coverage leg rather than on a
# hand-updated total.
EXPECTED_JSON_CIS = {(f"{a}|{p}|{o}", stat)
                     for a, p, o in TRIPLES for stat in ("level", "movement")}


def match_json(found_list):
    """Reproduce every published CI object, and report which measured ones were covered."""
    ok, checked, bad, covered = 0, 0, [], set()
    for path, obj in found_list:
        if obj["statistic"] == "levels":
            m = re.match(
                r"\$\.arms\[(\d+)\]\.headline\.(APPLY|DERIV)\..*\.shares\.(\w+)\.ci$", path)
            if not m:
                bad.append({"path": path, "why": "level CI at an unrecognised path"})
                continue
            key = f"{arm_order[int(m.group(1))]}|{m.group(2)}|{m.group(3)}"
            stat = "level"
        else:
            iid = HJ["declared_intervals"][int(re.match(r"\$\.declared_intervals\[(\d+)\]",
                                                        path).group(1))]["interval_id"]
            _, armk, pop, outcome, _ = iid.split("__")
            key, stat = f"{armk}|{pop}|{outcome}", "movement"
        covered.add((key, stat))
        for end in ("lower", "upper"):
            checked += 1
            want = r6(recomputed[key][stat][end])
            if r6(obj[end]) == want:
                ok += 1
            else:
                bad.append({"path": path, "end": end, "published": obj[end],
                            "recomputed": want})
    return ok, checked, bad, covered


json_ok, json_checked, json_bad, json_covered = match_json(found)
json_missing = sorted(f"{k}|{st}" for k, st in EXPECTED_JSON_CIS - json_covered)
n_json_levels = sum(1 for _p, o in found if o["statistic"] == "levels")
n_json_movements = sum(1 for _p, o in found if o["statistic"] == "movements")
check("C4a_published_json_renderings",
      json_ok == json_checked == N_ENDPOINTS and not json_bad and not json_missing
      and n_json_levels == N_TRIPLES and n_json_movements == N_TRIPLES,
      {"ci_objects_found": len(found), "level_ci_objects": n_json_levels,
       "movement_ci_objects": n_json_movements,
       "endpoint_values_checked": json_checked, "reproduced": json_ok,
       "endpoint_values_expected": N_ENDPOINTS,
       "expected_derived_from": ("measured.json $.bootstrap -- what this arm MEASURED. Nothing "
                                 "here is typed, and a publication that withholds an interval "
                                 "fails on `measured_quantities_missing` rather than on a "
                                 "constant somebody has to remember to update"),
       "measured_quantities_missing": json_missing,
       "precision": "6 dp", "mismatches": json_bad,
       "rows_checked": json_checked, "file": "artifacts/step9-headline-a.json"})

# C4a NEGATIVE CONTROL -- the completeness leg, shown REJECTING. Drop one published movement CI
# from the found list and require the check to fail. Without this, "72 of 72 covered" could be a
# tautology in which the expected count came from the same place as the observed one.
# Removed BY INDEX. A first attempt built the victim with `next((p, o) for p, o in found ...)`,
# which constructs a NEW tuple, so the identity filter `x is not _dropped` removed nothing and
# the control reported 72 of 72 still checked -- a control that could not perturb what it was
# perturbing. It is recorded rather than quietly fixed: it is the same defect class as the
# accommodation above, one level up.
_drop_i = next((i for i, (_p, o) in enumerate(found) if o["statistic"] == "movements"), None)
if _drop_i is None:
    check("C4a_negative_control_dropped_interval", False,
          {"rows_checked": 0, "why": "no movement CI object to drop: the control looked at "
                                     "nothing, which is not the same as finding nothing"})
else:
    _dropped = found[_drop_i]
    _short = found[:_drop_i] + found[_drop_i + 1:]
    assert len(_short) == len(found) - 1
    _ok, _checked, _bad, _cov = match_json(_short)
    _missing = EXPECTED_JSON_CIS - _cov
    check("C4a_negative_control_dropped_interval",
          bool(_missing) and _checked < N_ENDPOINTS,
          {"perturbation": f"one published movement CI removed ({_dropped[0]})",
           "endpoint_values_then_checked": _checked, "expected": N_ENDPOINTS,
           "measured_quantities_then_missing": sorted(f"{k}|{st}" for k, st in _missing),
           "coverage_leg_rejects_it": bool(_missing),
           "rows_checked": len(_short),
           "note": ("the accommodation this replaces could not have failed here: it compared "
                    "against a typed 54 and would have PASSED on a publication missing nine "
                    "intervals, and FAILED on the complete one")})

# ---------------------------------------------------------------------------------------------
# C4b published MD renderings (4 dp), parsed by TABLE CONTEXT, not by value
# ---------------------------------------------------------------------------------------------
md = open(os.path.join(ROOT, "artifacts", "step9-headline-a.md")).read().splitlines()
# The table markers carry the CI level, which is read from measured.json like everything else: a
# typed "95%" here would stop matching the day the level moved, and the parser would report zero
# rows rather than a wrong one.
LEVEL_MARKER = f"{CI_LEVEL}% CI, LEVEL"
MOVEMENT_MARKER = f"{CI_LEVEL}% CI, MOVEMENT"
md_pairs = []          # (kind, ordinal_within_kind, lower, upper)
in_level, lvl_tbl, row_i = False, -1, 0
in_mov = False
for line in md:
    if line.startswith("| Outcome |") and LEVEL_MARKER in line:
        in_level, in_mov, lvl_tbl, row_i = True, False, lvl_tbl + 1, 0
        continue
    if line.startswith("| Arm |") and MOVEMENT_MARKER in line:
        in_mov, in_level, row_i = True, False, 0
        continue
    if in_level:
        m = re.search(r"\|\s*\[([\d.]+)%,\s*([\d.]+)%\]\s*\|", line)
        if m:
            md_pairs.append(("level", lvl_tbl * len(OUTCOMES) + row_i,
                             float(m.group(1)), float(m.group(2))))
            row_i += 1
        elif not line.startswith("|"):
            in_level = False
    if in_mov:
        m = re.search(r"\|\s*\[([+-][\d.]+),\s*([+-][\d.]+)\]\s*pp\s*\|", line)
        if m:
            md_pairs.append(("movement", row_i, float(m.group(1)), float(m.group(2))))
            row_i += 1
        elif not line.startswith("|") and line.strip():
            in_mov = False

# expected order: arms outer, then population, then outcome -- the order both tables are written,
# and asserted above to BE the order of the measured keys rather than assumed to be
expected = TRIPLES


def match_md(pairs):
    ok, checked, bad, covered = 0, 0, [], set()
    for kind, ordinal, lo, hi in pairs:
        if ordinal >= len(expected):
            bad.append({"kind": kind, "ordinal": ordinal,
                        "why": "row beyond the measured quantities: the table is longer than "
                               "what this arm measured"})
            continue
        a, p, o = expected[ordinal]
        stat = "level" if kind == "level" else "movement"
        covered.add((f"{a}|{p}|{o}", stat))
        blk = recomputed[f"{a}|{p}|{o}"][stat]
        for end, got in (("lower", lo), ("upper", hi)):
            checked += 1
            if r4(blk[end]) == got:
                ok += 1
            else:
                bad.append({"kind": kind, "ordinal": ordinal, "key": f"{a}|{p}|{o}",
                            "end": end, "published": got, "recomputed": r4(blk[end])})
    return ok, checked, bad, covered


md_ok, md_checked, md_bad, md_covered = match_md(md_pairs)
md_missing = sorted(f"{k}|{st}" for k, st in EXPECTED_JSON_CIS - md_covered)
n_lvl = sum(1 for k, *_ in md_pairs if k == "level")
n_mov = sum(1 for k, *_ in md_pairs if k == "movement")
check("C4b_published_md_renderings",
      md_ok == md_checked == N_ENDPOINTS and n_lvl == N_TRIPLES and n_mov == N_TRIPLES
      and not md_bad and not md_missing,
      {"level_rows_parsed": n_lvl, "movement_rows_parsed": n_mov,
       "rows_expected_per_table": N_TRIPLES,
       "endpoint_values_checked": md_checked, "reproduced": md_ok,
       "endpoint_values_expected": N_ENDPOINTS,
       "measured_quantities_missing": md_missing,
       "precision": "4 dp",
       "mismatches": md_bad, "rows_checked": md_checked,
       "file": "artifacts/step9-headline-a.md",
       # THE OLD NOTE HERE DESCRIBED A FILTER THAT NEVER EXISTED. It said "the JSON carries only
       # the 9 with non-negative endpoints". The filter it was describing dropped every movement
       # with a NEGATIVE endpoint -- and one of those it dropped has a POSITIVE UPPER endpoint,
       # so "the 9 with non-negative endpoints" was not what was kept and never had been. The
       # filter itself is gone (decisions/0126: never drop an interval because its sign will not
       # fit), and the counts below are read off the two files rather than described.
       "both_files_carry_every_measured_quantity": not md_missing,
       "json_and_md_row_counts_agree": n_lvl == n_json_levels and n_mov == n_json_movements,
       "movements_with_a_negative_endpoint": sum(
           1 for kind, _o, lo, hi in md_pairs if kind == "movement" and (lo < 0 or hi < 0)),
       "of_those_with_a_positive_upper_endpoint": sum(
           1 for kind, _o, lo, hi in md_pairs
           if kind == "movement" and lo < 0 and hi > 0)})

# C4b NEGATIVE CONTROL -- the coverage leg shown REJECTING, for the same reason as C4a's.
if not md_pairs:
    check("C4b_negative_control_dropped_row", False,
          {"rows_checked": 0, "why": "no parsed md row to drop: looked at nothing"})
else:
    _short_md = md_pairs[:-1]
    _ok, _checked, _bad, _cov = match_md(_short_md)
    _missing = EXPECTED_JSON_CIS - _cov
    check("C4b_negative_control_dropped_row",
          bool(_missing) and _checked < N_ENDPOINTS,
          {"perturbation": "the last parsed md CI row removed",
           "endpoint_values_then_checked": _checked, "expected": N_ENDPOINTS,
           "measured_quantities_then_missing": sorted(f"{k}|{st}" for k, st in _missing),
           "coverage_leg_rejects_it": bool(_missing),
           "rows_checked": len(_short_md)})

# ---------------------------------------------------------------------------------------------
# C5 coverage: a check that looked at nothing must FAIL, not pass
# ---------------------------------------------------------------------------------------------
zero = [k for k, v in results.items() if v.get("rows_checked", 0) == 0]
check("C5_coverage_no_check_looked_at_nothing", not zero,
      {"checks_run": len(results), "checks_with_zero_rows": zero,
       "rows_checked": len(results)})

payload = {"step": 9, "instance": "a", "stage": 5, "api_calls": 0, "decision": "0125",
           "what_this_is": ("the emitted replicate set, checked against the PUBLISHED intervals. "
                            "No cross-arm comparison is performed here: the completeness test is "
                            "the Human Lead's."),
           "weights_file": os.path.join(OUT, "boot_weights.npz"),
           "manifest": MAN, "checks": results,
           "failures": failures, "exit": 1 if failures else 0}
with open(os.path.join(LOGS, "a_weights_selftest.json"), "w") as fh:
    json.dump(payload, fh, indent=1)

print(f"\n{len(results) - len(failures)}/{len(results)} checks pass; "
      f"raw endpoints {exact}/{checked} bit-exact; "
      f"json renderings {json_ok}/{json_checked}; md renderings {md_ok}/{md_checked}")
sys.exit(1 if failures else 0)
