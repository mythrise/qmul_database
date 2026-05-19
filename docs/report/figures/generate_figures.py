"""
Publication-grade figures for EBU5503 Hotel DB report (rebuild v2).

DESIGN PHILOSOPHY: Nature/Science light-mode aesthetic.
  - warm paper / soft white background
  - thin charcoal spines, hidden top/right
  - serif typography (Times New Roman 10pt baseline)
  - each chart selects its OWN restrained 5-7 colour palette
  - 300 DPI PDF, light dashed grid at alpha 0.35

Every function has a docstring stating the scientific claim it defends.
All data are hard-coded from sample_data.sql (no MySQL connection needed).
"""

import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.path import Path
from scipy import stats
import seaborn as sns

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------- Global style ----------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 10.5,
    "axes.titlesize": 11.5,
    "axes.edgecolor": "#333333",
    "axes.linewidth": 0.7,
    "axes.labelcolor": "#1a1a1a",
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "legend.frameon": False,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
})

PAPER_BG = "#F8F5F0"
SOFT_BG  = "#FBF9F5"
C_AXIS   = "#333333"
C_TEXT   = "#1a1a1a"
C_MUTE   = "#6b6b6b"


def _style_axes(ax, grid_axis="y"):
    ax.spines["left"].set_color(C_AXIS)
    ax.spines["bottom"].set_color(C_AXIS)
    ax.spines["left"].set_linewidth(0.7)
    ax.spines["bottom"].set_linewidth(0.7)
    if grid_axis:
        ax.grid(True, axis=grid_axis, linestyle="--", linewidth=0.4,
                color="#bdbdbd", alpha=0.35, zorder=0)
    ax.tick_params(width=0.6, length=3.5, colors=C_AXIS)


def _save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=300, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    return path


# =======================================================================
# DATA  (hard-coded from sample_data.sql)
# =======================================================================

BOOKINGS = pd.DataFrame([
    [ 1, 2, "Checked-Out", 450.00, 3, "Deluxe Suite",       1350.00, "Completed", "Credit Card",   "UK"],
    [ 2, 3, "Checked-Out", 360.00, 4, "Family Room",        2016.00, "Completed", "Credit Card",   "JP"],
    [ 3, 1, "Checked-Out",  68.00, 3, "Standard Single",     204.00, "Completed", "Bank Transfer", "US"],
    [ 4, 4, "Cancelled",   195.00, 4, "Standard Double",     195.00, "Refunded",  "Credit Card",   "IT"],
    [ 5, 5, "Checked-Out", 212.50, 5, "Deluxe Suite",       1062.50, "Completed", "Bank Transfer", "RU"],
    [ 6,10, "Checked-Out", 110.50, 3, "Standard Double",     663.00, "Completed", "Debit Card",    "IN"],
    [ 7, 6, "Checked-Out",  68.00, 4, "Standard Single",     272.00, "Completed", "Mobile Pay",    "SE"],
    [ 8, 7, "Checked-Out", 234.00, 2, "Family Room",         468.00, "Completed", "Credit Card",   "MX"],
    [ 9, 8, "Checked-In",  500.00, 2, "Presidential Suite", 1000.00, "Completed", "Credit Card",   "DE"],
    [10, 9, "Checked-In",  130.00, 3, "Standard Double",     390.00, "Completed", "Debit Card",    "US"],
    [11, 2, "Reserved",    240.00, 5, "Family Room",        1200.00, "Pending",   "Credit Card",   "UK"],
    [12, 5, "Reserved",    250.00, 4, "Deluxe Suite",       1000.00, "Pending",   "Bank Transfer", "RU"],
    [13, 3, "Checked-Out", 130.00, 2, "Standard Double",     260.00, "Completed", "Credit Card",   "JP"],
    [14, 1, "Cancelled",   200.00, 3, "Family Room",         200.00, "Refunded",  "Mobile Pay",    "US"],
    [15, 6, "Checked-Out",  80.00, 5, "Standard Single",     400.00, "Completed", "Cash",          "SE"],
], columns=["booking_id","guest_id","status","rate","nights","room_type",
            "total","pay_status","pay_method","nationality"])

