"""Three mechanisms of black-box dependence.

1. The boundary detector. Eight canonical node archetypes are given
   generative ground truth (criticality, access risk, capability closure,
   substitutability, reconstitution time). A shock-and-recovery model turns
   that ground truth into an expected loss, which no index can see. Three
   competing indices are then scored against it: import share, supplier
   concentration, and a capability-based burden. The archetypes are chosen
   so the disagreements are the interesting cases: the embargoed frontier
   node whose recorded imports are zero, the enclave assembly node whose
   output is domestic, the ore a region knows how to use, and the honest
   counter-case where import share is already right.

2. Proliferation and hysteresis. Capability is a stock that depreciates,
   is fed by domestic production, research, and absorbed imports, and is
   drained by imports that displace production without transferring
   knowledge. The sign of an import is therefore conditional on absorptive
   capacity, and the model must be able to produce both hollowing and
   upgrading. Below a minimum efficient scale the commons dissolves and
   depreciation jumps, which makes the loss cheap and the rebuild dear.

3. Breadth, depth, and the moving frontier. Two regions are built with
   equal mean burden and different topology: many moderate dependencies
   sharing upstream against few extreme frontier chokepoints. Ensembles of
   diffuse and targeted shocks rank them in opposite orders, which is the
   argument against a scalar index. A frontier that advances while
   capability accumulates gives the closure-rate result, and four policy
   instruments are then compared per unit of spend under both topologies.

Calibration is structural; the verified external anchors used in prose live
in results.json as cited_record entries. Mechanism 1 and 3 run on recorded
seeds; mechanism 2 is deterministic. Invariants fail the run.
"""
from __future__ import annotations

import math

import numpy as np

SEED = 20260816


def _py(x):
    """Recursively convert numpy scalars/arrays for json.dumps."""
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (np.floating,)):
        return round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()]
    if isinstance(x, float):
        return round(x, 6)
    return x


def _spearman(a, b) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    def rank(v):
        order = v.argsort()
        r = np.empty(len(v), dtype=float)
        r[order] = np.arange(len(v), dtype=float)
        # average ties
        for val in np.unique(v):
            m = v == val
            if m.sum() > 1:
                r[m] = r[m].mean()
        return r

    ra, rb = rank(a), rank(b)
    ra -= ra.mean()
    rb -= rb.mean()
    denom = math.sqrt(float((ra ** 2).sum() * (rb ** 2).sum()))
    return float((ra * rb).sum() / denom) if denom else 0.0


# ----------------------------------------------------------------------
# mechanism 1: the boundary detector
# ----------------------------------------------------------------------

HORIZON = 10.0          # policy horizon, years
DISCOUNT = 0.05
N_DRAWS = 4000          # shock draws per node

# Archetypes. Ground truth (hidden from every index):
#   crit  criticality: share of downstream output the node gates
#   acc   annual probability that qualified supply is interrupted
#   clos  capability closure: probability the region can deliver
#         qualified substitute output after an interruption
#   subs  availability of an already-qualified alternative supplier
#   recon reconstitution time in years, given no qualified substitute
# Observables (what the indices see):
#   imp   import share of consumption
#   hhi   supplier concentration of recorded trade
ARCHETYPES = {
    "embargoed_frontier_tool": {
        "crit": 0.85, "acc": 0.55, "clos": 0.08, "subs": 0.05, "recon": 14.0,
        "imp": 0.00, "hhi": 0.00,
        "note": "controlled: recorded imports are zero because supply is "
                "already denied"},
    "frontier_tool_supplied": {
        "crit": 0.85, "acc": 0.18, "clos": 0.10, "subs": 0.05, "recon": 12.0,
        "imp": 0.98, "hhi": 0.96,
        "note": "the same machine, still arriving"},
    "enclave_assembly": {
        "crit": 0.55, "acc": 0.30, "clos": 0.18, "subs": 0.25, "recon": 7.0,
        "imp": 0.15, "hhi": 0.30,
        "note": "assembled locally from an imported kit under foreign "
                "design and process authority"},
    "cloud_controlled_device": {
        "crit": 0.45, "acc": 0.35, "clos": 0.22, "subs": 0.30, "recon": 5.0,
        "imp": 0.20, "hhi": 0.55,
        "note": "modest goods value, external update and control authority"},
    "midstream_material": {
        "crit": 0.50, "acc": 0.28, "clos": 0.35, "subs": 0.30, "recon": 6.0,
        "imp": 0.90, "hhi": 0.85,
        "note": "a refining or wafer stage that left and did not come back"},
    "understood_ore": {
        "crit": 0.60, "acc": 0.25, "clos": 0.80, "subs": 0.60, "recon": 2.0,
        "imp": 0.95, "hhi": 0.55,
        "note": "high import share inside a process the region masters"},
    "standard_component": {
        "crit": 0.25, "acc": 0.20, "clos": 0.75, "subs": 0.85, "recon": 1.0,
        "imp": 0.80, "hhi": 0.45,
        "note": "documented, multiply sourced, qualifiable"},
    "white_box_import": {
        "crit": 0.65, "acc": 0.15, "clos": 0.85, "subs": 0.55, "recon": 2.5,
        "imp": 0.70, "hhi": 0.40,
        "note": "made elsewhere by choice, specified and integrated here"},
}


