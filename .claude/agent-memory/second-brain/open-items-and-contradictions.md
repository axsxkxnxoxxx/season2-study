---
name: open-items-and-contradictions
description: Live register of open items, blockers and cross-step contradictions in the Season 2 study, with the two conflicting sources named for each — as of the Step 1 gate close 2026-08-10
metadata:
  type: project
---

# Open items and contradictions — as of 2026-08-10, Step 1 gate closed

**Why this file exists:** Second Brain surfaces contradictions and names the two things that
conflict. It does not decide, arbitrate, or fix. Every entry below names its two sources so
the Human Lead can rule without re-reading the corpus.

**How to apply:** re-check each entry against the files before raising it — several will be
closed by ordinary progress rather than by a decision. Status as of 2026-08-10.

---

## C1. The Step 4 endpoint decision is open in one artifact and presupposed in another

- `artifacts/step0-access-and-setup.md` §0 and §6 item 1: `/users/:id/watched/shows` returns a **show-level aggregate with no per-episode timestamps** under Client-ID-only auth, and it paginates (`limit` silently clamped at 250). The Analytics Engineer stopped rather than substituting an endpoint. The endpoint decision is listed as **open and blocking Step 4**.
- `artifacts/step1-outcome-definition.md` §0, first line: "**Source, decided by the Human Lead:** `GET /users/:id/history`, unfiltered, one sweep per user."

Step 1's entire definition is built on a source that the Step 0 artifact still lists as an
undecided, blocking question. Either Step 0's open-items list is stale, or Step 1 records a
decision that exists nowhere in writing. **Nothing in `decisions/` records it** — that folder
holds only `.gitkeep`. Either way this is a missing Step 18 entry: the Step 4 endpoint choice
has no decision-log record, and it is one of the larger decisions taken so far.

## C2. Two figures in an approved public artifact have no public source

- `artifacts/step1-outcome-definition.md` §2.1: "The Step 0 probe found **123 records covering 96 distinct `(season, number)` pairs** on a single profile — 28 percent inflation, with 25 episodes appearing more than once." §5: "On the probe profile, **the first S2 watch preceded the last S1 watch by six weeks**."
- Neither figure appears in `artifacts/step0-access-and-setup.md` or in `artifacts/step0-episode-listing-endpoint-probe.md`. Those are the only two public Step 0 documents, and both cite their own run records.

The only trace is `logs/api_requests.ndjson`, which carries **two GET calls tagged
`run: step0-history-probe` at 2026-08-10T21:02Z** — one per-show-filtered history call and one
unfiltered history call, both HTTP 200. `logs/` is gitignored and never leaves the machine.
Unlike the other two Step 0 probes there is **no run record JSON** and **no probe script in
`src/`**, so the run is not reproducible from the repo.

Arithmetic verified: `(123 − 96) / 96 = 28.1%`. The figures are correct. The problem is
sourcing, on a public artifact, in support of two definitional choices — distinct-episode
counting (§2.1) and first-pass completion (§5).

Mitigating, and worth stating when this is raised: **neither rule depends on the figure.**
"Count distinct episodes, never play events" is independently in the `task-sheet.md` Step 1
checklist, and first-pass completion is defended in §5 on the merits, explicitly *not* on the
result. The figures are rhetorically load-bearing, not logically load-bearing.

## C3. `pull_date` has no value — the one outstanding blocker from Step 1

Adopted in **form** (D11), value **deliberately deferred** to Step 4's schedule. Human Lead
act; no agent performs it. Constraint: `pull_date ≤ earliest per-user fetch date in the whole
Step 4 sweep`. **Any step that right-censors, or that computes D3, D8 or D9, is blocked on
this value** — not on the Step 1 gate, which is closed.

## C4. The gap hypothesis is untested and belongs to no step

`artifacts/step1-outcome-definition.md` §3.3 and §11, and the probe's own §7: the episode-listing
probe covered **one show with contiguous numbering**. It confirms payload shape and auth, not
how Trakt represents a numbering gap. If Trakt lists a **placeholder** at the missing number
rather than omitting it, then `number ∈ E` for a non-existent episode, the drop rule readmits
exactly the case the set rule was built to exclude, and `L := |E|` counts an episode that does
not exist.

**Section 3 must not be read as "gaps handled."** What it buys is `D1 ⊆ E1` and `A ⊆ E2`
*relative to whatever `E` Trakt lists* — sufficient for the §3.2 invariants and for
`p ∈ (0, 1]`, and **not** a claim that gapped seasons are measured correctly.

The contradiction of ownership: the document assigns settling it to "wherever `E` is first
pulled at scale", which is not a step in `task-sheet.md` and has no owner. It requires finding
an in-frame show with a known numbering gap and inspecting its payload.

## C5. Step 6's estimation sample is specified two different ways, on a dual-implementation gate