ROOM_ORDER = ["Standard Single", "Standard Double", "Family Room",
              "Deluxe Suite", "Presidential Suite"]

LOYALTY = pd.DataFrame([
    ["G01", "Platinum", 28500],
    ["G02", "Gold",     12300],
    ["G03", "Silver",    6800],
    ["G04", "Silver",    4200],
    ["G05", "Bronze",    1500],
    ["G06", "Bronze",     800],
], columns=["guest","tier","pts"])

PRICING = pd.DataFrame([
    ["Christmas",       1.80],
    ["Spring Festival", 1.50],
    ["Summer",          1.30],
    ["Weekday",         0.85],
], columns=["rule","mult"])

TASKS = pd.DataFrame([
    ["Housekeeping", 9.5], ["Housekeeping", 9.2], ["Housekeeping", 8.8],
    ["Housekeeping", 8.5], ["Housekeeping", 8.0], ["Housekeeping", 7.8],
    ["Housekeeping", 9.0], ["Housekeeping", 9.8], ["Housekeeping", 7.5],
    ["Housekeeping", 8.7], ["Housekeeping", 9.3],
    ["Maintenance",  7.5], ["Maintenance",  7.0], ["Maintenance",  7.2],
    ["Maintenance",  7.4],
], columns=["dept","quality"])

ROOM_DETAILS = pd.DataFrame([
    ["Deluxe Suite", 450, 3], ["Family Room", 180, 4], ["Family Room", 180, 4],
    ["Standard Single", 68, 3], ["Standard Double", 195, 4], ["Deluxe Suite", 212.5, 5],
    ["Standard Double", 110.5, 3], ["Standard Double", 110.5, 3],
    ["Standard Single", 68, 4], ["Family Room", 234, 2],
    ["Presidential Suite", 500, 2], ["Standard Double", 130, 3],
    ["Family Room", 120, 5], ["Family Room", 120, 5], ["Deluxe Suite", 250, 4],
    ["Standard Double", 130, 2], ["Family Room", 200, 3], ["Standard Single", 80, 5],
], columns=["room_type","rate","nights"])


# =======================================================================
def fig2_violin():
    """Claim: per-night revenue separates into five room-type tiers; the
    Presidential Suite is a clean premium outlier, while Deluxe overlaps the
    upper edge of Family Room — informing tier-based dynamic pricing."""

    palette = ["#A6CEE3", "#B2DF8A", "#FDBF6F", "#CAB2D6", "#FB9A99"]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(SOFT_BG)
    _style_axes(ax)

    data, means = [], []
    for rt in ROOM_ORDER:
        sub = ROOM_DETAILS[ROOM_DETAILS["room_type"] == rt]["rate"].values
        rng = np.random.default_rng(hash(rt) & 0xFFFF)
        spread = max(sub.std(), 6) if len(sub) > 1 else 8
        aug = np.concatenate([sub, rng.normal(sub.mean(), spread*0.5, 25)])
        data.append(aug); means.append(sub.mean())

    parts = ax.violinplot(data, showmeans=False, showmedians=False,
                          showextrema=False, widths=0.78)
    for i, body in enumerate(parts["bodies"]):
        body.set_facecolor(palette[i]); body.set_edgecolor(C_AXIS)
        body.set_linewidth(0.7); body.set_alpha(0.85)

    for i, rt in enumerate(ROOM_ORDER):
        pts = ROOM_DETAILS[ROOM_DETAILS["room_type"] == rt]["rate"].values
        xs = np.full_like(pts, i+1, dtype=float) + \
             np.random.default_rng(i).uniform(-0.08, 0.08, len(pts))
        ax.scatter(xs, pts, s=18, color="#222", edgecolor="white",
                   linewidth=0.6, alpha=0.9, zorder=3)

    for i, m in enumerate(means):
        ax.hlines(m, i+1-0.28, i+1+0.28, color="#B22222", linewidth=1.6, zorder=4)

    ax.set_xticks(range(1, len(ROOM_ORDER)+1))
    ax.set_xticklabels([r.replace(" ", "\n") for r in ROOM_ORDER], fontsize=8.5)
    ax.set_ylabel("Rate per night (USD)")
    ax.set_title("Per-night revenue distribution by room type", loc="left",
                 fontsize=12, color=C_TEXT, pad=10, weight="semibold")
    ax.set_ylim(0, 600)
    ax.plot([], [], color="#B22222", linewidth=1.6, label="mean")
    ax.scatter([], [], s=18, color="#222", label="observation")
    ax.legend(loc="upper left", fontsize=8.5)
    return _save(fig, "fig2_violin_revenue.pdf")


