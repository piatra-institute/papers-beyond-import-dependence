# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-08-16 — v1, first full draft to publication

Scope: the entire paper, simulation, and evidence base, from the seed chat to publication.

Changes:
  - Sources: 29 entries verified against Crossref or the live institutional record. The 2026 anchors fetched at first hand this session: the manufacturer's annual report figures, the optics supplier's part counts, the three Reuters reports of June, March, and July 2026, the energy agency's concentration and inverter figures, the vulnerability index table with its authors, the accountability office's capacity series, the resilience review's relocalisation estimates, and the export-control categories. Seed corrections logged in research.md: the unverified metrology system count dropped, the extreme ultraviolet prototype timeline replaced with attributable reporting, the component count replaced by the supplier count from the primary record, and the regional score table treated as priors rather than findings. The seed's proposed empirical design is described as the programme the framework implies rather than claimed as executed.
  - Simulation design iterations logged: the capability dynamic first saturated at the bounds because gains were undamped, and was rewritten with growth damped by the room left and drains proportional to the stock, which is also what lets a break-even absorption exist; the two topologies were initially built at different mean burdens, so the comparison proved nothing until the means were equalized at 0.237 by construction; the policy allocator's first ordering key was constant across nodes, so every instrument spent on whatever came first in the list, and the corrected allocator spends on the largest reducible risk and skips nodes an instrument cannot touch; the single-budget policy comparison was replaced by a budget sweep after it became clear the answer depends on whether the budget can close a whole chokepoint, which is a finding rather than a nuisance.
  - Honest results kept rather than tuned away: blanket relocalization scores best in the underfunded depth window, reported with the cited macroeconomic cost the model does not charge it; the trade index reaches 0.80 rank correlation on the transparent subset, where the capability machinery earns little; and the never-lost capability level is unreachable behind a protective wall, which cuts against the reflex the diagnosis invites.
  - Voice: draft came in at 0 errors, 13 review-candidates; 13 negate-pivots rewritten, "exactly" thinned 7 to 4, and a 25-sentence run without a short sentence broken to 18.
  - Refs: the gate's bibliography parser keys on the literal first token while the in-text parser skips ALL-CAPS tokens, so an acronym-led corporate entry can never match; the annual report is therefore carried as a title-led reference and identified in the prose that uses it, and the optics supplier is cited under its full company name.

Verification:
  - voice: 0 errors, 0 review-candidates
  - refs: 26 in-text keys, 29 bib entries, 0 missing, 0 unused
  - claims: 739 sim values, 37 decimal claims in prose, 0 without a match
  - build: 14 pages, no missing-character warnings
  - simulation: 37/37 invariants
  - check => PASS
