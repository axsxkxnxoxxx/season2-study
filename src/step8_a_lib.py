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
import numpy as np

DAY = 86400
MUL = 2 * 10 ** 11
OFF = 10 ** 11
TAU_PULL = int(np.datetime64("2026-08-11T00:00:00", "s").astype("int64"))

NEVER, LEFT, CONT = 0, 1, 2


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
        p[sel] = self.cum[self.pair_slot[sel], mH[sel]] / self.L2[sel]

        return dict(W=W, tau1=tau1, tau2=tau2, keep_term1=keep_term1, keep_d10=keep_d10,
                    pos5=pos5, pos5_deriv=pos5_deriv, kA=kA, kAH=kAH, mH=mH, mA=mA,
                    outcome=outcome, continued=continued, never=never, left=left,
                    silent=silent, not_live=not_live, live=live, p=p)