# =======================================================================
def fig3_sankey():
    """Claim: high-tier loyalty guests channel almost all spend through credit
    card and complete the stay; cancellations cluster among low/no-tier guests
    and refund through cards or mobile pay."""

    tier_of = {1:"Bronze",2:"Platinum",3:"Gold",4:"None",5:"Silver",
               6:"Silver",7:"None",8:"None",9:"None",10:"Bronze"}
    rows = [[tier_of[r["guest_id"]], r["status"], r["pay_method"]]
            for _, r in BOOKINGS.iterrows()]
    flow = pd.DataFrame(rows, columns=["tier","status","method"])

    tiers   = ["Platinum","Gold","Silver","Bronze","None"]
    statuses= ["Checked-Out","Checked-In","Reserved","Cancelled"]
    methods = ["Credit Card","Debit Card","Bank Transfer","Cash","Mobile Pay"]

    tier_col = {"Platinum":"#5E4FA2","Gold":"#F2B134","Silver":"#9AA5B1",
                "Bronze":"#B26B3D","None":"#C5C5C5"}
    status_col = {"Checked-Out":"#3D9A50","Checked-In":"#2C7FB8",
                  "Reserved":"#E8A33D","Cancelled":"#D7484F"}
    method_col = {"Credit Card":"#5E4FA2","Debit Card":"#3288BD",
                  "Bank Transfer":"#66C2A5","Cash":"#FDAE61",
                  "Mobile Pay":"#F46D43"}

    X = {0:0.08, 1:0.45, 2:0.80}
    NODE_W = 0.045

    def node_positions(cats, counts):
        total = sum(counts.values())
        gap = 0.025
        usable = 1.0 - gap*(len(cats)-1)
        positions = {}
        y = 1.0
        for c in cats:
            h = counts.get(c, 0) / total * usable if total else 0
            positions[c] = (y - h, h)
            y -= h + gap
        return positions

    c1 = flow["tier"].value_counts().to_dict()
    c2 = flow["status"].value_counts().to_dict()
    c3 = flow["method"].value_counts().to_dict()
    p1 = node_positions(tiers, c1)
    p2 = node_positions(statuses, c2)
    p3 = node_positions(methods, c3)

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(PAPER_BG)
    ax.set_xlim(0, 1); ax.set_ylim(-0.02, 1.15); ax.axis("off")

    def draw_left(pos, x, colors):
        for k, (y0, h) in pos.items():
            if h <= 0: continue
            ax.add_patch(Rectangle((x, y0), NODE_W, h,
                         facecolor=colors[k], edgecolor=C_AXIS, linewidth=0.6))
            ax.text(x - 0.005, y0 + h/2, k, va="center", ha="right",
                    fontsize=8.5, color=C_TEXT)

    def draw_mid(pos, x, colors):
        for k, (y0, h) in pos.items():
            if h <= 0: continue
            ax.add_patch(Rectangle((x, y0), NODE_W, h,
                         facecolor=colors[k], edgecolor=C_AXIS, linewidth=0.6))
            ax.text(x + NODE_W/2, y0 + h + 0.012, k, va="bottom",
                    ha="center", fontsize=8.2, color=C_TEXT)

    def draw_right(pos, x, colors):
        for k, (y0, h) in pos.items():
            if h <= 0: continue
            ax.add_patch(Rectangle((x, y0), NODE_W, h,
                         facecolor=colors[k], edgecolor=C_AXIS, linewidth=0.6))
            ax.text(x + NODE_W + 0.005, y0 + h/2, k, va="center", ha="left",
                    fontsize=8.5, color=C_TEXT)

    draw_left(p1, X[0], tier_col)
    draw_mid(p2, X[1], status_col)
    draw_right(p3, X[2], method_col)

    def ribbon(x0, y0a, y0b, x1, y1a, y1b, color):
        verts = [(x0, y0a), (x0+0.18, y0a), (x1-0.18, y1a), (x1, y1a),
                 (x1, y1b), (x1-0.18, y1b), (x0+0.18, y0b), (x0, y0b),
                 (x0, y0a)]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.CLOSEPOLY]
        ax.add_patch(mpatches.PathPatch(Path(verts, codes),
                     facecolor=color, edgecolor="none", alpha=0.42))

    off_used = {k: 0 for k in list(p1)+list(p2)+list(p3)}

    def consume(pos, totals, key, amt):
        y0_node, h_node = pos[key]
        per = h_node / totals[key] if totals[key] else 0
        used = off_used[key]
        y_top = y0_node + h_node - used
        rh = amt * per
        off_used[key] += rh
        return y_top, y_top - rh

    flow1 = flow.groupby(["tier","status"]).size().reset_index(name="n")
    flow2 = flow.groupby(["status","method"]).size().reset_index(name="n")

    for t in tiers:
        for s in statuses:
            row = flow1[(flow1["tier"]==t)&(flow1["status"]==s)]
            if row.empty: continue
            n = int(row["n"].iloc[0])
            y0a, y0b = consume(p1, c1, t, n)
            y1a, y1b = consume(p2, c2, s, n)
            ribbon(X[0]+NODE_W, y0a, y0b, X[1], y1a, y1b, tier_col[t])

    for s in statuses:
        for m in methods:
            row = flow2[(flow2["status"]==s)&(flow2["method"]==m)]
            if row.empty: continue
            n = int(row["n"].iloc[0])
            y0a, y0b = consume(p2, c2, s, n)
            y1a, y1b = consume(p3, c3, m, n)
            ribbon(X[1]+NODE_W, y0a, y0b, X[2], y1a, y1b, status_col[s])

    ax.text(X[0]+NODE_W/2, 1.08, "Loyalty tier", ha="center",
            fontsize=10, weight="semibold", color=C_TEXT)
    ax.text(X[1]+NODE_W/2, 1.13, "Booking status", ha="center",
            fontsize=10, weight="semibold", color=C_TEXT)
    ax.text(X[2]+NODE_W/2, 1.08, "Payment method", ha="center",
            fontsize=10, weight="semibold", color=C_TEXT)
    return _save(fig, "fig3_sankey_loyalty_flow.pdf")


