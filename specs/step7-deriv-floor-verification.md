# Verification task — the DERIV started-and-left floor and Continued ceiling

**This is a verification, not a computation to be accepted.** A correction has been proposed by the
Human Lead. Your job is to **reproduce it from your own stored outputs, or to refute it.** Do not adopt
the proposed numbers because they are proposed. If your own outputs give something else, that is the
finding and you report it.

**This is not a gate step, not a rerun, and not a rule change.** The liveness rule is unchanged:
**ALT-BROAD** — a pair is not live iff **both** the account shows no insertion instant after `τ1`
**and** the pair is not Continued. Silence is anchored at `τ1` and only at `τ1`.

**Zero API calls.** Everything needed is on disk.

---

## Background, stated so the check is not blind

The started-and-left **floor** over the liveness exclusions was widened on **APPLY** (`decisions/0054`)
from 19,042 to **18,952 / 196,654 = 9.6372%**. The ground: 90 retained pairs are ¬Continued, live only
because they inserted after `τ1`, and had their **last insertion inside `(τ1, τ2)`**. Those pairs could
produce no evidence dated after that instant, so they **may in truth be Continued**, and a floor must
admit it.

**The same set exists on DERIV and the floor there was not widened.** That is the defect under review.

## What to compute

On **DERIV — Step 5 line 4 less D10, n = 147,370** — at **`W = 108`**, from your own `W = 108` outputs:

1. **The channel count** — pairs that are `¬Continued`, `|A| ≥ 1` (i.e. not never-started), and whose
   **last insertion instant lies in `(τ1, τ2)` — OPEN at `τ2`** (`0057`; it read `(τ1, τ2]`
   here and the closed form is wrong, not merely ambiguous: at `s = τ2` the unobserved remainder is
   empty, so nothing admissible is missing and the pair must not be conceded), where `τ1 = ⟦T0⟧ + W × 24h` and
   `τ2 = ⟦T0⟧ + (W + H) × 24h`, `H = 91`.
2. **The started-and-left floor under both extremes**, as a count and as a share of 147,370:
   - **extreme NONE** — no channel pair is in truth Continued
   - **extreme ALL** — every channel pair is in truth Continued
3. **The started-and-left ceiling**, and whether it moves between the two extremes.
4. **The Continued ceiling** under extreme ALL, as a count and a share of 147,370.
5. The same four quantities on **APPLY — line 1 less D10, n = 196,654** — so the two populations are
   stated side by side.

## The proposed correction, to be confirmed or refuted

| DERIV, n = 147,370 | Proposed |
| :--- | ---: |
| channel count | **89** |
| S&L floor, extreme ALL | **16,655 → 11.3015%** |
| S&L floor, extreme NONE | 16,744 → 11.3619% |
| S&L ceiling | 16,843 → 11.4291% *(unchanged between extremes)* |
| Continued ceiling, extreme ALL | **121,570 → 82.4930%** |

State for each row: **confirmed**, or **refuted with your own figure.**

## Two questions to answer in your own terms

- **Does the endpoint move between the extremes?** Report the movement in pp on both populations. If it
  does not move, say so — the choice would then be numerically empty.
- **Is the widened floor the right endpoint on the ground stated above?** The ground offered is that a
  floor must cover the case the filter exists to guard against. A margin argument was also offered —
  that the 90 had ample opportunity to produce Continued evidence and did not — and the Human Lead has
  **withdrawn it as cherry-picked** (p5 = 1.7 days was quoted; the median for the same pairs is 44.5).
  **Say whether you think any margin statistic belongs in an endpoint's justification at all.** Argue
  it; do not defer.

## Rules

- **Every figure states which population produced it, at the point of use.** An unlabelled figure is a
  defect.
- **Do not read the other instance's output folder, and do not ask about it.** The Human Lead diffs.
- **Do not edit `task-sheet.md` or any agent definition file.** The spec propagation is assigned
  elsewhere. If you find a spec file that contradicts your own result, **report it as a defect; do not
  fix it.**
- If your own stored outputs are insufficient to answer a row, **say so** rather than reconstructing it
  from a source you cannot check.

## Deliverable

Write **`artifacts/step7-deriv-floor-check-<your namespace letter>.md`** and the matching `.json`, then
report the path and a two-line summary, and **stop.**
