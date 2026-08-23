"""Step 9, arm `b`, stage 0: the clock vector, and the check that catches a wrong one.

ONE DEFINITION. Both the pipeline (`step9_b_1_compute.py`) and the reproduction harness
(`step9_b_0b_reproduce.py`) import from here, so the check that is demonstrated is the same
object as the check that runs. Adopts nothing. Zero API calls.

WHY THIS FILE EXISTS.
  The premiere-anchored arm was built with `series.astype("int64") // 10 ** 9`. That divisor is
  a CLAIM ABOUT THE DTYPE -- it is right for `datetime64[ns]` and wrong for anything else -- and
  pandas 3 resolves this column at `datetime64[us]`. The claim was false, the vector decoded to
  January 1970 in every entry, and T0' collapsed to the S1 completion date for every pair.

  The correction is NOT a second constant. `10 ** 6` would be the same defect with a different
  number and would break again on the next resolution change. THE TICK RATE IS READ OFF THE
  DTYPE, and cross-checked against numpy's own unit-declared cast, which performs the conversion
  from the dtype rather than from an arithmetic constant.

THE TWO CHECK SHAPES, and why only one of them is used.
  DEF-A  decode the epoch vector back to calendar dates and compare it, ELEMENTWISE and on every
         row, against the frame's own `s2_premiere_date` strings.
  DEF-B  assert the epoch vector lands inside a plausible calendar window.

  DEF-B PASSES CLEAN ON A VECTOR THAT IS WRONG IN EVERY ENTRY as soon as the window is drawn
  loosely, and it never compares the vector to the thing it is supposed to be. DEF-A cannot pass
  on a wrong vector, because the only vector it accepts is the frame's own dates. Only DEF-A is
  used, and `verify_premiere_epoch()` raises rather than returning a flag a caller can ignore.

THE SECOND CHECK: `verify_t0_prime_order()`, id T0PRIME-ORDER.
  DEF-A verifies the PREMIERE EPOCH VECTOR. T0PRIME-ORDER verifies the thing the deliverable
  actually makes a claim about -- the ORIGIN VECTOR `T0' = max(S2 premiere, S1 completion)` and
  its ordering against the adopted `T0` -- because that ordering is the warrant for running the
  premiere arm on the adopted arm's row set without re-censoring it. It is built in the same
  shape as DEF-A and for the same reason: the bare inequality `T0' <= T0` is TRUE FOR THE WRONG
  REASON on a collapsed vector and cannot fail, so part 1 reconstructs `T0'` from the frame's own
  date STRINGS, which the epoch conversion never touches. Both checks raise; both state their
  coverage; both are demonstrated FAILING on the defective vector in `step9_b_0b_reproduce.py`.
"""
import numpy as np

DAY = 86400

# ticks per second, by numpy/pandas datetime resolution code. This table is not a divisor: the
# entry is SELECTED by the dtype the data actually carries, and an unrecognised resolution is a
# hard stop rather than a default.
TICKS_PER_SECOND = {"s": 1, "ms": 10 ** 3, "us": 10 ** 6, "ns": 10 ** 9}


def resolution_of(series):
    """The datetime resolution the column actually carries, e.g. 'us'. Hard stop if unknown."""
    dt = series.dtype
    unit = getattr(dt, "unit", None)            # pandas DatetimeTZDtype carries .unit
    if unit is None:
        unit = np.datetime_data(np.dtype(dt))[0]
    if unit not in TICKS_PER_SECOND:
        raise ValueError("HARD STOP: unrecognised datetime resolution %r on dtype %r. A default "
                         "here would be the assumption this function exists to remove." %
                         (unit, dt))
    return unit