def _true_loss(rng, a: dict) -> float:
    """Expected discounted output loss over the horizon.

    An interruption arrives with annual probability acc. Output gated by
    the node stops until either an already-qualified alternative is
    switched in (probability subs, short delay), or the region reconstitutes
    the node (probability clos, taking recon years), or the horizon ends.
    """
    losses = np.empty(N_DRAWS)
    for k in range(N_DRAWS):
        t = 0.0
        loss = 0.0
        while t < HORIZON:
            gap = rng.exponential(1.0 / a["acc"])
            t += gap
            if t >= HORIZON:
                break
            if rng.random() < a["subs"]:
                dur = 0.25 + rng.exponential(0.35)
            elif rng.random() < a["clos"]:
                dur = a["recon"] * (0.5 + rng.random())
            else:
                dur = HORIZON - t          # unresolved within the horizon
            dur = min(dur, HORIZON - t)
            loss += a["crit"] * dur * math.exp(-DISCOUNT * t)
            t += dur
        losses[k] = loss
    return float(losses.mean())


def _capability_burden(a: dict) -> float:
    """The paper's index. Uses only quantities an assessor could code:
    criticality, access risk, closure, substitutability, and reconstitution
    time normalized to the horizon. It never sees the loss."""
    r = 1.0 - math.exp(-a["recon"] / HORIZON)
    return a["crit"] * a["acc"] * (1 - a["clos"]) * (1 - a["subs"]) * r


def run_detector() -> dict:
    rng = np.random.default_rng(SEED)
    names = list(ARCHETYPES)
    rows = {}
    for n in names:
        a = ARCHETYPES[n]
        rows[n] = {
            "truth": _true_loss(rng, a),
            "import_share": a["imp"],
            "trade_index": a["imp"] * a["hhi"],
            "capability_burden": _capability_burden(a),
            "note": a["note"],
        }
    truth = [rows[n]["truth"] for n in names]
    rho = {
        "import_share": _spearman([rows[n]["import_share"] for n in names], truth),
        "trade_index": _spearman([rows[n]["trade_index"] for n in names], truth),
        "capability_burden": _spearman([rows[n]["capability_burden"] for n in names],
                                       truth),
    }

    def rank_of(key, node):
        vals = sorted(names, key=lambda n: -rows[n][key])
        return vals.index(node) + 1

    ranks = {n: {k: rank_of(k, n) for k in
                 ("truth", "import_share", "trade_index", "capability_burden")}
             for n in names}

    # the four diagnostic disagreements
    diag = {
        "embargoed_truth_rank": ranks["embargoed_frontier_tool"]["truth"],
        "embargoed_trade_rank": ranks["embargoed_frontier_tool"]["trade_index"],
        "embargoed_capability_rank": ranks["embargoed_frontier_tool"]["capability_burden"],
        "enclave_truth_rank": ranks["enclave_assembly"]["truth"],
        "enclave_trade_rank": ranks["enclave_assembly"]["trade_index"],
        "enclave_capability_rank": ranks["enclave_assembly"]["capability_burden"],
        "ore_truth_rank": ranks["understood_ore"]["truth"],
        "ore_trade_rank": ranks["understood_ore"]["trade_index"],
        "ore_capability_rank": ranks["understood_ore"]["capability_burden"],
        "standard_truth_rank": ranks["standard_component"]["truth"],
        "standard_trade_rank": ranks["standard_component"]["trade_index"],
    }

    # the control episode: the same node before and after an embargo
    supplied = rows["frontier_tool_supplied"]
    embargoed = rows["embargoed_frontier_tool"]
    episode = {
        "trade_index_before": supplied["trade_index"],
        "trade_index_after": embargoed["trade_index"],
        "trade_index_change": embargoed["trade_index"] - supplied["trade_index"],
        "truth_before": supplied["truth"],
        "truth_after": embargoed["truth"],
        "truth_ratio": embargoed["truth"] / supplied["truth"],
        "capability_burden_before": supplied["capability_burden"],
        "capability_burden_after": embargoed["capability_burden"],
    }

    # honest limit: on the subset where nothing is opaque, the trade measure
    # is already adequate, so the capability index earns nothing there
    plain = ["understood_ore", "standard_component", "white_box_import",
             "midstream_material"]
    plain_rho = {
        "trade_index": _spearman([rows[n]["trade_index"] for n in plain],
                                 [rows[n]["truth"] for n in plain]),
        "capability_burden": _spearman([rows[n]["capability_burden"] for n in plain],
                                       [rows[n]["truth"] for n in plain]),
    }

    return {
        "constants": {"HORIZON": HORIZON, "DISCOUNT": DISCOUNT,
                      "N_DRAWS": N_DRAWS, "SEED": SEED},
        "nodes": rows,
        "spearman_vs_truth": rho,
        "spearman_magnitude": {k: abs(v) for k, v in rho.items()},
        "ranks": ranks,
        "diagnostics": diag,
        "embargo_episode": episode,
        "transparent_subset_spearman": plain_rho,
    }


