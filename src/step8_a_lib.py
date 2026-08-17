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
#
# THE ENTRY THIS BUILD IS LAUNCHED AGAINST IS `0093` -- a ruling is not closed until the ARTIFACTS
# carry it. The previous build of this arm was tagged 0092 and reported, as a finding, that 0092
# had NO FILE in decisions/. THAT FINDING IS NOW CLOSED: the entry exists. It is not asserted
# closed from memory -- the surface-state block in step8_a_5_diagnostics.py counts the files on
# disk on THIS run and the deliverable's reading is DERIVED from that count, which is exactly the
# defect 0093 was written against: a claim about a surface that was true when written, published
# by a rerun that could have contradicted it.
BUILD_TAG = "a/2026-08-16-0093"
BUILD_NAME = ("position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0093 -- a "
              "ruling is not closed until the artifacts carry it -- together with Red Team's "
              "EIGHTH pass, which closed every blocker against this arm and left three minor "
              "items, all three against this arm's own text rather than its arithmetic")
# The long form lives in build_record()["what_moved_on_this_build"], stated ONCE. BUILD_NAME is
# quoted at every point of use, so a paragraph there is a paragraph repeated forty times -- and a
# stamp that buries the figure it stamps is worse than a short one that points at it.
WHAT_MOVED = (
    "THREE THINGS MOVE, none of them a population, a rule, a waterfall line, an outcome share, a "
    "bound endpoint, an invariant RESULT or any measured count. All three are Red Team's "
    "eighth-pass minor items against this arm, and all three are about TEXT THIS ARM PUBLISHED "
    "rather than about what it computed. "
    "(A) A HARDCODED CONCLUSION STRING SAT BESIDE LIVE COUNTS. The surface-state block measured "
    "four surfaces on disk at run time and then published a fixed sentence -- '0092's N2 edit "
    "reached surface 1 and no other' -- which a rerun can contradict and DID: the agent files and "
    "second-brain now carry the correction, and decisions/0092 now has a file. The READING IS NOW "
    "DERIVED FROM THE MEASUREMENT, per-surface, with both the stale form and the corrected form "
    "counted on every surface (CLAUDE.md's negative AND positive halves). SS9 items 20 and 21 are "
    "regenerated from those counts and now report CLOSED. THIS IS decisions/0093's OWN MECHANISM "
    "SEEN FROM INSIDE AN ARM: the ruling was recorded, propagated and passing every control while "
    "this arm's artifact still published the superseded reading, because an artifact only changes "
    "on a run. "
    "(B) THE FALSIFIABILITY HEADLINE IS AN ARM-AGAINST-ARM DIVERGENCE AND NEITHER ARM FLAGGED IT. "
    "This arm publishes a THREE-WAY split over the nine labels -- 6 pure CODE CHECK + 1 CODE CHECK "
    "BY CONSTRUCTION/DATA CHECK AS SPECIFIED + 2 DATA CHECK -- derived from the label strings, and "
    "the spec's own sentence is three-way. The other arm publishes a TWO-WAY split over the same "
    "nine labels. REPORTED AS A DIVERGENCE, NOT RECONCILED, and this arm does not read the other "
    "arm's output: the fact is carried from Red Team's eighth pass. "
    "(C) THE SYMMETRIC-DIFFERENCE-0 WARRANT WAS ONE NOTCH STRONGER THAN THE MONOTONICITY ALLOWS. "
    "The measurement is right and unchanged; the sentence 'a total that does not move can still be "
    "a different set of rows, and that is what the symmetric difference rules out' is WITHDRAWN. "
    "The date-level counterfactual RELAXES both bounds, so A and A_H only gain episodes; all three "
    "Continued conjuncts are monotone in them; so the counterfactual exclusion set is a SUBSET of "
    "the adopted one and an unchanged TOTAL already forces set equality. The subset direction and "
    "each conjunct's monotonicity are now MEASURED and emitted rather than argued, and the "
    "symmetric difference is labelled as CONFIRMING THE ARITHMETIC, not as independent evidence. "
    "PRIOR BUILD a/2026-08-16-0092 MOVED SEVEN THINGS, none of them a population, a rule, a "
    "waterfall line, an outcome share, a bound endpoint or an invariant RESULT. Six were Red "
    "Team's seventh-pass findings against this arm; the seventh was decisions/0092's N2 "
    "requirement. They are retained here because a build record that drops what an earlier build "
    "corrected cannot tell a fix from a drift. "
    "(1) THE 'INERT ON LINE 6' WARRANT IS WITHDRAWN and the claim is rescoped. The previous "
    "deliverable said line 6 does not move under the date-level counterfactual 'because the "
    "silence test reads an insertion clock, not an episode timestamp'. That is a property of "
    "CONJUNCT 1 and cannot explain the invariance of a CONJUNCTION whose second conjunct is NOT "
    "Continued -- an episode-timestamp computation that moves on 55 APPLY rows under this very "
    "counterfactual. WHAT WAS MEASURED IS NOW STATED: conjunct 2 IS recomputed on the "
    "counterfactual outcome (`silent & ~cont_`, cont_ from the counterfactual state function), so "
    "703 -> 703 is a measurement and not a tautology -- and the 604/99 SPLIT under every "
    "counterfactual form is now reported, on both populations, which it was not. The invariance is "
    "a FACT ABOUT THIS DATA at W = 108, not a structure. "
    "(2) THE '1 EPISODE AT tau1' ATTRIBUTION IS WITHDRAWN -- WRONG OBJECT. decisions/0068's "
    "strictness ruling is about INSERTION INSTANTS in the silence test; the 1 is a distinct S2 "
    "EPISODE by canonical watched_at, which is the unit of the SS5.6a table. The ruling's OWN "
    "quantity -- accounts whose last insertion instant falls exactly AT tau1 -- is measured here "
    "for the first time in this arm, on both populations. "
    "(3) THE `+1` PERTURBATION DOES NOT TEST INDEPENDENCE. On a same-mask denominator the clauses "
    "sum to N and the stated population reads N + 1, so it fires identically -- it would have "
    "passed on the very build whose defect it claimed to fix. It is RELABELLED as what it is (the "
    "identity is arithmetic, not a literal) and a REAL independence control is added: injected "
    "wrong-population defects, each asserting that the same-mask form PASSES and the "
    "independently-sourced form FAILS. "
    "(4) `p_at_bound`'s FALSE CARDINALITY IS EMITTED, on all four populations, and the TWO "
    "DIFFERENT FALSE CLASSES on that page are named apart: the COEXTENSIVITY-GAP class (0082's "
    "superseded two-mechanism definition), which is EMPTY, and the COLUMN's own FALSE value "
    "(Started-and-left below the bound), which is 17,895 on APPLY position 5. "
    "(5) THE PER-SITE D11 TABLE'S S1_completion_walk 'examined' CELL held a different quantity "
    "from the other twelve rows -- 73 is a RECORD count of the post-cutoff candidates, not an "
    "examined count, and the walk's unit is DISTINCT S1 EPISODES. All three objects are now named "
    "and the examined column is the same kind of quantity in every row. "
    "(6) D2's 'both bind' COUNT NOW CARRIES ITS POPULATION AT THE POINT OF USE AND IS MEASURED ON "
    "BOTH POPULATIONS AT BOTH POSITIONS (decisions/0092, N2), and the combined waterfall's DERIV "
    "line 4 is RELABELLED: it is not a single filter, it is Step 5 lines 1 through 4 and its "
    "sub-decomposition is emitted. "
    "(7) A CLAIM THIS ARM PUBLISHED ABOUT ITS OWN SOURCE WAS FALSE: 'no .date(), dt.date, "
    "normalize() or day-flooring anywhere in step8_a_*.py'. floor_day() appears three times in "
    "step8_a_2_positions.py, legitimately -- [[T0]] is day-floored by Step 1 SS2.4 and SS5.6a's "
    "own argument depends on it. The claim is corrected to the true and narrower one: no "
    "day-flooring in any BOUNDARY TEST. "
    "PRIOR BUILDS OF THIS INSTANCE: a/2026-08-16-0092 (what Red Team's EIGHTH pass reviewed), "
    "a/2026-08-16-0090 (sixth and seventh), a/2026-08-16-0088 (fifth), a/2026-08-16-0085 "
    "(fourth), the pre-0085 run (third).")
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
        "what_moved_on_this_build": WHAT_MOVED,
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
        "spec_read": "task-sheet.md Step 8 as it stands, plus decisions/0066-0093",
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
