# Beyond Import Dependence

Capability Closure and the Measurement of Strategic Black Boxes. In June 2026 the sole maker of extreme ultraviolet lithography systems stated it had never shipped one to China, and that none of the 314 machines operating worldwide is located there. On any measure built from trade flows, Chinese exposure to that machine is zero: nothing is imported, so nothing can be cut off. The measure is inverted rather than imprecise, and the inversion is systematic, because trade measures improve at the moment a border closes. This paper separates import dependence from black-box dependence and defines the second: a node is a strategic black box for a region, at a horizon, a performance level, a quantity, a cost ceiling, and a coalition boundary, when it is critical, when access can be interrupted by someone else, and when the region cannot credibly specify, verify, modify, produce, qualify, scale, service, or replace it in time. Three mechanisms price the difference. Eight canonical node types with generative ground truth are scored by three competing indices: a capability index recovers the true ordering at a rank correlation of 1.00 while import share and a concentration-weighted trade index score −0.31 and −0.286, and simulating an embargo drops a node's trade index from 0.94 to 0 while its true expected loss rises by a factor of 1.61. Capability as a stock gives the conditional sign of an import: at an import share of 0.5 the break-even absorptive capacity is 0.83, a production floor prevents the commons collapse that follows a fall below minimum efficient scale, the fall takes 14 years while the climb back to the starting level takes 20, and the level of a region that never lost the capability is unreachable behind a protective wall at all. Two regions with identical mean burden of 0.237 and opposite topology reverse their loss ranking with the kind of shock, which is the formal case against any scalar dependence index, and selective unboxing turns out to be lumpy: below a budget threshold, closing half a set of chokepoints buys almost nothing. The paper argues for measuring capability, not for closing borders.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Mechanisms 1 and 3 run on recorded seeds and mechanism 2 is deterministic, so a rerun reproduces every number bit for bit. Thirty-seven invariant checks fail the run loudly if broken, among them: the capability index beating both trade measures and the trade index remaining adequate on the transparent subset where nothing is opaque; the embargo simultaneously improving the trade index and worsening the truth; the conditional sign of imports with an interior break-even; the production floor preventing commons collapse; the rebuild taking longer than the decline while the never-lost level stays unreachable behind a wall; the ranking reversal between diffuse and targeted shocks; the frontier gap widening while the ratio improves; and the lumpiness of selective unboxing, including the underfunded window in which blanket relocalization scores best. The verified external figures enter results.json as cited records with sources.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build beyond-import-dependence`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