def epoch_seconds(series):
    """Epoch SECONDS from a datetime Series, with the conversion derived from the dtype.

    Returns (values, provenance). `provenance` records the dtype, the resolution read off it and
    the ticks-per-second selected, so the output says how it was converted instead of leaving a
    reader to assume.
    """
    unit = resolution_of(series)
    ticks = TICKS_PER_SECOND[unit]
    ints = np.asarray(series.astype("int64"), dtype=np.int64)
    if (ints == np.iinfo(np.int64).min).any():
        raise ValueError("HARD STOP: NaT in the datetime column; an epoch value cannot be "
                         "derived for it and a sentinel would enter the clock silently.")
    derived = ints // ticks

    # INDEPENDENT CROSS-CHECK: numpy's unit-declared cast. It reaches the same seconds by a
    # different route -- declaring the target unit rather than dividing -- so a wrong tick rate
    # cannot survive both. Elementwise, on every row.
    declared = np.asarray(series.to_numpy(), dtype="datetime64[s]").astype(np.int64)
    if not np.array_equal(derived, declared):
        bad = int((derived != declared).sum())
        raise AssertionError("HARD STOP: derived epoch seconds disagree with the unit-declared "
                             "cast on %d of %d rows (resolution %r)." % (bad, ints.size, unit))
    return derived.astype(np.int64), {
        "dtype": str(series.dtype),
        "resolution_read_off_the_dtype": unit,
        "ticks_per_second_selected": int(ticks),
        "divisor_hardcoded": False,
        "cross_checked_against": "numpy unit-declared cast to datetime64[s]",
        "cross_check_rows": int(ints.size),
        "cross_check_mismatches": 0,
    }


def _decode_to_dates(epoch):
    """Epoch seconds -> 'YYYY-MM-DD' strings, one per row."""
    return np.asarray(epoch, dtype=np.int64).astype("datetime64[s]").astype(
        "datetime64[D]").astype(str)


def def_a_compare(epoch, truth_dates, label):
    """DEF-A: decoded epoch vector vs the frame's own date strings, elementwise, every row.

    Returns a result dict. It always states its COVERAGE, because a check that looked at nothing
    and a check that found nothing report the same value.
    """
    decoded = _decode_to_dates(epoch)
    truth = np.asarray(truth_dates, dtype=str)
    if decoded.shape != truth.shape:
        raise AssertionError("HARD STOP: %s -- %d decoded rows against %d frame rows." %
                             (label, decoded.size, truth.size))
    if decoded.size == 0:
        raise AssertionError("HARD STOP: %s compared zero rows." % label)
    mism = decoded != truth
    n_mism = int(mism.sum())
    first = None
    if n_mism:
        i = int(np.flatnonzero(mism)[0])
        first = {"row_index": i, "decoded": str(decoded[i]), "frame_says": str(truth[i])}
    return {
        "check": "DEF-A",
        "label": label,
        "what_it_compares": "the epoch vector decoded back to calendar dates, against the "
                            "frame's own s2_premiere_date strings, elementwise",
        "rows_compared": int(decoded.size),
        "mismatches": n_mism,
        "passes": n_mism == 0,
        "first_mismatch": first,
        "why_not_a_calendar_window": "DEF-B passes clean on a vector that is wrong in every "
                                     "entry; this cannot, because the only vector it accepts is "
                                     "the frame's own dates",
    }


def verify_premiere_epoch(by_show_epoch, by_show_truth, by_pair_epoch, by_pair_truth):
    """Both DEF-A comparisons, by show and by pair. RAISES on failure; does not return a flag."""
    res = {
        "by_show": def_a_compare(by_show_epoch, by_show_truth, "premiere epoch, one row per show"),
        "by_pair": def_a_compare(by_pair_epoch, by_pair_truth, "premiere epoch, one row per pair"),
    }
    for k, r in res.items():
        if not r["passes"]:
            raise AssertionError(
                "HARD STOP: DEF-A failed on %s -- %d of %d rows disagree with the frame; first "
                "mismatch %r. The premiere clock vector is wrong and no figure may be computed "
                "from it." % (k, r["mismatches"], r["rows_compared"], r["first_mismatch"]))
    res["total_rows_compared"] = res["by_show"]["rows_compared"] + res["by_pair"]["rows_compared"]
    return res


def _first(mask, **cols):
    """The first offending row, with the columns that show why. None if there is none."""
    idx = np.flatnonzero(mask)
    if idx.size == 0:
        return None
    i = int(idx[0])
    out = {"row_index": i}
    for k, v in cols.items():
        out[k] = str(np.asarray(v)[i])
    return out


