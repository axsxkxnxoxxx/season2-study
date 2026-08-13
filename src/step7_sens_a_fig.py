"""Step 7 gate-closing sensitivity test (decisions/0041 SS4), instance namespace `a`.

STAGE 5 — a continuous sweep of the threshold, and the figure.

The four required settings are four points on a curve. Sweeping T continuously shows whether
the flatness is a property of the rule or an accident of which three numbers were picked.

Output: artifacts/step7-sensitivity-a.png (aggregate curves and counts only, no row detail)
        processed/step7/sens_a/sweep.json

This is NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved gate.

Zero API calls.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/sens_a")
ART = os.path.join(ROOT, "artifacts")

MARKS = [787, 1293, 2200]


def main():
    st = np.load(os.path.join(OUT, "pair_states.npz"))
    never, cont, left = st["never"], st["continued"], st["left"]
    no_after, gap, measured = st["no_after"], st["gap"], st["measured"]
    boot = json.load(open(os.path.join(OUT, "bootstrap.json")))

    grid = np.unique(np.concatenate([
        np.arange(30.0, 4001.0, 5.0), np.array(MARKS, dtype=float)]))

    rows = []
    for T in grid:
        live = ~(no_after | (measured & (gap >= T)))
        k = int(live.sum())
        rows.append((T, k,
                     100.0 * int((never & live).sum()) / k,
                     100.0 * int((cont & live).sum()) / k,
                     100.0 * int((left & live).sum()) / k,
                     int((measured & (gap >= T)).sum())))
    arr = np.array(rows)
    T, klive, s_nev, s_con, s_lef, n_gapkill = (arr[:, i] for i in range(6))

    # the T -> infinity limit
    lim = ~no_after
    kl = int(lim.sum())
    lim_sh = [100.0 * int((never & lim).sum()) / kl,
              100.0 * int((cont & lim).sum()) / kl,
              100.0 * int((left & lim).sum()) / kl]
    # the literal-bracket reading
    brk = measured
    kb = int(brk.sum())
    brk_sh = [100.0 * int((never & brk).sum()) / kb,
              100.0 * int((cont & brk).sum()) / kb,
              100.0 * int((left & brk).sum()) / kb]

    states = [("never_started", s_nev, lim_sh[0], brk_sh[0]),
              ("continued", s_con, lim_sh[1], brk_sh[1]),
              ("started_and_left", s_lef, lim_sh[2], brk_sh[2])]

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("Step 7 gate-closing diagnostic (decisions/0041 §4) — outcome shares against "
                 "the liveness threshold\n"
                 "NOT a study result. Step 8 has not launched and is an unapproved gate; "
                 "population and status are both provisional.",
                 fontsize=11.5, y=0.985)

    for ax, (name, curve, limv, brkv) in zip(axes.flat[:3], states):
        ci = boot["shares_with_clustered_intervals"]["threshold_1293d"][name]
        lo, hi = ci["clustered_95_ci_pct"]
        ax.axhspan(lo, hi, color="0.87", zorder=0,
                   label=f"95% account-clustered CI at T=1293 (width {hi - lo:.2f} pp)")
        ax.plot(T, curve, lw=1.8, color="#1f4e79", zorder=3, label="threshold rule")
        ax.axhline(limv, color="#c0392b", ls="--", lw=1.3, zorder=2,
                   label=f"parameter-free, T→∞ limit ({limv:.4f}%)")
        ax.axhline(brkv, color="#7d3c98", ls=":", lw=1.3, zorder=2,
                   label=f"parameter-free, literal bracket ({brkv:.4f}%)")
        for m in MARKS:
            v = curve[np.argmin(np.abs(T - m))]
            ax.plot([m], [v], "o", color="#e67e22", ms=6, zorder=4)
            ax.annotate(f"{m}d\n{v:.4f}%", (m, v), textcoords="offset points",
                        xytext=(6, 10), fontsize=8, color="#a04000")
        ax.set_title(f"{name.replace('_', ' ')} share (%)", fontsize=11)
        ax.set_xlabel("liveness threshold T (days)")
        ax.set_ylabel("share of live pairs (%)")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7.5, loc="best")

    ax = axes.flat[3]
    ax.plot(T, n_gapkill, lw=1.8, color="#1f4e79", label="excluded on a MEASURED gap ≥ T")
    ax.axhline(int(no_after.sum()), color="#c0392b", ls="--", lw=1.3,
               label=f"excluded on absent evidence, edge case (i): {int(no_after.sum())} "
                     f"— constant in T")
    for m in MARKS:
        ax.plot([m], [n_gapkill[np.argmin(np.abs(T - m))]], "o", color="#e67e22", ms=6)
    ax.set_yscale("symlog", linthresh=10)
    ax.set_title("what the threshold actually excludes, out of 147,370 pairs", fontsize=11)
    ax.set_xlabel("liveness threshold T (days)")
    ax.set_ylabel("pairs excluded")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="best")

    fig.tight_layout(rect=[0, 0, 1, 0.945])
    fig.savefig(os.path.join(ART, "step7-sensitivity-a.png"), dpi=140)

    sweep = {
        "what": "GATE-CLOSING SENSITIVITY DIAGNOSTIC for Step 7. NOT the Step 9 deliverable.",
        "instance": "sens_a", "api_calls": 0,
        "grid_days": [float(x) for x in T[::20]],
        "curve_never_started_pct": [round(float(x), 4) for x in s_nev[::20]],
        "curve_continued_pct": [round(float(x), 4) for x in s_con[::20]],
        "curve_started_and_left_pct": [round(float(x), 4) for x in s_lef[::20]],
        "sweep_range_days": [float(T.min()), float(T.max())],
        "share_range_over_whole_sweep_pp": {
            "never_started": round(float(s_nev.max() - s_nev.min()), 4),
            "continued": round(float(s_con.max() - s_con.min()), 4),
            "started_and_left": round(float(s_lef.max() - s_lef.min()), 4),
        },
        "share_range_over_the_clustered_interval_787_2200_pp": {
            n: round(float(c[(T >= 787) & (T <= 2200)].max()
                           - c[(T >= 787) & (T <= 2200)].min()), 4)
            for n, c, _, _ in states
        },
        "T_infinity_limit_shares_pct": {n: round(v, 4) for n, v in
                                        zip([s[0] for s in states], lim_sh)},
        "literal_bracket_shares_pct": {n: round(v, 4) for n, v in
                                       zip([s[0] for s in states], brk_sh)},
    }
    with open(os.path.join(OUT, "sweep.json"), "w") as fh:
        json.dump(sweep, fh, indent=2)
    print(json.dumps({k: sweep[k] for k in
                      ("share_range_over_whole_sweep_pp",
                       "share_range_over_the_clustered_interval_787_2200_pp")}, indent=2))


if __name__ == "__main__":
    main()
