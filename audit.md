# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-23 — structured-evidence migration

Structured-evidence migration (references and claims).
- references.yaml: 30 CSL entries. 14 with DOIs resolved through doi.org content negotiation (10 matched automatically in Crossref; brusoni2001, carvalho2021, dong2016 and oecd2025 assigned by hand from Crossref searches). 16 entered by hand: nelson1982, pisano2012, polanyi1966 (books) and asml2026, bis2024, cpc2025, doe2025, gao2025, iea2026a, iea2026b, reuters2026a-c, safran2026, unido2026, zeiss2026 (institutional and press sources, with URLs). Organisation ids renamed (bureau2024 -> bis2024, central2025 -> cpc2025, department2025 -> doe2025, government2025 -> gao2025, international2026a/b -> iea2026b/a, organisation2025 -> oecd2025, united2026 -> unido2026, carl2026 -> zeiss2026). Citeproc orders the two IEA 2026 works by title, so the inverter commentary renders as 2026a and the ETP chapter as 2026b (swapped relative to the legacy letters); ids follow the rendered letters.
- Correction: Dong and Mirza (2016) figure "as much as 70 to 90 percent of medicines consumed in most of sub-Saharan Africa" -> "an estimated 79 percent of pharmaceuticals used in Africa" (PMC4709802 full text); the requirements clause now names what the editorial names (regulatory authority, quality-assurance systems, trained people). The cited record in simulation/analyses.py changed accordingly (who_africa_medicine_imports_low/high_pct 70/90 -> who_africa_pharmaceuticals_imported_pct 79); the rerun changed only that cited record in results.json.
- Correction: acemoglu2012 DOI record has no authors; authors entered from the article. Connell Garcia's name split corrected (family Connell Garcia). Titles cleaned of footnote asterisks.
- claims.yaml: 75 claims (48 computation, 19 source, 2 definition, 2 assumption, 3 interpretation, 1 normative); computation claims bound to simulation/output/results.json run model. Source claims checked against Crossref/OpenAlex abstracts, PMC full text, and the institutional pages and PDFs (ASML annual report, ZEISS, BIS, GAO via Internet Archive, DOE, IEA x2, CPC recommendations, UNIDO report, EC EXVI brief).
- Source statements not bound: Reuters 2026a-c (314 EUV systems, none in China; executives' bottleneck list; roughly 5 and 20 DUV tools) because Reuters refuses automated access and the articles are not archived; OECD relocalisation costs (over 18 percent of trade, over 5 percent of output) because oecd.org returned 403; the EU/US/China EXVI scores (0.22, 0.28, 0.13; 0.22, 0.19, 0.17), which sit in figures of the EC brief; Safran LEAP-1C and the C919 licence episode; Teece, Henderson and Clark, Polanyi, Nelson and Winter, Pisano and Shih (books or no abstract).
- Execution receipt: run id model (uv run python run_all.py), 38/38 invariants.
- metadata claims_target: claim-ledger.

## 2026-09-22 — prose revision

Prose rewritten against the house standards. Headings made descriptive (Introduction, Production and knowledge boundaries, Definition of a strategic black box, Comparison of dependence indices, Types of black box, Dynamics of capability loss, Topology of dependence and the frontier, Policy instruments, Regional positions, Objections, Falsification, Conclusion, Reproducibility).

Corrections found during the pass:
  - The break-even absorptive capacity (0.83) was obtained by linear interpolation between sweep points 0.8 and 0.9. A bisection on the model gives 0.8337; the value stands. New field proliferation.absorption_break_even_exact and invariant break_even_bisection_near_interpolation (38 invariants).
  - The text said imports build capability above absorptive capacity 0.83 and then cited a "high-absorption importer" with capacity 0.75 beating autarky. The sweep uses no engineering linkage while that arm has linkage 0.5; the text now states the break-even as the no-linkage value and attributes the arm's advantage to linkage.
  - Mean burden reported as 0.237; the value is 0.2375 exactly, now stated.
  - Trade-index rank correlation appeared as -0.286 in the body and -0.29 in the abstract; now -0.29 throughout.
  - The ASML 2025 annual report figures had a bibliography entry but no in-text citation; citation added.
  - "Fall takes 14 years" is now defined as the time to come within 0.02 of the final level, matching the code.

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
