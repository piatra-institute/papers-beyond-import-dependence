# Brief

Written before research begins.

## Question

In June 2026 a lithography maker stated that it had never shipped an extreme ultraviolet machine to China, and that none of the 314 such machines operating in the world sits there. On any trade-based measure of dependence, China's exposure to that machine is zero: nothing is imported, so nothing can be cut off. The measure is exactly inverted. Meanwhile a region can host a battery plant, an assembly line, or a data center, record the output as domestic, and hold none of the architecture, tooling, process recipes, firmware authority, or certification that would let it build the next one. What quantity is being missed by every measure that counts products crossing borders, and what follows for how an economy should think about what it buys?

## Claim

Import dependence and black-box dependence are different quantities, they diverge exactly where policy matters, and the divergence is measurable. Five moves carry the paper:

1. **Two boundaries.** The production boundary asks where a thing is made. The knowledge boundary asks who could specify, verify, modify, reproduce, qualify, scale, service, and supersede it. Competent integrators routinely know more than they make, and the classic result is that outsourcing production is not the same act as outsourcing knowledge. Cross the two boundaries and four cells appear: closed capability, white-box import, enclave assembly, and full black-box dependence. Trade statistics see one axis of the four-cell space.
2. **A definition with its parameters exposed.** A node is a strategic black box for a region, at a horizon, a performance level, a quantity, a cost ceiling, and a coalition boundary, when it is critical, when access can be interrupted by someone else, and when the region cannot credibly deliver qualified output after that interruption. Every one of those qualifiers does work: prototypes are not production, ten units are not a million, a member state is not the union, and a claim without a horizon is not a claim. The condition is a probability, so the paper reports distributions rather than verdicts.
3. **The banned-node inversion, priced.** When an export control bites, recorded imports fall to zero and every trade-based vulnerability index improves while the underlying exposure worsens. The paper's first mechanism builds eight canonical node types with known ground truth and asks which index recovers the true expected loss. The claim to test is that a capability index beats import share and supplier concentration overall, and that the failures of the trade measures are systematic rather than noisy: they are wrong about the embargoed frontier node, the enclave assembly node, the commodity import, and the ore that a region knows how to use.
4. **Proliferation as a mechanism, with the sign of imports left open.** Capability is a stock that depreciates. Imports feed it through exposure and use, and drain it by removing the domestic volume that keeps suppliers, tool shops, test rigs, and trained engineers alive. Which effect dominates is set by absorptive capacity and local linkage, so the model must be able to produce both hollowing and upgrading from the same equation, and the paper reports the boundary between them. The nonlinearity that matters is a minimum efficient scale: below it the commons dissolves, and the asymmetry between the cost of holding capability and the cost of rebuilding it is the paper's hysteresis result.
5. **Breadth against depth, and why a scalar cannot decide.** Two regions can share a mean burden and face entirely different risks: many moderate dependencies bound together by shared upstream, against a handful of frontier chokepoints. The paper builds both, shocks them diffusely and precisely, and shows the ranking reverses with the shock. The frontier race follows: a region can raise absolute capability every year while its distance to a moving frontier stays constant, which is the correct formal statement of what a lithography programme is up against. Policy is then allocated per unit of spend across diversification, stockpiling, selective unboxing, and blanket relocalization, and the finding to test is that the best instrument is a function of topology while the worst is the same everywhere.

## Kind

**formal-model** with a comparative empirical frame; ships a simulation. `has_simulation: true`, `claims_target: results.json`.

Three mechanisms, calibrated against verified anchors and reporting honest failure regimes:

- **The boundary detector.** Canonical node archetypes with generative ground truth, an explicit shock and recovery model producing true expected loss, and three competing indices scored by rank correlation. Must produce: the capability index dominating on average; the embargoed frontier node ranked near-safest by import share and worst by capability; the enclave node invisible to both trade measures; and the honest counter-case, the standardized commodity where import share is right and the capability index adds nothing.
- **Proliferation and hysteresis.** The capability stock with a conditional import term and a scale cliff. Must produce: the absorptive-capacity threshold at which imports switch from building capability to eroding it; the collapse below minimum efficient scale; the ratio of rebuild cost to maintenance cost; and the deployment-without-learning case where two regions install identical capacity and only one ends with the capability to build it.
- **Breadth, depth, and the frontier.** Two topologies at equal mean burden, ensembles of diffuse and targeted shocks, a correlation structure that makes diffuse shocks bite the broad region, a frontier that moves while capability accumulates, and a policy allocation comparing four instruments per unit of spend under both topologies.

## Constraint

The paper stands alone and cites no PIATRA paper. It is not an argument for autarky, and the modelled cost of blanket relocalization is stated with the same emphasis as the cost of dependence. It does not claim Europe is uniquely dependent, since the verified trade index has the European Union less exposed than the United States overall, and the paper's argument is precisely that the index is the wrong instrument rather than that the index has the wrong sign. It does not assert Chinese capabilities that are announced but unverified, and prototype claims are kept distinct from production evidence throughout. Latin America and Africa enter as capability ladders, operational to maintenance to reproductive to developmental, rather than as regional averages. Every number is traced to the primary record, institutional authors are spelled out in text, and the simulation's numbers are described as facts about the model.

## Cornerstone literature

Each with one job:

- **Brusoni, Prencipe and Pavitt** — the knowledge boundary against the production boundary; integrators know more than they make.
- **Kapoor and Adner** — the same distinction tested on outcomes.
- **Cohen and Levinthal** — absorptive capacity; why the sign of an import is conditional.
- **Gereffi, Humphrey and Sturgeon; Sturgeon** — value-chain governance and modular networks; codifiability as the variable that decides what a supplier relationship transmits.
- **Henderson and Clark** — architectural knowledge as a distinct thing to lose.
- **Teece** — complementary assets; why the design owner without the production system loses anyway.
- **Baldwin and Clark** — modularity as option value, and the option that outsourcing sells.
- **Polanyi; Nelson and Winter** — tacit knowledge and routines; the part of a process that no document carries.
- **Pisano and Shih** — the industrial commons and its dissolution below scale.
- **Lall; Bell and Pavitt** — capability ladders in developing economies; operation is not reproduction.
- **Hidalgo and Hausmann** — capabilities as the latent structure behind what a place can make.
- **Acemoglu, Carvalho, Ozdaglar and Tahbaz-Salehi; Barrot and Sauvagnat; Carvalho, Nirei, Saito and Tahbaz-Salehi** — network propagation and input specificity; the empirical fact that a small input stops a large output.
- **Farrell and Newman** — weaponized interdependence; why the access term is political rather than logistical.
- **The External Vulnerability Index; the Organisation for Economic Co-operation and Development's resilience review; the International Energy Agency; the Government Accountability Office; the Department of Energy; the World Health Organization; the United Nations Industrial Development Organization** — the measured world the paper argues with rather than against.