# ----------------------------------------------------------------------
# mechanism 2: proliferation and hysteresis
# ----------------------------------------------------------------------

YEARS = 40
DELTA0 = 0.035       # baseline depreciation of capability
DELTA_LOST = 0.12    # depreciation once the commons is below scale
Q_STAR = 0.35        # minimum efficient scale, share of domestic demand
ALPHA = 0.055        # learning by doing per unit of domestic production
BETA = 0.020         # research contribution
CHI = 0.110          # knowledge absorbed from imports
OMEGA = 0.090        # displacement: imports that take the volume away
DEMAND = 1.0
K_INIT = 0.55
RD = 0.35            # research effort, held constant across arms


def _capability_path(ac: float, import_share: float, link: float = 0.0,
                     k0: float = K_INIT, years: int = YEARS,
                     protect: float = 0.0) -> dict:
    """Run the capability stock forward.

    ac    absorptive capacity, the fraction of an import's knowledge the
          region can take up
    import_share  share of domestic demand met from outside
    link  local supplier and engineering linkage attached to that import
    protect  floor under domestic production (a procurement guarantee)

    Gains are damped by the room left to grow, drains are proportional to
    the stock, so the system settles at interior points rather than at the
    bounds.
    """
    k = k0
    m = import_share
    ks, qs, deltas = [], [], []
    below_since = None
    for t in range(years):
        q_dom = DEMAND * max(protect, (1 - m) * (0.55 + 0.9 * k))
        delta = DELTA_LOST if q_dom < Q_STAR else DELTA0
        if q_dom < Q_STAR and below_since is None:
            below_since = t
        gain = (ALPHA * q_dom + BETA * RD + CHI * m * ac * (1 + link)) * (1 - k)
        drain = OMEGA * m * (1 - ac) * k + delta * k
        k = min(1.0, max(0.0, k + gain - drain))
        ks.append(k)
        qs.append(q_dom)
        deltas.append(delta)
    return {"k": ks, "q_dom": qs, "delta": deltas, "final_k": ks[-1],
            "below_scale_from": below_since}


def _years_to_settle(path: list, tol: float = 0.02) -> int:
    """Years until the path is within tol of its final value."""
    final = path[-1]
    for i, v in enumerate(path):
        if abs(v - final) <= tol:
            return i + 1
    return len(path)


def _rebuild_years(k_start: float, target: float, protect: float = 0.55) -> float:
    """Years to climb back to a target capability from a collapsed stock,
    with the commons gone and a heavy public push behind protected demand."""
    k = k_start
    for t in range(400):
        q_dom = DEMAND * max(protect, 0.55 + 0.9 * k)
        delta = DELTA_LOST if q_dom < Q_STAR else DELTA0
        k = min(1.0, k + (ALPHA * q_dom + BETA * RD) * (1 - k) - delta * k)
        if k >= target:
            return t + 1.0
    return float("inf")


