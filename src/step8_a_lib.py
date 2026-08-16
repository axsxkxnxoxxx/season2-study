"""Step 8, namespace `a`. Shared arm logic.

One place computes the clock, the two outcome instants, the outcome states and the liveness
rule, so the W = 108 table and the Step 13 arms cannot drift apart. GATE: adopts nothing.
Zero API calls.

THE OPERATORS, each with the line that fixes it:

  tau1 = [[T0]] + W*24h,  tau2 = [[T0]] + (W+H)*24h            Step 1 SS2.4, SS7 as amended by 0034
  A    = {distinct S2 episodes, number in E2, canonical ts < tau1}     half-open, STRICT `<`
  A_H  = the same set read at tau2                                     A subset A_H since tau1 < tau2
  Never started      |A| = 0
  Continued          |A| >= 1  and  F2 in A_H  and  |A_H| >= ceil(0.90*L2)
  Started and left   |A| >= 1  and not Continued
  p (S&L only)       |{e in E2 : e <= max(A_H)}| / L2                  rank form, NOT m_H/L2

  NOT LIVE iff (no insertion instant > tau1) AND (NOT Continued)       ALT-BROAD, 0048/0054/0064
      -- "after" is STRICT (0068): an instant exactly AT tau1 does not make the account live
      -- evidence restricted to records dated before tau_pull (0070 ruling 2)

`date(watched_at) <= T1` appears nowhere: every bound is an instant comparison.
"""
import hashlib
import os
import subprocess

import numpy as np

DAY = 86400
MUL = 2 * 10 ** 11
OFF = 10 ** 11
TAU_PULL = int(np.datetime64("2026-08-11T00:00:00", "s").astype("int64"))

NEVER, LEFT, CONT = 0, 1, 2

ROOT = "/Users/alyanashantel/Documents/season2-study"
SRC = os.path.join(ROOT, "src")

# ---------------------------------------------------------------------------------------------
# PROVENANCE. Every count, every invariant result and every waterfall figure carries the BUILD it
# was measured on -- Human Lead ruling, decisions/0079 (B6), extending decisions/0078. A count
# without its provenance can be correct when written and wrong when read, because the pipeline
# moved underneath it and nothing in the text says which pipeline it belongs to. Partial
# application is worse than none: two labelled figures imply the rest did not need it.
#
# The tag below is what appears at each point of use; this record is the one full definition.
# ---------------------------------------------------------------------------------------------
# THREE BUILDS NOW EXIST ON 2026-08-16 -- the run Red Team's third pass reviewed, the rerun
# against decisions/0085 that its fourth pass reviewed, and THIS rerun against decisions/0088.
# A shared tag would make every figure ambiguous between them, which is the exact failure the
# provenance rule exists to prevent, so the tag carries the entry it was run against.
#
# THE BUILD-TAG FORMAT IS STATED, because Red Team's fourth pass (0087 F5-F9, item F7) recorded
# that the convention is unstated free text and the Human Lead's diff cannot key on it. This
# instance's format is `<instance>/<UTC run date>-<decision entry the run was launched against>`.
# It is NOT the git commit: the worktree is dirty at launch by construction, since the stage
# files are edited for the entry the run implements, so the commit does not identify the code.
# The stage-file SHA-256 prefixes in build_record() are what identify the code, and they are
# emitted with every build record. F7 is a carried limitation, not a ruling; this states the
# convention rather than proposing one.
BUILD_TAG = "a/2026-08-16-0088"
BUILD_NAME = ("position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 "
              "(B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage "
              "quantities named as separate objects and the mislabel corrected; the D9 clustering "
              "universe ruled to U1, ranked by distinct strict keys merged). The earlier "
              "2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- "
              "are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE "
              "MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is "
              "computed on was ruled and this instance's previous universe was the D9 coverage "
              "pivot rather than the sweep. They are different builds and are tagged apart.")
STAGE_FILES = ["step8_a_lib.py", "step8_a_1_scan.py", "step8_a_2_positions.py",
               "step8_a_3_table.py", "step8_a_4_arms.py", "step8_a_4b_slugs.py",
               "step8_a_5_diagnostics.py", "step8_a_6_emit.py", "step8_a_run.py"]


def _sha(path, n=12):
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()[:n]
    except OSError:
        return None