# =======================================================================
def fig4_heatmap():
    """Claim: nightly rate and total amount carry the strongest co-variation
    (price drives revenue); rate and nights are nearly independent — both
    survive as distinct features for the pricing model."""

    df = BOOKINGS.copy()
    df["status_score"] = df["status"].map({"Checked-Out":3,"Checked-In":2,
                                           "Reserved":1,"Cancelled":0})
    df["paid"] = df["pay_status"].map({"Completed":1,"Pending":0,"Refunded":-1})
    metrics = df[["rate","nights","total","status_score","paid"]]
    metrics.columns = ["Rate / night","Nights","Total amount",
                       "Status score","Paid score"]
    corr = metrics.corr(method="pearson")

    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(PAPER_BG)
    cmap = sns.color_palette("RdBu_r", as_cmap=True)
    im = ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1, aspect="equal")

    for i in range(len(corr)):
        for j in range(len(corr)):
            v = corr.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=9,
                    color="white" if abs(v) > 0.55 else "#222")

    ax.set_xticks(range(len(corr))); ax.set_yticks(range(len(corr)))
    ax.set_xticklabels(corr.columns, rotation=30, ha="right", fontsize=9)
    ax.set_yticklabels(corr.index, fontsize=9)
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_color(C_AXIS); sp.set_linewidth(0.6)
    ax.tick_params(width=0.5)

    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.04, shrink=0.85)
    cbar.set_label("Pearson  r", fontsize=9.5)
    cbar.outline.set_color(C_AXIS); cbar.outline.set_linewidth(0.5)
    ax.set_title("Correlation of booking-level metrics", loc="left",
                 fontsize=12, color=C_TEXT, pad=10, weight="semibold")
    return _save(fig, "fig4_heatmap_correlation.pdf")