def run_proliferation() -> dict:
    arms = {
        "autarkic": _capability_path(ac=0.5, import_share=0.0),
        "absorbing_importer": _capability_path(ac=0.75, import_share=0.5,
                                               link=0.5),
        "passive_importer": _capability_path(ac=0.15, import_share=0.5),
        "deep_import_low_absorption": _capability_path(ac=0.15,
                                                       import_share=0.8),
        "deep_import_high_absorption": _capability_path(ac=0.85,
                                                        import_share=0.8,
                                                        link=0.6),
        "guaranteed_floor": _capability_path(ac=0.15, import_share=0.8,
                                             protect=0.40),
    }

    # the sign of an import: sweep absorptive capacity at a fixed share
    sweep = []
    base = _capability_path(ac=0.0, import_share=0.0)["final_k"]
    for ac in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        fk = _capability_path(ac=ac, import_share=0.5)["final_k"]
        sweep.append({"ac": ac, "final_k": fk, "vs_no_import": fk - base})
    crossing = None
    for a, b in zip(sweep, sweep[1:]):
        if a["vs_no_import"] < 0 <= b["vs_no_import"]:
            span = b["vs_no_import"] - a["vs_no_import"]
            crossing = a["ac"] + (0 - a["vs_no_import"]) / span * (b["ac"] - a["ac"])
            lo_ac, hi_ac = a["ac"], b["ac"]
            break
    # the interpolated crossing is only a grid estimate; bisect the model
    crossing_exact = None
    if crossing is not None:
        for _ in range(50):
            mid = 0.5 * (lo_ac + hi_ac)
            if _capability_path(ac=mid, import_share=0.5)["final_k"] - base < 0:
                lo_ac = mid
            else:
                hi_ac = mid
        crossing_exact = hi_ac

    # hysteresis: the fall is fast and cheap, the climb is slow and dear
    hollow = arms["deep_import_low_absorption"]
    held = arms["absorbing_importer"]
    target = held["final_k"]
    decline_years = _years_to_settle(hollow["k"])
    rebuild_to_start = _rebuild_years(hollow["final_k"], K_INIT)
    rebuild_to_held = _rebuild_years(hollow["final_k"], target)
    hysteresis = {
        "held_final_k": held["final_k"],
        "hollowed_final_k": hollow["final_k"],
        "start_k": K_INIT,
        "years_of_decline": decline_years,
        "years_to_rebuild_to_start": rebuild_to_start,
        "rebuild_over_decline": rebuild_to_start / decline_years,
        "held_level_reachable_behind_a_wall": math.isfinite(rebuild_to_held),
        "below_scale_from": hollow["below_scale_from"],
    }

    # deployment without learning: identical installed capacity, different
    # share of the value chain performed locally
    deployment = {}
    for label, ac, link in (("learning_deployment", 0.8, 0.7),
                            ("turnkey_deployment", 0.1, 0.0)):
        p = _capability_path(ac=ac, import_share=0.85, link=link)
        deployment[label] = {"final_k": p["final_k"],
                             "installed_equal": True,
                             "below_scale_from": p["below_scale_from"]}
    deployment["gap"] = (deployment["learning_deployment"]["final_k"]
                         - deployment["turnkey_deployment"]["final_k"])

    return {
        "constants": {"YEARS": YEARS, "DELTA0": DELTA0,
                      "DELTA_LOST": DELTA_LOST, "Q_STAR": Q_STAR,
                      "ALPHA": ALPHA, "BETA": BETA, "CHI": CHI,
                      "OMEGA": OMEGA, "K_INIT": K_INIT, "RD": RD},
        "arms": {k: {"final_k": v["final_k"],
                     "below_scale_from": v["below_scale_from"],
                     "k": v["k"], "q_dom": v["q_dom"]}
                 for k, v in arms.items()},
        "absorption_sweep": sweep,
        "absorption_break_even": crossing,
        "absorption_break_even_exact": crossing_exact,
        "hysteresis": hysteresis,
        "deployment": deployment,
    }


# ----------------------------------------------------------------------
# mechanism 3: breadth, depth, and the moving frontier
# ----------------------------------------------------------------------

N_SHOCKS = 6000