def build_record():
    """The one full definition of this build. Cited by BUILD_TAG everywhere else."""
    try:
        head = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, timeout=20).stdout.strip()
        dirty = bool(subprocess.run(["git", "-C", ROOT, "status", "--porcelain"],
                                    capture_output=True, text=True, timeout=20).stdout.strip())
    except Exception:
        head, dirty = None, None
    return {
        "build_tag": BUILD_TAG,
        "build_name": BUILD_NAME,
        "instance": "a",
        "run_date_utc": "2026-08-16",
        "why_this_exists": "decisions/0079 (B6), extending decisions/0078: every count, every "
                           "invariant result and every waterfall figure names the pipeline it was "
                           "measured on, not only its population. Partial application is worse "
                           "than none.",
        "pipeline": "src/step8_a_run.py, one run, stages 1 -> 6 in order",
        "stage_files_sha256_12": {f: _sha(os.path.join(SRC, f)) for f in STAGE_FILES},
        "git_head_short": head,
        "git_worktree_dirty_at_launch": dirty,
        "parameters": {"W_days": 108, "H_days": 91,
                       "tau_pull_utc": "2026-08-11T00:00:00Z",
                       "filter_order": "decisions/0029, positions 1-7",
                       "liveness_rule": "ALT-BROAD (0048/0054, approved 0064)",
                       "arm_grid_days": [38, 46, 77, 91, 107, 108, 150, 213]},
        "inputs": {"processed/step5/full_scan.npz": "size %d bytes, mtime %d (not hashed: 1.05 GB)"
                   % (os.path.getsize(os.path.join(ROOT, "processed/step5/full_scan.npz")),
                      int(os.path.getmtime(os.path.join(ROOT, "processed/step5/full_scan.npz")))),
                   "processed/step5/calibration.npz": _sha(
                       os.path.join(ROOT, "processed/step5/calibration.npz")),
                   "processed/step5/pair_revision5.csv": _sha(
                       os.path.join(ROOT, "processed/step5/pair_revision5.csv")),
                   "processed/step2/frame.csv": _sha(os.path.join(ROOT, "processed/step2/frame.csv")),
                   "processed/step4/pull_ledger.jsonl": _sha(
                       os.path.join(ROOT, "processed/step4/pull_ledger.jsonl"))},
        "spec_read": "task-sheet.md Step 8 as it stands, plus decisions/0066-0085",
        "relation_to_the_2026_08_13_build": "this build reproduces the figures decisions/0078 and "
                                            "0079 restate on the position-5 build of 2026-08-13 "
                                            "(58,345 pairs; 324 of 5,694; 178 of 2,549; 703/99). "
                                            "Where a figure agrees, that is measured here and "
                                            "stated, not carried.",
    }