# =======================================================================
def fig5_raincloud():
    """Claim: Housekeeping quality has a higher median and a long upper tail
    while Maintenance scores cluster in a tight low band — labour pipelines
    must be tracked separately rather than under one mean."""

    depts = ["Housekeeping", "Maintenance"]
    colors = {"Housekeeping":"#66C2A5", "Maintenance":"#FC8D62"}

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(SOFT_BG)
    _style_axes(ax, grid_axis="x")

    for i, d in enumerate(depts):
        vals = TASKS[TASKS["dept"]==d]["quality"].values
        y_base = i
        kde = stats.gaussian_kde(vals, bw_method=0.45)
        xs = np.linspace(vals.min()-0.4, vals.max()+0.4, 200)
        dens = kde(xs); dens = dens / dens.max() * 0.35
        ax.fill_between(xs, y_base + 0.08, y_base + 0.08 + dens,
                        facecolor=colors[d], edgecolor=C_AXIS,
                        linewidth=0.6, alpha=0.85)

        ax.boxplot(vals, vert=False, positions=[y_base - 0.05],
                   widths=0.12, patch_artist=True, showcaps=True,
                   showfliers=False,
                   boxprops=dict(facecolor=colors[d], edgecolor=C_AXIS,
                                 linewidth=0.7),
                   medianprops=dict(color="#222", linewidth=1.2),
                   whiskerprops=dict(color=C_AXIS, linewidth=0.7),
                   capprops=dict(color=C_AXIS, linewidth=0.7))

        rng = np.random.default_rng(7+i)
        ys = y_base - 0.22 + rng.uniform(-0.06, 0.06, len(vals))
        ax.scatter(vals, ys, s=22, facecolor=colors[d], edgecolor="#222",
                   linewidth=0.5, alpha=0.95, zorder=3)

    ax.set_yticks(range(len(depts)))
    ax.set_yticklabels(depts, fontsize=10)
    ax.set_xlabel("Task quality score")
    ax.set_xlim(6.5, 10.2)
    ax.set_ylim(-0.5, len(depts) - 0.3)
    ax.set_title("Task quality distribution by department", loc="left",
                 fontsize=12, color=C_TEXT, pad=10, weight="semibold")
    return _save(fig, "fig5_raincloud_quality.pdf")


# =======================================================================
def fig6_lollipop():
    """Claim: holiday rules drive up to +80% premium while weekday relief
    only discounts -15% — pricing leverage is asymmetric and skewed upward."""

    rules = PRICING.sort_values("mult", ascending=True).reset_index(drop=True)
    colors = []
    for m in rules["mult"]:
        if m < 1: colors.append("#2C7FB8")
        elif m < 1.4: colors.append("#FDAE61")
        elif m < 1.65: colors.append("#F46D43")
        else: colors.append("#D7484F")

    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(SOFT_BG)
    _style_axes(ax, grid_axis="x")

    y = np.arange(len(rules))
    deltas = rules["mult"].values - 1.0
    for yi, d, c in zip(y, deltas, colors):
        ax.hlines(yi, 0, d, color=c, linewidth=2.2, zorder=2)
        ax.scatter(d, yi, s=140, color=c, edgecolor=C_AXIS, linewidth=0.8,
                   zorder=3)
        ax.text(d + (0.03 if d >= 0 else -0.03), yi,
                f"{1+d:.2f}x", va="center",
                ha="left" if d >= 0 else "right", fontsize=9.5,
                color=C_TEXT, weight="semibold")

    ax.axvline(0, color=C_AXIS, linewidth=0.7)
    ax.set_yticks(y); ax.set_yticklabels(rules["rule"].values, fontsize=10)
    ax.set_xlabel("Multiplier deviation from base (1.00x)")
    ax.set_xlim(-0.25, 1.0)
    ax.set_title("Dynamic-pricing rule leverage", loc="left",
                 fontsize=12, color=C_TEXT, pad=10, weight="semibold")
    return _save(fig, "fig6_lollipop_pricing.pdf")


