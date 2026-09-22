# Beyond Import Dependence

Capability Closure and the Measurement of Strategic Black Boxes.

In June 2026 the sole maker of extreme ultraviolet lithography systems stated that it had never shipped one to China and that none of the 314 machines operating worldwide is located there (Reuters, 2026a). Trade-based dependence measures therefore score Chinese exposure to that machine as zero, and in general they improve when a border closes. We separate import dependence from black-box dependence. A node is a strategic black box for a region when it is critical, when access to it can be interrupted by others, and when the region cannot credibly specify, verify, modify, produce, qualify, scale, service or replace it at the required performance, quantity, cost and horizon. In a model of 8 canonical node types with generative ground truth, a capability index recovers the true ordering of expected loss exactly (rank correlation 1.00), while import share and a concentration-weighted trade index correlate at −0.31 and −0.29. Embargoing one node drops its trade index from 0.94 to 0 while its expected loss rises by a factor of 1.61. Treating capability as a stock, an import share of 0.5 builds capability above an absorptive capacity of 0.83 (without local engineering linkage) and erodes it below; the fall after hollowing takes 14 years and the climb back to the starting level 20. Two regions with identical mean burden of 0.2375 and opposite topology reverse their loss ranking with the type of shock, which argues against any scalar dependence index. The results support measuring capability and do not support closing borders.

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

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build beyond-import-dependence`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