# Two regions, equal mean node burden, different topology.
# broad:  many moderate nodes, sharing upstream clusters (correlated)
# deep:   mostly closed, a few frontier nodes with extreme burden
def _regions():
    broad = {"burdens": [0.30] * 18 + [0.05] * 6,
             "clusters": [0] * 6 + [1] * 6 + [2] * 6 + [3] * 6}
    deep = {"burdens": [0.1125] * 20 + [0.92, 0.88, 0.85, 0.80],
            "clusters": list(range(20)) + [20, 20, 20, 20]}
    return {"broad": broad, "deep": deep}


def _shock_losses(rng, region: dict, mode: str) -> np.ndarray:
    b = np.array(region["burdens"])
    cl = np.array(region["clusters"])
    n = len(b)
    out = np.empty(N_SHOCKS)
    for k in range(N_SHOCKS):
        if mode == "diffuse":
            # a shock to a shared upstream cluster hits every node in it
            hit_cluster = rng.integers(0, cl.max() + 1)
            hit = cl == hit_cluster
        elif mode == "targeted":
            # an adversary picks the single worst reachable node
            hit = np.zeros(n, dtype=bool)
            hit[int(np.argmax(b))] = True
        elif mode == "random_node":
            hit = np.zeros(n, dtype=bool)
            hit[rng.integers(0, n)] = True
        else:
            raise ValueError(mode)
        sev = b[hit] * (0.6 + 0.8 * rng.random(hit.sum()))
        # complementary failures compound: 1 - prod(1 - loss)
        out[k] = 1.0 - np.prod(1.0 - np.clip(sev, 0, 1))
    return out


def _policy(region: dict, instrument: str, budget: float) -> list:
    """Spend a budget on one instrument and return the new burden vector.

    Instruments differ in unit cost, in how much of a node's burden they
    remove, and in where they work at all. Diversification needs an
    alternative supplier to qualify, and a node whose burden is extreme is
    extreme partly because no alternative exists. Inventory buys months
    against a node that takes a decade to reconstitute.
    """
    b = list(region["burdens"])
    n = len(b)
    if instrument == "relocalize":
        # spread thin across every node regardless of burden
        per, cap = 0.55, 0.60
        share = min(1.0, budget / (per * n))
        return [x - cap * share * x for x in b]
    spec = {
        "diversify": {"per": 0.55, "cap": 0.45, "ceiling": 0.70,
                      "cap_above": 0.05},
        "stockpile": {"per": 0.30, "cap": 0.30, "ceiling": 0.70,
                      "cap_above": 0.00},
        "unbox":     {"per": 2.00, "cap": 0.95, "ceiling": 1.01,
                      "cap_above": 0.95},
    }[instrument]
    def effect(i):
        cap = spec["cap"] if b[i] <= spec["ceiling"] else spec["cap_above"]
        return cap * b[i]

    # spend on the largest reducible risk first, and skip nodes the
    # instrument barely touches: no planner buys a second source for a node
    # that has no second source
    order = sorted(range(n), key=lambda i: -effect(i))
    spent = 0.0
    for i in order:
        cap = spec["cap"] if b[i] <= spec["ceiling"] else spec["cap_above"]
        if cap < 0.10:
            continue
        cost = spec["per"] * b[i]
        if spent + cost > budget:
            continue
        spent += cost
        b[i] = b[i] - cap * b[i]
    return b


