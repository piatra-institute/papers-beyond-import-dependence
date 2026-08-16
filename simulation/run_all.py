"""Orchestrator: reproduces every number and all three figures in the paper.

    cd simulation
    uv run run_all.py

Writes output/results.json and output/figures/*.png. Mechanisms 1 and 3 run
on recorded seeds and mechanism 2 is deterministic, so a rerun reproduces
every number bit for bit. A failed invariant fails the run.
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    from figures import plot_detector, plot_proliferation, plot_topology
    plot_detector(results, str(OUT / "figures" / "detector.png"))
    plot_proliferation(results, str(OUT / "figures" / "proliferation.png"))
    plot_topology(results, str(OUT / "figures" / "topology.png"))

    d = results["detector"]
    print("detector: rank correlation with true loss ->",
          {k: round(v, 3) for k, v in d["spearman_vs_truth"].items()})
    e = d["embargo_episode"]
    print(f"  embargo episode: trade index {e['trade_index_before']:.2f} -> "
          f"{e['trade_index_after']:.2f} while true loss rises "
          f"{e['truth_before']:.2f} -> {e['truth_after']:.2f} "
          f"({e['truth_ratio']:.2f}x)")
    print(f"  transparent subset: trade "
          f"{d['transparent_subset_spearman']['trade_index']:.2f}, capability "
          f"{d['transparent_subset_spearman']['capability_burden']:.2f}")

    p = results["proliferation"]
    print("proliferation:", {k: round(v["final_k"], 3)
                             for k, v in p["arms"].items()})
    print(f"  break-even absorptive capacity {p['absorption_break_even']:.2f}")
    h = p["hysteresis"]
    print(f"  hysteresis: {h['years_of_decline']}y down, "
          f"{h['years_to_rebuild_to_start']:.0f}y back "
          f"({h['rebuild_over_decline']:.2f}x); never-lost level reachable "
          f"behind a wall: {h['held_level_reachable_behind_a_wall']}")
    print(f"  deployment without learning: gap {p['deployment']['gap']:.3f}")

    t = results["topology"]
    pr = t["profile"]
    print(f"topology: mean burden broad {pr['broad']['mean_burden']:.3f} / "
          f"deep {pr['deep']['mean_burden']:.3f}; nodes over 0.2: "
          f"{pr['broad']['breadth_above_0_2']} / {pr['deep']['breadth_above_0_2']}; "
          f"worst decile {pr['broad']['depth_worst_decile']:.2f} / "
          f"{pr['deep']['depth_worst_decile']:.2f}")
    print("  ranking by shock:", t["ranking_by_shock"])
    f = t["frontier"]
    print(f"  frontier: capability x{f['capability_growth_factor']:.2f}, gap "
          f"{f['gap_start']:.2f} -> {f['gap_end']:.2f}, ratio "
          f"{f['ratio_start']:.2f} -> {f['ratio_end']:.2f}")
    for name, v in t["policy"].items():
        print(f"  {name}: best at budget 4 = {v['best']}; unboxing best from "
              f"{v['unbox_best_from_budget']}; relocalization best at "
              f"{v['relocalize_best_at']}")
    print("checks:", f"{sum(results['checks'].values())}/{len(results['checks'])}")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