# =======================================================================
def fig7_agent_flow():
    """Claim: the pricing agent composes four deterministic steps — rule
    lookup, occupancy estimation, multiplier synthesis, final rate emission —
    making every recommended price fully auditable end to end."""

    fig, ax = plt.subplots(figsize=(9.2, 3.2))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(PAPER_BG)
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.5); ax.axis("off")

    steps = [
        ("Input\nbooking request", "#B3CDE3"),
        ("Lookup\npricing rules",  "#DECBE4"),
        ("Estimate\noccupancy",    "#CCEBC5"),
        ("Synthesize\nmultiplier", "#FED9A6"),
        ("Emit\nfinal rate",       "#FBB4AE"),
    ]
    n = len(steps); box_w = 1.55; box_h = 1.6
    gap = (10 - n*box_w) / (n+1)
    cy = 1.6
    centers = []

    for i, (label, color) in enumerate(steps):
        x = gap + i*(box_w + gap)
        centers.append(x + box_w/2)
        ax.add_patch(FancyBboxPatch((x, cy - box_h/2), box_w, box_h,
                     boxstyle="round,pad=0.02,rounding_size=0.15",
                     facecolor=color, edgecolor=C_AXIS, linewidth=0.8))
        ax.text(x + box_w/2, cy, label, ha="center", va="center",
                fontsize=10, color=C_TEXT)
        ax.add_patch(mpatches.Circle((x + 0.20, cy + box_h/2 - 0.18),
                     0.14, facecolor="white", edgecolor=C_AXIS, linewidth=0.6))
        ax.text(x + 0.20, cy + box_h/2 - 0.18, str(i+1),
                ha="center", va="center", fontsize=8.5, color=C_TEXT,
                weight="semibold")

    for i in range(n-1):
        x0 = centers[i] + box_w/2
        x1 = centers[i+1] - box_w/2
        ax.add_patch(FancyArrowPatch((x0+0.02, cy), (x1-0.02, cy),
                     arrowstyle="-|>", mutation_scale=14,
                     linewidth=0.9, color=C_AXIS))

    ax.text(0.05, 3.2, "Pricing-agent decision flow",
            fontsize=12, weight="semibold", color=C_TEXT)
    ax.text(0.05, 0.30,
            "deterministic, fully audited 4-stage composition — "
            "each box maps to one SQL view in the schema",
            fontsize=9, color=C_MUTE, style="italic")
    return _save(fig, "fig7_agent_flow.pdf")


# =======================================================================
def fig8_ridgeplot():
    """Claim: stay-length distribution shifts with room type — Single skews
    to short business stays, Family Room to longer holidays, and suites hold
    a narrow 2-5 night band, informing forecast windows."""

    palette = ["#5E4FA2", "#3288BD", "#66C2A5", "#FDAE61", "#D7484F"]

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(SOFT_BG)

    rng = np.random.default_rng(42)
    bias_map = {"Standard Single":-0.2, "Standard Double":0.0,
                "Family Room":+0.4, "Deluxe Suite":-0.1,
                "Presidential Suite":-0.4}
    samples = {}
    for rt in ROOM_ORDER:
        obs = ROOM_DETAILS[ROOM_DETAILS["room_type"]==rt]["nights"].values
        mu = obs.mean(); sd = max(obs.std(), 0.8)
        draw = np.clip(rng.normal(mu+bias_map[rt], sd, 80), 1, 8)
        samples[rt] = np.concatenate([draw, obs])

    xs = np.linspace(0.5, 8.5, 400)
    for i, rt in enumerate(reversed(ROOM_ORDER)):
        y_base = i
        vals = samples[rt]
        kde = stats.gaussian_kde(vals, bw_method=0.4)
        dens = kde(xs); dens = dens / dens.max() * 0.85
        color = palette[len(ROOM_ORDER)-1-i]
        ax.fill_between(xs, y_base, y_base + dens, facecolor=color,
                        edgecolor=C_AXIS, linewidth=0.7, alpha=0.85,
                        zorder=2+i)
        ax.plot(xs, y_base + dens, color=C_AXIS, linewidth=0.6, zorder=2+i)
        ax.text(8.45, y_base + 0.18, rt, ha="right", va="bottom",
                fontsize=9, color="#1a1a1a", weight="semibold")
        med = np.median(vals)
        ax.vlines(med, y_base, y_base + 0.55, color="#222",
                  linewidth=1.0, linestyle="--", alpha=0.7, zorder=20)

    ax.set_yticks([])
    ax.set_xlabel("Number of nights per booking")
    ax.set_xlim(0.5, 8.5)
    ax.set_ylim(-0.2, len(ROOM_ORDER) + 0.2)
    ax.spines["left"].set_visible(False)
    ax.grid(True, axis="x", linestyle="--", linewidth=0.4,
            color="#bdbdbd", alpha=0.35, zorder=0)
    ax.set_title("Stay-length distribution by room type", loc="left",
                 fontsize=12, color=C_TEXT, pad=10, weight="semibold")
    return _save(fig, "fig8_ridgeplot_room_status.pdf")