- `task-sheet.md` Step 6: "Restrict to users who did start S2" and "Anchor the lag on the S2 finale date, not the premiere, **for weekly-release shows**" — i.e. all shows, weekly ones included.
- `artifacts/step1-outcome-definition.md` §9 (handoff to Step 6): the D12 classifier, "which, under open question 2's recommendation, *is* the estimation sample, so it must be applied as written rather than paraphrased." §10.1 Q2 recommends **C1 (all-at-once) only**.
- `artifacts/step1-outcome-definition.md` §10.1 also states these questions are **not closed by approval**, and §8 states the treatment of negative lags in the Step 6 lag distribution "stays open."

So Q2 is the one open question with **no drafted default in the body to fall back on**. §10.1's
own fallback rule — "until then the drafted boundary is what the document says" — has nothing
to point at for Q2.

**Why this is urgent rather than tidy:** Step 6 is a gate *and* runs dual implementation. The
two isolated instances read `task-sheet.md`, which says all shows. Step 1 §9 says C1-only. The
two instances could produce different `W` values from faithful readings, and the diff would
prove nothing — which is precisely the failure the dual-implementation rule exists to prevent.
The document itself names this risk for the *old* cadence wording; the same risk now sits on
the estimation sample. **This wants a Human Lead ruling on Q2 before Step 6 is dispatched.**

## C6. Two Step 8 obligations from Step 1 are not in Step 8's own checklist

`task-sheet.md` Step 8 enumerates the filters as "frame, contamination exclusions, S1
completion rule, W, and liveness rule". Step 1 adds two things that land at Step 8 and appear
in neither that list nor Step 8's checklist:

1. **Right-censoring.** Step 1 §6 imposes an ordering constraint on it (Step 5 contamination exclusion runs **before** right-censoring) and requires its removal reported as **two lines** in the waterfall — the `max(W, 91)` term and the incremental `+ H` term. But right-censoring is not named as a filter in Step 8 at all.
2. **The `L2 = 1` exclusion.** Step 1 §7 excludes those pairs from the headline population at Step 8 with counts reported. Not in Step 8's checklist.

Both reach Step 8 only through Step 1 §9's handoff list. Step 8 is a dual-implementation gate,
so the same divergence logic as C5 applies, more weakly.

## C7. Critical path, for sequencing awareness

`Step 4 endpoint decision (C1)` → Steps 3 and 4 → **`pull_date` value (C3)** → Step 5 gate →
Steps 6 and 7 gates → Step 8 gate. `task-sheet.md` says Steps 3 and 4 are the long pole and
should start first; `artifacts/step0-access-and-setup.md` says Step 4 cannot be built until
C1 is resolved. The long pole is behind an unrecorded decision.

---

## Checks that PASS — recorded so they are not re-litigated

Verified against `artifacts/step1-outcome-definition.md` on 2026-08-10:

- **Censoring clearance does not cost any show.** 31 Dec 2024 (frame cap on the S2 finale) + `max(W,91) + H` = +182 days at `W ≤ 91` ≈ mid-2025, inside a 2026 pull. Correct as §6 states.
- **The `+H` cost estimate is right.** An Aug 2026 pull moves the effective S1-completion cutoff from about May 2026 to about Feb 2026.
- **The 91-day arm sits inside the primary censored population.** `T0' + 91 + H ≤ T0 + 91 + H ≤ T0 + max(W,91) + H ≤ pull_date`, since premiere ≤ finale and `91 ≤ max(W,91)`. Holds.
- **D12 is exhaustive and mutually exclusive** for `span ≥ 0` under first-match ordering; C0 absorbs missing and `span < 0`. Verified by case split.
- **`(123 − 96)/96 = 28.1%`** — the §2.1 figure is arithmetically right (its sourcing is C2).
- **The boundary convention is used consistently.** `watched_at < τ1` in §2.4, §7, D3, D8, and the complement `watched_at ≥ τ1` for the Step 7 liveness test in §9. No second reading survives anywhere in the document. `date(watched_at) ≤ T1` appears only where it is being withdrawn.
- **Directions are declared in both senses.** The two one-day effects offset: D13's half-open window moves the never-started share **up**, the §0 UTC finale skew and the `τ0 := ⟦T0⟧` effect move it **down**. Neither is corrected against the other; both are stated. Consistent across §0, §2.4, §6.
- **Privacy boundary is intact.** `.gitignore` covers `.env`, `raw/`, `processed/`, `logs/`. No username, user ID or individual watch history appears in any file in `artifacts/` or `decisions/`. One username does appear in an endpoint path in `logs/api_requests.ndjson`, which is correct — that folder is machine-local.

## One edge case, harmless today, noted so it is not discovered later

At `L2 = 1`, `weekly_span = 0`, so `span ∈ {2, 3}` falls through C1 and lands in **C2
"weekly"** under D12. Harmless **only because** `L2 = 1` shows are excluded from the headline
population (§7). But the exclusion happens at Step 8 and the classification is available from
Step 2 onward, so anyone classifying before excluding will see nonsense weekly buckets. Order
matters here and is not written down anywhere.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[decision-log-step18]], [[withdrawn-claims-register]].