def run_topology() -> dict:
    rng = np.random.default_rng(SEED + 1)
    regs = _regions()
    profile = {}
    for name, r in regs.items():
        b = np.array(r["burdens"])
        profile[name] = {
            "n_nodes": len(b),
            "mean_burden": float(b.mean()),
            "breadth_above_0_2": int((b > 0.2).sum()),
            "depth_worst_decile": float(np.sort(b)[-max(1, len(b) // 10):].mean()),
            "concentration": float(((b / b.sum()) ** 2).sum()),
        }

    losses = {}
    for name, r in regs.items():
        losses[name] = {}
        for mode in ("diffuse", "targeted", "random_node"):
            L = _shock_losses(rng, r, mode)
            losses[name][mode] = {
                "mean": float(L.mean()),
                "p95": float(np.quantile(L, 0.95)),
            }
    ranking = {
        mode: ("broad" if losses["broad"][mode]["mean"] > losses["deep"][mode]["mean"]
               else "deep")
        for mode in ("diffuse", "targeted", "random_node")
    }

    # the moving frontier: capability accumulates, the frontier advances
    frontier = []
    cap, front = 0.35, 1.00
    CAP_RATE, FRONT_RATE = 0.115, 0.045
    for t in range(30):
        cap = cap + CAP_RATE * (1 - cap / (front * 1.05))
        front = front * (1 + FRONT_RATE)
        frontier.append({"year": t, "capability": cap, "frontier": front,
                         "gap": front - cap, "ratio": cap / front})
    frontier_summary = {
        "capability_start": frontier[0]["capability"],
        "capability_end": frontier[-1]["capability"],
        "capability_growth_factor": frontier[-1]["capability"] / frontier[0]["capability"],
        "gap_start": frontier[0]["gap"],
        "gap_end": frontier[-1]["gap"],
        "ratio_start": frontier[0]["ratio"],
        "ratio_end": frontier[-1]["ratio"],
        "gap_widened": frontier[-1]["gap"] > frontier[0]["gap"],
        "ratio_improved": frontier[-1]["ratio"] > frontier[0]["ratio"],
    }

    # policy per unit of spend, judged against a mixed shock ensemble: a
    # planner does not know which kind of shock arrives
    BUDGET = 4.0
    MIX = {"diffuse": 0.3, "random_node": 0.4, "targeted": 0.3}

    def mixed_loss(region):
        return float(sum(w * _shock_losses(rng, region, m).mean()
                         for m, w in MIX.items()))

    BUDGETS = [2.0, 4.0, 6.0, 8.0, 10.0, 12.0]
    policy = {}
    for name, r in regs.items():
        base = mixed_loss(r)
        policy[name] = {"shock_mix": MIX, "baseline_loss": base,
                        "by_budget": [], "instruments": {}}
        for bud in BUDGETS:
            row = {"budget": bud}
            for inst in ("diversify", "stockpile", "unbox", "relocalize"):
                nb = _policy(r, inst, bud)
                L = mixed_loss({"burdens": nb, "clusters": r["clusters"]})
                row[inst] = base - L
            row["best"] = max(("diversify", "stockpile", "unbox", "relocalize"),
                              key=lambda i: row[i])
            policy[name]["by_budget"].append(row)
            if bud == BUDGET:
                for inst in ("diversify", "stockpile", "unbox", "relocalize"):
                    policy[name]["instruments"][inst] = {
                        "reduction": row[inst],
                        "reduction_per_unit_spend": row[inst] / bud,
                    }
                policy[name]["best"] = row["best"]
                policy[name]["worst"] = min(
                    ("diversify", "stockpile", "unbox", "relocalize"),
                    key=lambda i: row[i])
        # the budget at which closing chokepoints starts to pay
        unbox_from = next((row["budget"] for row in policy[name]["by_budget"]
                           if row["best"] == "unbox"), None)
        policy[name]["unbox_best_from_budget"] = unbox_from
        policy[name]["relocalize_best_at"] = [
            row["budget"] for row in policy[name]["by_budget"]
            if row["best"] == "relocalize"]
        policy[name]["relocalize_ever_best"] = bool(
            policy[name]["relocalize_best_at"])

    return {
        "constants": {"N_SHOCKS": N_SHOCKS, "BUDGET": 4.0,
                      "POLICY_MIX": {"diffuse": 0.3, "random_node": 0.4,
                                     "targeted": 0.3},
                      "CAP_RATE": 0.115, "FRONT_RATE": 0.045},
        "profile": profile,
        "losses": losses,
        "ranking_by_shock": ranking,
        "frontier_path": frontier,
        "frontier": frontier_summary,
        "policy": policy,
    }


# ----------------------------------------------------------------------
# cited records
# ----------------------------------------------------------------------

CITED_RECORDS = {
    "asml_suppliers": {"value": 5100,
        "source": "ASML 2025 annual report"},
    "asml_euv_shipped_2025": {"value": 48,
        "source": "ASML 2025 annual report"},
    "asml_duv_shipped_2025": {"value": 279,
        "source": "ASML 2025 annual report (374 in 2024)"},
    "euv_systems_worldwide": {"value": 314,
        "source": "Reuters, June 19, 2026, citing an ASML internal presentation; "
                  "none located in China"},
    "zeiss_highna_projection_parts": {"value": 40000,
        "source": "ZEISS, High-NA EUV lithography (more than 40,000)"},
    "zeiss_highna_illumination_parts": {"value": 25000,
        "source": "ZEISS (more than 25,000)"},
    "zeiss_network_partners": {"value": 1200,
        "source": "ZEISS (more than 1,200 members)"},
    "bis_equipment_categories": {"value": 24,
        "source": "Bureau of Industry and Security, December 2, 2024"},
    "bis_software_categories": {"value": 3,
        "source": "Bureau of Industry and Security, December 2, 2024"},
    "iea_china_solar_share_pct": {"value": 85,
        "source": "IEA Energy Technology Perspectives 2026"},
    "iea_china_battery_share_pct": {"value": 80,
        "source": "IEA Energy Technology Perspectives 2026"},
    "iea_china_wafer_share_pct": {"value": 95,
        "source": "IEA Energy Technology Perspectives 2026"},
    "iea_china_anode_share_pct": {"value": 97,
        "source": "IEA Energy Technology Perspectives 2026"},
    "iea_battery_interruption_usd_bn_per_month": {"value": 17,
        "source": "IEA ETP 2026; almost two-thirds of losses in the EU"},
    "iea_eu_inverter_capacity_gw": {"value": 95,
        "source": "IEA inverter supply chains commentary, 2025 capacity"},
    "iea_eu_inverter_demand_gw": {"value": 90,
        "source": "IEA inverter supply chains commentary"},
    "iea_inverter_project_premium_pct": {"value": 2,
        "source": "IEA: just under 2 percent for utility-scale projects"},
    "exvi_semiconductors_eu": {"value": 0.22,
        "source": "Connell Garcia and Ho 2025, External Vulnerability Index, BACI 2022"},
    "exvi_semiconductors_us": {"value": 0.19, "source": "same"},
    "exvi_semiconductors_cn": {"value": 0.17, "source": "same"},
    "exvi_all_industrial_eu": {"value": 0.22, "source": "same"},
    "exvi_all_industrial_us": {"value": 0.28, "source": "same"},
    "exvi_all_industrial_cn": {"value": 0.13, "source": "same"},
    "gao_us_capacity_share_1990_pct": {"value": 37,
        "source": "GAO-26-107882"},
    "gao_us_capacity_share_2022_pct": {"value": 10,
        "source": "GAO-26-107882"},
    "gao_us_memory_share_pct": {"value": 3,
        "source": "GAO-26-107882, two most common memory types, 2022"},
    "doe_transformer_price_multiple_low": {"value": 4,
        "source": "US Department of Energy, grid supply chain"},
    "doe_transformer_price_multiple_high": {"value": 9,
        "source": "US Department of Energy, grid supply chain"},
    "oecd_relocalisation_trade_pct": {"value": 18,
        "source": "OECD Supply Chain Resilience Review 2025 (over 18 percent)"},
    "oecd_relocalisation_gdp_pct": {"value": 5,
        "source": "OECD Supply Chain Resilience Review 2025 (over 5 percent)"},
    "who_africa_medicine_imports_low_pct": {"value": 70,
        "source": "Dong and Mirza 2016, Bulletin of the WHO 94: 71-72"},
    "who_africa_medicine_imports_high_pct": {"value": 90,
        "source": "Dong and Mirza 2016"},
    "china_duv_units_2026": {"value": 5,
        "source": "Reuters, July 28, 2026 (about 5 machines in 2026)"},
    "china_duv_units_2027": {"value": 20,
        "source": "Reuters, July 28, 2026 (about 20 in 2027)"},
}


# ----------------------------------------------------------------------
# invariants
# ----------------------------------------------------------------------

def _checks(det: dict, pro: dict, top: dict) -> dict:
    c = {}
    # mechanism 1
    r = det["spearman_vs_truth"]
    c["capability_beats_import_share"] = r["capability_burden"] > r["import_share"]
    c["capability_beats_trade_index"] = r["capability_burden"] > r["trade_index"]
    c["capability_rank_correlation_high"] = r["capability_burden"] >= 0.8
    d = det["diagnostics"]
    c["embargoed_node_is_worst_in_truth"] = d["embargoed_truth_rank"] == 1
    c["embargoed_node_looks_safest_on_trade"] = d["embargoed_trade_rank"] >= 7
    c["capability_index_catches_embargoed"] = d["embargoed_capability_rank"] <= 2
    c["enclave_invisible_to_trade"] = (d["enclave_trade_rank"]
                                       - d["enclave_truth_rank"] >= 3)
    c["capability_index_catches_enclave"] = (d["enclave_capability_rank"]
                                             <= d["enclave_truth_rank"] + 1)
    c["ore_overstated_by_trade"] = (d["ore_truth_rank"]
                                    - d["ore_trade_rank"] >= 2)
    e = det["embargo_episode"]
    c["embargo_improves_trade_index"] = e["trade_index_change"] < 0
    c["embargo_worsens_truth"] = e["truth_ratio"] > 1.2
    p = det["transparent_subset_spearman"]
    c["trade_index_adequate_when_transparent"] = p["trade_index"] >= 0.8
    # mechanism 2
    a = pro["arms"]
    c["absorbing_importer_beats_autarky"] = (a["absorbing_importer"]["final_k"]
                                             > a["autarkic"]["final_k"])
    c["passive_importer_loses_capability"] = (a["passive_importer"]["final_k"]
                                              < K_INIT)
    c["import_sign_is_conditional"] = (a["deep_import_high_absorption"]["final_k"]
                                       > a["deep_import_low_absorption"]["final_k"])
    c["break_even_bisection_near_interpolation"] = (
        pro["absorption_break_even_exact"] is not None
        and abs(pro["absorption_break_even_exact"]
                - pro["absorption_break_even"]) < 0.1)
    c["break_even_absorption_interior"] = (pro["absorption_break_even"] is not None
                                           and 0.0 < pro["absorption_break_even"] < 1.0)
    c["deep_low_absorption_falls_below_scale"] = (
        a["deep_import_low_absorption"]["below_scale_from"] is not None)
    c["floor_prevents_commons_collapse"] = (
        a["guaranteed_floor"]["below_scale_from"] is None
        and a["guaranteed_floor"]["final_k"] > a["deep_import_low_absorption"]["final_k"])
    h = pro["hysteresis"]
    c["rebuild_takes_longer_than_decline"] = h["rebuild_over_decline"] > 1.2
    c["held_level_unreachable_behind_a_wall"] = (
        not h["held_level_reachable_behind_a_wall"])
    dep = pro["deployment"]
    c["deployment_without_learning_gap"] = dep["gap"] > 0.15
    c["capability_stays_interior"] = all(
        0.0 < a[k]["final_k"] < 1.0 for k in a)
    # mechanism 3
    pr = top["profile"]
    c["equal_mean_burden_by_construction"] = (
        abs(pr["broad"]["mean_burden"] - pr["deep"]["mean_burden"]) < 0.02)
    c["broad_has_more_nodes_over_threshold"] = (
        pr["broad"]["breadth_above_0_2"] > pr["deep"]["breadth_above_0_2"])
    c["deep_has_worse_tail"] = (pr["deep"]["depth_worst_decile"]
                                > pr["broad"]["depth_worst_decile"])
    rk = top["ranking_by_shock"]
    c["ranking_reverses_with_shock"] = rk["diffuse"] != rk["targeted"]
    c["diffuse_hurts_broad"] = rk["diffuse"] == "broad"
    c["targeted_hurts_deep"] = rk["targeted"] == "deep"
    f = top["frontier"]
    c["capability_rises_substantially"] = f["capability_growth_factor"] > 1.5
    c["frontier_gap_widens_anyway"] = f["gap_widened"]
    c["relative_position_still_improves"] = f["ratio_improved"]
    pol = top["policy"]
    c["diversification_wins_under_breadth"] = pol["broad"]["best"] == "diversify"
    c["unboxing_is_lumpy_under_depth"] = (
        pol["deep"]["unbox_best_from_budget"] is not None
        and pol["deep"]["unbox_best_from_budget"] > pol["deep"]["by_budget"][0]["budget"])
    c["unboxing_eventually_wins_under_depth"] = (
        pol["deep"]["by_budget"][-1]["best"] == "unbox")
    c["breadth_never_needs_unboxing_first"] = all(
        row["best"] != "unbox" for row in pol["broad"]["by_budget"][:2])
    c["relocalization_never_best_when_funded"] = all(
        row["best"] != "relocalize"
        for k in pol for row in pol[k]["by_budget"][-2:])
    c["relocalization_wins_only_underfunded"] = all(
        all(b < pol[k]["unbox_best_from_budget"]
            for b in pol[k]["relocalize_best_at"])
        for k in pol if pol[k]["unbox_best_from_budget"] is not None)
    return c


def run() -> dict:
    det = run_detector()
    pro = run_proliferation()
    top = run_topology()
    checks = _checks(det, pro, top)
    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise SystemExit(f"INVARIANT FAILURES: {failed}")
    return _py({
        "detector": det,
        "proliferation": pro,
        "topology": top,
        "cited_records": CITED_RECORDS,
        "checks": checks,
    })