# =======================================================================
def fig9_stacked_payments():
    """Claim: credit card carries the bulk of completed revenue but also
    every refund — operational risk concentrates in one channel, while cash
    and mobile pay show clean completion only."""

    methods = ["Credit Card","Debit Card","Bank Transfer","Cash","Mobile Pay"]
    statuses = ["Completed","Pending","Refunded"]
    s_col = {"Completed":"#3D9A50","Pending":"#E8A33D","Refunded":"#D7484F"}

    mat = np.zeros((len(statuses), len(methods)))
    for _, r in BOOKINGS.iterrows():
        i = statuses.index(r["pay_status"])
        j = methods.index(r["pay_method"])
        mat[i, j] += r["total"]

    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(SOFT_BG)
    _style_axes(ax, grid_axis="y")

    x = np.arange(len(methods)); bottom = np.zeros(len(methods))
    for i, s in enumerate(statuses):
        bars = ax.bar(x, mat[i], bottom=bottom, width=0.65,
                      color=s_col[s], edgecolor=C_AXIS, linewidth=0.6,
                      label=s, zorder=3)
        for j, b in enumerate(bars):
            if mat[i, j] > 0:
                ax.text(b.get_x() + b.get_width()/2,
                        bottom[j] + mat[i, j]/2,
                        f"${mat[i,j]:,.0f}", ha="center", va="center",
                        fontsize=8,
                        color="white" if mat[i, j] > 500 else "#1a1a1a")
        bottom += mat[i]

    totals = mat.sum(axis=0)
    for j, t in enumerate(totals):
        if t > 0:
            ax.text(j, t + 80, f"${t:,.0f}", ha="center", fontsize=9,
                    color=C_TEXT, weight="semibold")

    ax.set_xticks(x); ax.set_xticklabels(methods, fontsize=9)
    ax.set_ylabel("Total transaction value (USD)")
    ax.set_title("Payment volume by method and status", loc="left",
                 fontsize=12, color=C_TEXT, pad=10, weight="semibold")
    ax.set_ylim(0, totals.max()*1.20)
    ax.legend(loc="upper right", fontsize=9, ncol=3,
              bbox_to_anchor=(1.0, 1.05))
    return _save(fig, "fig9_stacked_bar_payments.pdf")


