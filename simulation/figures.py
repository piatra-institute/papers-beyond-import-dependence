"""Figures for *Beyond Import Dependence*. Each reads the results dict and
writes one PNG.

Palette (CVD-checked in a prior validation; line styles and direct labels as
secondary encoding): amber, green, blue, warm gray; red reserved for harm.
"""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#1a1a1a"
GRID = "#d9d9d9"
AMBER = "#b45309"
GREEN = "#15803d"
BLUE = "#2563eb"
GRAY = "#57534e"
RED = "#b3202c"

NODE_LABEL = {
    "embargoed_frontier_tool": "frontier tool, embargoed",
    "frontier_tool_supplied": "frontier tool, supplied",
    "enclave_assembly": "enclave assembly",
    "cloud_controlled_device": "cloud-controlled device",
    "midstream_material": "midstream material",
    "understood_ore": "ore inside a mastered process",
    "white_box_import": "white-box import",
    "standard_component": "standard component",
}


def _style(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
    ax.tick_params(colors=INK, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)


def plot_detector(res: dict, path: str) -> None:
    det = res["detector"]
    nodes = det["nodes"]
    order = sorted(nodes, key=lambda n: -nodes[n]["truth"])
    truth = np.array([nodes[n]["truth"] for n in order])
    trade = np.array([nodes[n]["trade_index"] for n in order])
    cap = np.array([nodes[n]["capability_burden"] for n in order])
    # scale each index to its own maximum: only the ordering is claimed
    trade_s = trade / trade.max()
    cap_s = cap / cap.max()
    truth_s = truth / truth.max()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.2),
                                   gridspec_kw={"width_ratios": [1.5, 1]})
    y = np.arange(len(order))[::-1]
    h = 0.26
    ax1.barh(y + h, truth_s, height=h, color=GRAY, label="true expected loss")
    ax1.barh(y, cap_s, height=h, color=GREEN, label="capability burden")
    ax1.barh(y - h, trade_s, height=h, color=RED,
             label="trade index (imports x concentration)")
    ax1.set_yticks(y)
    ax1.set_yticklabels([NODE_LABEL[n] for n in order], fontsize=8.5)
    ax1.set_xlabel("scaled to each measure's own maximum", fontsize=9)
    ax1.set_title("measures by node type, ordered by true loss",
                  fontsize=10, color=INK)
    ax1.legend(frameon=False, fontsize=8, loc="lower right")
    ax1.annotate("imports are zero because supply is denied",
                 (0.015, y[0] - h), fontsize=7.5, color=RED, va="center",
                 xytext=(34, 0), textcoords="offset points",
                 arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    _style(ax1)

    rho = det["spearman_vs_truth"]
    keys = ["import_share", "trade_index", "capability_burden"]
    labels = ["import\nshare", "trade\nindex", "capability\nburden"]
    vals = [rho[k] for k in keys]
    colors = [RED, AMBER, GREEN]
    ax2.bar(range(3), vals, color=colors, width=0.6)
    for i, v in enumerate(vals):
        ax2.annotate(f"{v:+.2f}", (i, v), fontsize=9, ha="center",
                     va="bottom" if v >= 0 else "top", color=INK,
                     xytext=(0, 4 if v >= 0 else -4),
                     textcoords="offset points")
    ax2.axhline(0, color=INK, lw=0.9)
    ax2.set_xticks(range(3))
    ax2.set_xticklabels(labels, fontsize=8.5)
    ax2.set_ylim(-0.65, 1.2)
    ax2.set_ylabel("rank correlation with true loss", fontsize=9)
    ax2.set_title("rank correlation with true loss",
                  fontsize=10, color=INK)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_proliferation(res: dict, path: str) -> None:
    pro = res["proliferation"]
    arms = pro["arms"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 3.9),
                                   gridspec_kw={"width_ratios": [1.35, 1]})
    style = {
        "autarkic": (GRAY, "--", "closed: no imports"),
        "absorbing_importer": (GREEN, "-", "imports at 0.5, high absorption"),
        "passive_importer": (AMBER, "-", "imports at 0.5, low absorption"),
        "deep_import_low_absorption": (RED, "-", "imports at 0.8, low absorption"),
        "guaranteed_floor": (BLUE, "-.", "same, with a production floor"),
    }
    q_star = pro["constants"]["Q_STAR"]
    for name, (c, ls, lab) in style.items():
        k = arms[name]["k"]
        ax1.plot(range(1, len(k) + 1), k, ls, color=c, lw=1.7, label=lab)
    ax1.axhline(pro["constants"]["K_INIT"], color=INK, lw=0.7, ls=":")
    ax1.annotate("starting capability", (len(arms["autarkic"]["k"]) - 1,
                 pro["constants"]["K_INIT"]), fontsize=7.5, color=INK,
                 ha="right", va="bottom")
    ax1.set_xlabel("year", fontsize=9)
    ax1.set_ylabel("capability closure", fontsize=9)
    ax1.set_title("capability over time by import regime", fontsize=10, color=INK)
    ax1.legend(frameon=False, fontsize=7.8, loc="center right")
    _style(ax1)

    sw = pro["absorption_sweep"]
    ac = [s["ac"] for s in sw]
    dv = [s["vs_no_import"] for s in sw]
    ax2.plot(ac, dv, "-o", color=BLUE, lw=1.8, ms=4)
    ax2.axhline(0, color=INK, lw=0.9)
    be = pro["absorption_break_even"]
    ax2.axvline(be, color=GREEN, lw=0.9, ls=":")
    ax2.annotate(f"break-even\nabsorption {be:.2f}\n(no linkage)", (be, min(dv) * 0.55),
                 fontsize=8, color=GREEN, ha="right",
                 xytext=(-6, 0), textcoords="offset points")
    ax2.set_xlabel("absorptive capacity", fontsize=9)
    ax2.set_ylabel("capability gained against closure", fontsize=9)
    ax2.set_title("capability change against absorptive capacity", fontsize=10, color=INK)
    _style(ax2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_topology(res: dict, path: str) -> None:
    top = res["topology"]
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(11.4, 3.7),
                                        gridspec_kw={"width_ratios": [1, 1, 1.15]})
    # left: the same mean, two distributions, two shock rankings
    losses = top["losses"]
    modes = ["diffuse", "targeted"]
    x = np.arange(len(modes))
    w = 0.36
    ax1.bar(x - w / 2, [losses["broad"][m]["mean"] for m in modes], width=w,
            color=AMBER, label="breadth region")
    ax1.bar(x + w / 2, [losses["deep"][m]["mean"] for m in modes], width=w,
            color=BLUE, label="depth region")
    for i, m in enumerate(modes):
        for off, reg, col in ((-w / 2, "broad", AMBER), (w / 2, "deep", BLUE)):
            v = losses[reg][m]["mean"]
            ax1.annotate(f"{v:.2f}", (i + off, v), fontsize=8, ha="center",
                         va="bottom", color=col, xytext=(0, 2),
                         textcoords="offset points")
    ax1.set_xticks(x)
    ax1.set_xticklabels(["shared-upstream\nshock", "targeted\nchokepoint"],
                        fontsize=8.5)
    ax1.set_ylabel("mean output loss", fontsize=9)
    ax1.set_ylim(0, 1.05)
    mb = top["profile"]["broad"]["mean_burden"]
    ax1.set_title(f"loss by shock type at equal mean burden ({mb:.4f})",
                  fontsize=9.5, color=INK)
    ax1.legend(frameon=False, fontsize=8, loc="upper left")
    _style(ax1)

    # middle: the moving frontier
    fp = top["frontier_path"]
    yr = [p["year"] for p in fp]
    ax2.plot(yr, [p["frontier"] for p in fp], "--", color=RED, lw=1.7,
             label="frontier")
    ax2.plot(yr, [p["capability"] for p in fp], "-", color=GREEN, lw=1.9,
             label="capability")
    ax2.fill_between(yr, [p["capability"] for p in fp],
                     [p["frontier"] for p in fp], color=RED, alpha=0.10)
    f = top["frontier"]
    ax2.annotate(f"gap {f['gap_start']:.2f} to {f['gap_end']:.2f}\n"
                 f"ratio {f['ratio_start']:.2f} to {f['ratio_end']:.2f}",
                 (yr[-1], 0.5), fontsize=7.8, color=INK, ha="right")
    ax2.set_xlabel("year", fontsize=9)
    ax2.set_ylabel("capability level", fontsize=9)
    ax2.set_title("capability and frontier over time",
                  fontsize=9.5, color=INK)
    ax2.legend(frameon=False, fontsize=8, loc="upper left")
    _style(ax2)

    # right: policy per budget under depth
    deep = top["policy"]["deep"]["by_budget"]
    broad = top["policy"]["broad"]["by_budget"]
    buds = [r["budget"] for r in deep]
    for inst, col, ls in (("unbox", GREEN, "-"),
                          ("diversify", AMBER, "--"),
                          ("relocalize", RED, "-."),
                          ("stockpile", GRAY, ":")):
        ax3.plot(buds, [r[inst] for r in deep], ls, color=col, lw=1.7,
                 label=inst.replace("unbox", "selective unboxing"))
        ax3.plot(buds, [r[inst] for r in broad], ls, color=col, lw=1.0,
                 alpha=0.35)
    ub = top["policy"]["deep"]["unbox_best_from_budget"]
    ax3.axvline(ub, color=GREEN, lw=0.8, ls=":")
    ax3.annotate("partial unboxing:\nlittle gain", (ub - 0.25, 0.055),
                 fontsize=7.5, color=GREEN, ha="right", va="bottom")
    ax3.set_xlabel("budget (bold: depth region, faint: breadth)", fontsize=8.5)
    ax3.set_ylabel("loss avoided", fontsize=9)
    ax3.set_title("loss avoided against budget by instrument",
                  fontsize=9.5, color=INK)
    ax3.legend(frameon=False, fontsize=7.5, loc="upper left")
    _style(ax3)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