class Arms:
    def __init__(self, scan, positions, frame, H=91):
        self.H = H
        self.pair_user = scan["pair_user"]
        self.pair_show = scan["pair_show"]
        self.n = self.pair_user.size
        self.s2_ptr = scan["s2_ptr"].astype(np.int64)
        self.s2_num = scan["s2_num"]
        self.s2_ts = scan["s2_ts"].astype(np.int64)
        self.s2_prefmax = scan["s2_prefmax"]
        self.s1_ptr = scan["s1_ptr"].astype(np.int64)
        self.s1_ts = scan["s1_ts"].astype(np.int64)
        self.has_s3 = scan["has_s3"]
        self.act_counts = scan["act_counts"]

        self.t0 = positions["t0"].astype(np.int64)
        self.pos3 = positions["pos3"]
        self.pos4 = positions["pos4"]
        self.pos4_deriv = positions["pos4_deriv"]
        self.L2 = positions["L2"].astype(np.int64)
        self.need2 = np.ceil(0.90 * self.L2).astype(np.int64)

        f = frame.set_index("show_trakt_id")
        self.F2 = f.s2_F.reindex(self.pair_show).to_numpy().astype(np.int64)

        # cumulative |{e in E2 : e <= n}| per show, for the rank form of p
        shows = f.index.to_numpy()
        maxnum = int(max(max(int(x) for x in str(s).split(",") if x.strip().isdigit())
                         for s in f.s2_E))
        cum = np.zeros((shows.size, maxnum + 2), dtype=np.int16)
        for i, s in enumerate(f.s2_E):
            for e in (int(x) for x in str(s).split(",") if x.strip().isdigit()):
                cum[i, e] = 1
        cum = np.cumsum(cum, axis=1)
        slot = np.full(int(shows.max()) + 1, -1, dtype=np.int64)
        slot[shows] = np.arange(shows.size)
        self.cum = cum
        self.pair_slot = slot[self.pair_show]

        # account-level last insertion instant, D11-restricted (0070 ruling 2)
        uids = scan["uids"]
        uslot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
        uslot[uids] = np.arange(uids.size)
        self.last_inst = scan["last_inst_d11"][uslot[self.pair_user]]
        self.last_inst_unrestricted = scan["last_inst_all"][uslot[self.pair_user]]

        # searchsorted key: rows are already sorted by (pair, canonical ts)
        self.s2_key = (np.repeat(np.arange(self.n, dtype=np.int64), np.diff(self.s2_ptr)) * MUL
                       + (self.s2_ts + OFF))
        self.pair_base = np.arange(self.n, dtype=np.int64) * MUL

    def count_before(self, bound):
        """Per pair, the number of distinct S2 episodes whose canonical timestamp is < bound."""
        idx = np.searchsorted(self.s2_key, self.pair_base + (bound.astype(np.int64) + OFF),
                              side="left")
        return idx - self.s2_ptr[:-1]

    def maxnum_before(self, k):
        """max(A) for the first k episodes of each pair; 0 where k == 0."""
        out = np.zeros(self.n, dtype=np.int64)
        nz = k > 0
        out[nz] = self.s2_prefmax[self.s2_ptr[:-1][nz] + k[nz] - 1]
        return out

    def run(self, W):
        """Positions 5, 6 and 7 at this W. Positions 1-4 do not contain W."""
        H = self.H
        t0 = self.t0
        tau1 = t0 + W * DAY
        tau2 = t0 + (W + H) * DAY

        keep_term1 = (t0 + max(W, 91) * DAY) <= TAU_PULL
        keep_d10 = (t0 + (max(W, 91) + H) * DAY) <= TAU_PULL
        pos5 = self.pos4 & keep_d10
        pos5_deriv = self.pos4_deriv & keep_d10

        kA = self.count_before(tau1)
        kAH = self.count_before(tau2)
        mH = self.maxnum_before(kAH)
        mA = self.maxnum_before(kA)

        continued = (kA >= 1) & (mH == self.F2) & (kAH >= self.need2)
        never = kA == 0
        left = (kA >= 1) & ~continued
        outcome = np.where(never, NEVER, np.where(continued, CONT, LEFT)).astype(np.int8)

        silent = self.last_inst <= tau1            # "after tau1" is STRICT
        not_live = silent & ~continued
        live = ~not_live

        p = np.full(self.n, np.nan)
        sel = left & (kAH > 0)
        # the RANK NUMERATOR |{e in E2 : e <= m_H}|, kept as its own array because `p_at_bound`
        # is defined on it. decisions/0083 SS2 restates the column: it marks WHETHER p reached its
        # bound, not why -- 0082's two mechanisms are COEXTENSIVE by construction, since set
        # membership puts m_H in E2 and the numerator is L2 iff m_H = max(E2) = F2. Both clauses
        # are still computed separately, so the emptiness of the FALSE class is MEASURED at every
        # arm rather than asserted; it is W-invariant, so a FALSE row anywhere means the rank form
        # or the set-membership rule has broken.
        p_num = np.full(self.n, -1, dtype=np.int64)
        p_num[sel] = self.cum[self.pair_slot[sel], mH[sel]]
        p[sel] = p_num[sel] / self.L2[sel]
        p_saturated = sel & (p_num == self.L2)          # rank numerator at its bound L2
        p_final_ep = sel & (mH == self.F2)              # left at the final episode F2 = max(E2)

        return dict(W=W, tau1=tau1, tau2=tau2, keep_term1=keep_term1, keep_d10=keep_d10,
                    pos5=pos5, pos5_deriv=pos5_deriv, kA=kA, kAH=kAH, mH=mH, mA=mA,
                    outcome=outcome, continued=continued, never=never, left=left,
                    silent=silent, not_live=not_live, live=live, p=p, p_num=p_num,
                    p_defined=sel, p_saturated=p_saturated, p_final_ep=p_final_ep)