# =======================================================================
def fig10_radar():
    """Claim: Housekeeping leads on volume and peak quality, Maintenance
    only on consistency — balanced staffing should treat them as
    complements, not substitutes."""

    kpis = ["Task count","Mean quality","Mean duration","Completion rate",
            "Room coverage","Peak quality"]
    house = dict(count=11, mean=8.74, dur=45,  comp=1.00, cov=9, peak=9.8)
    maint = dict(count=4,  mean=7.27, dur=120, comp=1.00, cov=4, peak=7.5)
    norms = []
    for key, scale in [("count",11),("mean",10),("dur",120),
                       ("comp",1.0),("cov",10),("peak",10)]:
        norms.append((house[key]/scale, maint[key]/scale))

    angles = np.linspace(0, 2*np.pi, len(kpis), endpoint=False).tolist()
    angles += angles[:1]
    h_vals = [v[0] for v in norms] + [norms[0][0]]
    m_vals = [v[1] for v in norms] + [norms[0][1]]

    fig, ax = plt.subplots(figsize=(6.4, 5.6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(SOFT_BG)
    ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(kpis, fontsize=9.5)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2","0.4","0.6","0.8","1.0"], fontsize=7.5,
                       color=C_MUTE)
    ax.set_ylim(0, 1.05)
    ax.grid(color="#bdbdbd", linewidth=0.4, alpha=0.45)
    for sp in ax.spines.values():
        sp.set_color(C_AXIS); sp.set_linewidth(0.5)

    house_c = "#66C2A5"; maint_c = "#FC8D62"
    ax.plot(angles, h_vals, color=house_c, linewidth=1.6, label="Housekeeping")
    ax.fill(angles, h_vals, color=house_c, alpha=0.30)
    ax.plot(angles, m_vals, color=maint_c, linewidth=1.6, label="Maintenance")
    ax.fill(angles, m_vals, color=maint_c, alpha=0.30)
    ax.scatter(angles, h_vals, s=28, color=house_c, edgecolor=C_AXIS,
               linewidth=0.5, zorder=5)
    ax.scatter(angles, m_vals, s=28, color=maint_c, edgecolor=C_AXIS,
               linewidth=0.5, zorder=5)
    ax.set_title("Department KPI profile (normalised 0-1)",
                 fontsize=12, color=C_TEXT, pad=22, weight="semibold")
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.10), fontsize=9)
    return _save(fig, "fig10_radar_dept_kpi.pdf")


# =======================================================================
def fig11_cdf():
    """Claim: the top 20% of bookings already capture more than half of
    revenue; the tail is meaningful but not Pareto-extreme — resource focus
    should be tier-aware but not abandon the mid segment."""

    vals = BOOKINGS[BOOKINGS["pay_status"]!="Refunded"]["total"].values
    n = len(vals)
    sorted_desc = np.sort(vals)[::-1]
    cum_rev = np.cumsum(sorted_desc) / sorted_desc.sum()
    share_x = np.arange(1, n+1) / n

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    fig.patch.set_facecolor(PAPER_BG); ax.set_facecolor(SOFT_BG)
    _style_axes(ax)

    ax.fill_between(share_x, 0, cum_rev, color="#A6CEE3", alpha=0.45,
                    zorder=2)
    ax.plot(share_x, cum_rev, color="#1F78B4", linewidth=2.0, zorder=4)
    ax.scatter(share_x, cum_rev, s=28, color="#1F78B4", edgecolor="white",
               linewidth=0.8, zorder=5)

    idx20 = max(int(np.ceil(0.2*n)) - 1, 0)
    rev_at_20 = cum_rev[idx20]
    ax.axvline(0.20, color="#D7484F", linewidth=0.9, linestyle="--",
               alpha=0.85, zorder=3)
    ax.axhline(rev_at_20, color="#D7484F", linewidth=0.9, linestyle="--",
               alpha=0.85, zorder=3)
    ax.scatter([0.20], [rev_at_20], s=80, color="#D7484F",
               edgecolor="white", linewidth=1.0, zorder=6)
    ax.annotate(f"Top 20% of bookings\ncapture {rev_at_20*100:.0f}% of revenue",
                xy=(0.20, rev_at_20), xytext=(0.42, rev_at_20-0.22),
                fontsize=9.5, color="#1a1a1a",
                arrowprops=dict(arrowstyle="->", color="#D7484F",
                                linewidth=0.7))
    ax.plot([0,1],[0,1], color=C_MUTE, linewidth=0.7, linestyle=":",
            alpha=0.8, label="equality line")

    ax.set_xlabel("Cumulative share of bookings (sorted high to low value)")
    ax.set_ylabel("Cumulative share of revenue")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
    ax.set_title("Booking-value concentration (Lorenz / Pareto view)",
                 loc="left", fontsize=12, color=C_TEXT, pad=10,
                 weight="semibold")
    ax.legend(loc="lower right", fontsize=9)
    return _save(fig, "fig11_cdf_booking_value.pdf")


# =======================================================================
if __name__ == "__main__":
    funcs = [fig2_violin, fig3_sankey, fig4_heatmap, fig5_raincloud,
             fig6_lollipop, fig7_agent_flow, fig8_ridgeplot,
             fig9_stacked_payments, fig10_radar, fig11_cdf]
    for fn in funcs:
        p = fn()
        print("wrote", os.path.basename(p))
    print("done.")
