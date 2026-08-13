"""Step 7 rerun (decisions/0040), instance A4 — the gap distribution chart.

Aggregates only: histograms, survival curves and threshold curves. No usernames, no user ids,
no individual watch histories. Zero API calls.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/a4")
ART = os.path.join(ROOT, "artifacts")

THR_EXT = 1293
THR_MEAS = 632


def ccdf(x, n_pts=600):
    xs = np.sort(x)
    q = np.linspace(0, 1, n_pts, endpoint=False)
    v = np.quantile(xs, q)
    return v, 1.0 - q


def main():
    br = json.load(open(os.path.join(OUT, "bracketing_W108.json")))
    arms = json.load(open(os.path.join(OUT, "arms.json")))
    boot = json.load(open(os.path.join(OUT, "bootstrap.json")))

    d = np.load(os.path.join(OUT, "pair_bracketing_W108.npz"))
    ref, gap, no_after, no_before = d["ref"], d["gap_days"], d["no_after"], d["no_before"]
    g = gap[ref & ~no_after & ~no_before]
    n_open = int((ref & no_after).sum())
    n_nb = int((ref & no_before).sum())
    pooled = np.load(os.path.join(OUT, "pooled_gaps.npz"))["gap_days"]
    rep = np.load(os.path.join(OUT, "bootstrap_replicates.npz"))

    fig, ax = plt.subplots(2, 3, figsize=(19.5, 11))
    fig.suptitle(
        "Step 7 (rerun on decisions/0040), instance A4 — bracketing-gap distribution on the "
        "POST-D10 population\n"
        f"W = 108 d, H = 91 d, tau_pull = 2026-08-11.  152,126 -> D10 -> "
        f"{br['population']['post_D10_population']:,} pairs; "
        f"{len(g):,} carry a measured bracketing gap, {n_open:,} are open-ended, "
        f"{n_nb:,} have no pre-tau1 instant and are LIVE per decisions/0021.  "
        "PROPOSED, NOT ADOPTED.",
        fontsize=11)

    # --- 1. histogram of the bracketing gap, log x ---
    a = ax[0, 0]
    pos = g[g > 0]
    bins = np.logspace(np.log10(pos.min()), np.log10(pos.max()), 90)
    a.hist(pos, bins=bins, color="#4477aa", edgecolor="none")
    a.axvline(THR_MEAS, color="#cc3311", lw=1.8,
              label=f"632 d — 99th of measured-gap set")
    a.axvline(THR_EXT, color="#000000", lw=1.8, ls="--",
              label=f"1,293 d — 99th of EXTENDED set")
    a.set_xscale("log")
    a.set_xlabel("bracketing gap (days, log scale)")
    a.set_ylabel("pairs (one gap per pair)")
    a.set_title("1. The gap bracketing tau1, one per pair\n"
                f"median {np.median(g):.2f} d, p75 {np.percentile(g, 75):.2f} d, "
                f"p95 {np.percentile(g, 95):.1f} d")
    a.legend(fontsize=8)

    # --- 2. survival curve with the exclusion region ---
    a = ax[0, 1]
    v, s = ccdf(g)
    a.plot(v, s, color="#4477aa", lw=2, label="measured bracketing gaps")
    n_tot = len(g) + n_open
    a.axhline(n_open / n_tot, color="#999999", ls=":", lw=1.5,
              label=f"open-ended floor {n_open / n_tot:.4%} (never falls below)")
    a.axvline(THR_MEAS, color="#cc3311", lw=1.5)
    a.axvline(THR_EXT, color="#000000", lw=1.5, ls="--")
    a.axhline(0.01, color="#ee7733", ls="-.", lw=1.2, label="1% quota")
    a.set_xscale("log")
    a.set_yscale("log")
    a.set_xlabel("gap length (days, log scale)")
    a.set_ylabel("share of pairs with a gap at least this long")
    a.set_title("2. Survival. The quota is read off the y-axis,\n"
                "the threshold off the x-axis — that is the quota property")
    a.legend(fontsize=8)

    # --- 3. pooled vs bracketing: the length bias 0037 named ---
    a = ax[0, 2]
    qs = np.concatenate([np.linspace(0.001, 0.99, 400), np.linspace(0.99, 0.99999, 200)])
    a.plot(np.quantile(pooled, qs), 1 - qs, color="#999933", lw=2,
           label=f"POOLED gaps (n={len(pooled):,})")
    a.plot(np.quantile(g, qs), 1 - qs, color="#4477aa", lw=2,
           label=f"BRACKETING gaps (n={len(g):,})")
    a.axvline(4, color="#882255", lw=1.5, ls=":",
              label="pooled 99th = 4 d (withdrawn basis)")
    a.set_xscale("log")
    a.set_yscale("log")
    a.set_xlabel("gap length (days, log scale)")
    a.set_ylabel("survival")
    a.set_title("3. Why 0037 withdrew the pooled basis: length bias.\n"
                f"{br['withdrawn_pooled_basis']['bracketing_pairs_failing_pooled_threshold_rate']:.1%}"
                " of bracketing gaps exceed the pooled 99th")
    a.legend(fontsize=8)

    # --- 4. threshold as a function of the chosen percentile ---
    a = ax[1, 0]
    ps = np.linspace(80, 99.9, 300)
    ext = np.concatenate([g, np.full(n_open, np.inf)])
    with np.errstate(invalid="ignore"):
        t_ext = np.array([np.percentile(ext, q) for q in ps])
    t_meas = np.array([np.percentile(g, q) for q in ps])
    a.plot(ps, t_meas, color="#cc3311", lw=2, label="measured-gap-only reference")
    fin = np.isfinite(t_ext)
    a.plot(ps[fin], t_ext[fin], color="#000000", lw=2, ls="--",
           label="EXTENDED reference (open-ended = inf)")
    cut = 100 * (1 - n_open / n_tot)
    a.axvline(cut, color="#999999", ls=":", lw=1.5,
              label=f"above the {cut:.3f}th the extended p is INFINITE")
    a.axvline(99, color="#ee7733", lw=1.2)
    a.set_yscale("log")
    a.set_xlabel("percentile chosen")
    a.set_ylabel("threshold (days, log scale)")
    a.set_title("4. The threshold is whatever the chosen percentile costs.\n"
                "No feature of the data picks a level")
    a.legend(fontsize=8)

    # --- 5. W-coupling ---
    a = ax[1, 1]
    ws = sorted(int(k) for k in arms["arms"])
    te = [arms["arms"][str(w)]["EXTENDED_reference"]["threshold_days"] for w in ws]
    tm = [arms["arms"][str(w)]["MEASURED_ONLY_reference"]["threshold_days"] for w in ws]
    a.plot(ws, tm, "o-", color="#cc3311", label="measured-gap-only reference")
    a.plot(ws, te, "s--", color="#000000", label="EXTENDED reference")
    a.axvline(108, color="#ee7733", lw=1.2, label="adopted W = 108")
    a.set_xlabel("W (days)")
    a.set_ylabel("refitted threshold (days)")
    a.set_title("5. The threshold IS a function of W (0038 SS6).\n"
                f"measured-only {min(tm)}–{max(tm)} d, extended {min(te)}–{max(te)} d "
                "across the Step 13 arms")
    a.legend(fontsize=8)

    # --- 6. bootstrap ---
    a = ax[1, 2]
    for key, col, lab in (("thr_meas", "#cc3311", "measured-only, account-clustered"),
                          ("thr_meas_iid", "#88ccee", "measured-only, i.i.d. (invented precision)")):
        x = rep[key]
        x = x[np.isfinite(x)]
        a.hist(x, bins=70, alpha=0.6, color=col, label=lab)
    ci = boot["ACCOUNT_CLUSTERED"]["measured_only"]["ci95_ceil_days"]
    a.axvline(THR_MEAS, color="#000000", lw=1.8, label=f"point estimate {THR_MEAS} d")
    for e in ci:
        a.axvline(e, color="#000000", ls=":", lw=1.4)
    a.set_xlabel("bootstrap 99th percentile (days)")
    a.set_ylabel(f"replicates (B = {boot['replicates']:,})")
    a.set_title(f"6. Account-clustered bootstrap, B = {boot['replicates']:,}.\n"
                f"clustered 95% CI [{ci[0]}, {ci[1]}] d — "
                f"{boot['IID_FOR_CONTRAST_NOT_TO_BE_REPORTED']['measured_only']['clustered_width_over_iid_width']}x "
                "the i.i.d. width")
    a.legend(fontsize=8)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    path = os.path.join(ART, "step7-gap-distribution-a4.png")
    fig.savefig(path, dpi=110)
    print("wrote", path)


if __name__ == "__main__":
    main()