def verify_t0_prime_order(t0_prime, t0_finale, premiere_dates_by_pair, s1_epoch,
                          tau2_prime, tau2_finale, tau_pull, retained):
    """T0PRIME-ORDER: the warrant for running the premiere arm on the ADOPTED arm's row set.

    WHAT IT CHECKS, AND WHY THE CLAIM NEEDS CHECKING.
      The premiere-anchored arm is not re-censored: it runs on the adopted arm's position-5 rows.
      That is licensed only if `T0' <= T0` on every pair, because D10 retains a pair on the
      FINALE clock and the premiere arm then reads `tau2'` on it.

    WHY IT IS THREE PARTS AND NOT THE ONE INEQUALITY.
      `T0' <= T0` ON ITS OWN CANNOT FAIL ON A COLLAPSED VECTOR. `T0' = max(premiere, S1
      completion)`, so a premiere epoch that decodes to 1970 gives `T0' = the S1 completion date`
      for every pair, and that is `<= T0 = max(finale, S1 completion)` unconditionally. It is
      TRUE FOR THE WRONG REASON, which is precisely what the removed boolean
      `t0_is_earlier_or_equal_for_every_pair` was.
      PART 1 IS THEREFORE A RECONSTRUCTION OF `T0'` FROM A SOURCE THE EPOCH CONVERSION NEVER
      TOUCHED -- the frame's own date STRINGS, compared lexicographically, which is chronological
      for ISO dates. It is what fails on the defective vector: there `T0'` decodes to the S1
      completion date on every pair, while the reconstruction says the premiere date wherever the
      premiere is the later of the two. Parts 2 and 3 are then real assertions ON A VECTOR THAT
      HAS BEEN PINNED, rather than on one that could be anything.

    IT RAISES. It does not return a flag a caller can ignore, and every part states its coverage,
    because a check that looked at nothing and a check that found nothing report the same value.
    """
    t0_prime = np.asarray(t0_prime, dtype=np.int64)
    t0_finale = np.asarray(t0_finale, dtype=np.int64)
    if t0_prime.size == 0:
        raise AssertionError("HARD STOP: T0PRIME-ORDER compared zero pairs.")
    if t0_prime.shape != t0_finale.shape:
        raise AssertionError("HARD STOP: T0PRIME-ORDER -- %d T0' rows against %d T0 rows."
                             % (t0_prime.size, t0_finale.size))

    # ---- PART 1: reconstruction, off the frame's date strings --------------------------------
    decoded = _decode_to_dates(t0_prime)
    prem_days = np.asarray(premiere_dates_by_pair, dtype=str)
    s1_days = _decode_to_dates(s1_epoch)
    if prem_days.shape != decoded.shape or s1_days.shape != decoded.shape:
        raise AssertionError("HARD STOP: T0PRIME-ORDER part 1 -- %d decoded rows against %d "
                             "premiere strings and %d S1 dates."
                             % (decoded.size, prem_days.size, s1_days.size))
    expected = np.where(prem_days >= s1_days, prem_days, s1_days)
    mism = decoded != expected
    part1 = {
        "part": 1,
        "name": "T0' RECONSTRUCTED from the frame's own date strings",
        "what_it_compares": "T0' decoded back to calendar dates, against the elementwise later "
                            "of the frame's s2_premiere_date STRING and the decoded first-pass "
                            "S1 completion date -- lexicographic max, which is chronological "
                            "for ISO dates. The truth side never passes through the epoch "
                            "conversion, which is where the defect lived.",
        "rows_compared": int(decoded.size),
        "mismatches": int(mism.sum()),
        "passes": bool(not mism.any()),
        "first_mismatch": _first(mism, T0_prime_decodes_to=decoded, reconstruction_says=expected,
                                 frame_premiere=prem_days, s1_completion=s1_days),
        "this_is_the_part_that_fails_on_the_defective_vector": True,
    }
    if not part1["passes"]:
        raise AssertionError(
            "HARD STOP: T0PRIME-ORDER part 1 failed -- T0' disagrees with its reconstruction "
            "from the frame on %d of %d pairs; first %r. The premiere-anchored clock is not "
            "max(S2 premiere, S1 completion) and the un-re-censored row set is unwarranted."
            % (part1["mismatches"], part1["rows_compared"], part1["first_mismatch"]))

    # ---- PART 2: the ordering itself ---------------------------------------------------------
    viol = t0_prime > t0_finale
    part2 = {
        "part": 2,
        "name": "T0' <= T0 on every pair",
        "what_it_compares": "the premiere-anchored origin against the finale-anchored origin, "
                            "elementwise, as epoch seconds, on every pair in the frame -- not "
                            "only on the retained ones.",
        "rows_compared": int(t0_prime.size),
        "violations": int(viol.sum()),
        "passes": bool(not viol.any()),
        "pairs_strictly_earlier": int((t0_prime < t0_finale).sum()),
        "pairs_equal": int((t0_prime == t0_finale).sum()),
        "first_violation": _first(viol, T0_prime=t0_prime, T0=t0_finale),
        "max_excess_days": float(np.max((t0_prime - t0_finale) / DAY)),
    }
    if not part2["passes"]:
        raise AssertionError(
            "HARD STOP: T0PRIME-ORDER part 2 failed -- T0' is LATER than T0 on %d of %d pairs; "
            "first %r. A pair retained on the finale clock is then not observable on the "
            "premiere clock, and the row set may not be reused."
            % (part2["violations"], part2["rows_compared"], part2["first_violation"]))

    # ---- PART 3: the consequence, on the retained rows ---------------------------------------
    tau2_prime = np.asarray(tau2_prime, dtype=np.int64)
    tau2_finale = np.asarray(tau2_finale, dtype=np.int64)
    part3 = {"part": 3,
             "name": "tau2' < tau2 <= tau_pull on every RETAINED pair",
             "what_it_compares": "the premiere arm's outcome instant against the adopted arm's, "
                                 "and against the global frozen cutoff, on the position-5 row "
                                 "set of each population.",
             "tau_pull_epoch": int(tau_pull),
             "populations": {}}
    for pop, mask in retained.items():
        mask = np.asarray(mask, dtype=bool)
        n = int(mask.sum())
        if n == 0:
            raise AssertionError("HARD STOP: T0PRIME-ORDER part 3 compared zero rows on %s." % pop)
        late = tau2_prime[mask] >= tau2_finale[mask]
        past = tau2_prime[mask] > tau_pull
        res = {
            "rows_compared": n,
            "tau2_prime_not_before_tau2_violations": int(late.sum()),
            "tau2_prime_after_tau_pull_violations": int(past.sum()),
            "passes": bool(not late.any() and not past.any()),
            "min_margin_days_tau2_to_tau2_prime":
                float(np.min((tau2_finale[mask] - tau2_prime[mask]) / DAY)),
            "min_margin_days_tau2_prime_to_tau_pull":
                float(np.min((tau_pull - tau2_prime[mask]) / DAY)),
        }
        part3["populations"][pop] = res
        if not res["passes"]:
            raise AssertionError(
                "HARD STOP: T0PRIME-ORDER part 3 failed on %s -- %d pairs with tau2' not before "
                "tau2 and %d with tau2' after tau_pull, of %d compared."
                % (pop, res["tau2_prime_not_before_tau2_violations"],
                   res["tau2_prime_after_tau_pull_violations"], n))
    part3["passes"] = True

    return {
        "check": "T0PRIME-ORDER",
        "raises_on_failure": True,
        "replaces": ["t0_is_earlier_or_equal_for_every_pair",
                     "tau2_observable_on_every_retained_pair_APPLY",
                     "tau2_observable_on_every_retained_pair_DERIV"],
        "why_the_inequality_alone_is_not_enough":
            "T0' = max(premiere, S1 completion), so a premiere epoch that decodes to 1970 gives "
            "T0' = the S1 completion date on every pair, which is <= T0 unconditionally. The "
            "inequality is then TRUE FOR THE WRONG REASON and cannot fail. Part 1 pins T0' "
            "against a source the epoch conversion never touched, and is what fails on the "
            "defective vector.",
        "part_1_reconstruction": part1,
        "part_2_ordering": part2,
        "part_3_observability": part3,
        "total_rows_compared": (part1["rows_compared"] + part2["rows_compared"]
                                + sum(p["rows_compared"] for p in part3["populations"].values())),
        "passes": True,
    }
