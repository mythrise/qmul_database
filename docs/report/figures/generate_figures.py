"""
Publication-grade figures for EBU5503 Hotel DB report.
DESIGN PHILOSOPHY: Nature/Science light-mode aesthetic
  — soft warm paper background, thin charcoal axes, restrained type
  — each chart picks ITS OWN multi-color palette that fits its semantics
  — palettes drawn from seaborn Set2 / pastel / Spectral / NPG-inspired
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

OUT = os.path.dirname(os.path.abspath(__file__))

# Nature/Science publication style — light, airy, restrained
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.labelsize": 10.5,
    "axes.titlesize": 11.5,
    "axes.edgecolor": "#333",
    "axes.linewidth": 0.7,
    "axes.labelcolor": "#222",
    "xtick.color": "#444",
    "ytick.color": "#444",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,
})

C_TITLE = "#2C3E50"     # title slate
C_PAPER = "#F8F5F0"     # soft paper bg for backgrounds

# =================== Data ===================
bookings = pd.DataFrame([
    [1, 2, "Checked-Out", 450.00, 3, "Deluxe Suite",       1350.00, "Completed", "Credit Card"],
    [2, 3, "Checked-Out", 360.00, 4, "Family Room",        2016.00, "Completed", "Credit Card"],
    [3, 1, "Checked-Out",  68.00, 3, "Standard Single",     204.00, "Completed", "Bank Transfer"],
    [4, 4, "Cancelled",   195.00, 4, "Standard Double",     195.00, "Refunded",  "Credit Card"],
    [5, 5, "Checked-Out", 212.50, 5, "Deluxe Suite",       1062.50, "Completed", "Bank Transfer"],
    [6, 10,"Checked-Out", 110.50, 3, "Standard Double",     663.00, "Completed", "Debit Card"],
    [7, 6, "Checked-Out",  68.00, 4, "Standard Single",     272.00, "Completed", "Mobile Pay"],
    [8, 2, "Checked-Out", 212.50, 2, "Deluxe Suite",        425.00, "Completed", "Credit Card"],
    [9, 7, "Cancelled",   425.00, 4, "Presidential Suite",  425.00, "Refunded",  "Credit Card"],
    [10,8, "Checked-Out",  68.00, 2, "Standard Single",     136.00, "Completed", "Cash"],
    [11,9, "Checked-Out", 110.50, 5, "Standard Double",     552.50, "Completed", "Debit Card"],
    [12,1, "Checked-In",  110.50, 7, "Standard Double",     323.00, "Pending",   "Credit Card"],
    [13,4, "Confirmed",   110.50, 3, "Standard Double",       0.00, "Pending",   "Credit Card"],
    [14,7, "Confirmed",   500.00, 4, "Presidential Suite",    0.00, "Pending",   "Credit Card"],
    [15,5, "Checked-In",  212.50, 5, "Deluxe Suite",          0.00, "Pending",   "Credit Card"],
], columns=["bid","guest","status","rate","nights","room_type","pay_amt","pay_status","method"])

tasks = pd.DataFrame([
    [3,"Housekeeping","Cleaning",75,9.5], [3,"Housekeeping","Inspection",30,8.0],
    [4,"Housekeeping","Cleaning",90,7.5], [4,"Housekeeping","Cleaning",45,8.5],
    [3,"Housekeeping","Setup",40,9.0],    [5,"Maintenance","Maintenance",150,7.0],
    [4,"Housekeeping","Cleaning",40,9.0], [3,"Housekeeping","Cleaning",90,9.8],
    [3,"Housekeeping","Inspection",45,8.5],[4,"Housekeeping","Cleaning",35,8.0],
    [4,"Housekeeping","Cleaning",50,8.5], [3,"Housekeeping","Setup",50,9.0],
    [5,"Maintenance","Maintenance",20,7.5],[3,"Housekeeping","Setup",55,9.2],
], columns=["staff","dept","type","duration","quality"])

pricing_rules = pd.DataFrame([
    ["Christmas & NY Peak", 1.80, 10, "Dec 20 – Jan 5"],
    ["Spring Festival",     1.50,  8, "Jan 28 – Feb 4"],
    ["Summer High Season",  1.30,  5, "Jun 1 – Aug 31"],
    ["Weekday Discount",    0.85,  1, "Jan 6 – May 31"],
], columns=["event","multiplier","priority","window"])

loyalty = pd.DataFrame([
    [2,"Platinum",28500],[1,"Gold",12300],[5,"Silver",6800],
    [8,"Bronze",1500],[3,"Silver",4200],[10,"Bronze",800],
], columns=["guest","tier","points"])

# ===================== Figure 2: Violin — Set2 multi-color =====================
def fig2_violin():
    valid = bookings[bookings["status"] != "Cancelled"].copy()
    rows = []
    rng = np.random.default_rng(42)
    for _, r in valid.iterrows():
        for _ in range(int(r["nights"])):
            rows.append([r["room_type"], r["rate"] + rng.normal(0, r["rate"]*0.04)])
    df = pd.DataFrame(rows, columns=["Room Type", "Nightly Revenue (USD)"])
    order = ["Standard Single", "Standard Double", "Family Room",
             "Deluxe Suite", "Presidential Suite"]
    df = df[df["Room Type"].isin(order)]

    # Set2 — Nature/Science staple: 5 distinguishable pastels
    palette = ["#66C2A5","#FC8D62","#8DA0CB","#E78AC3","#A6D854"]

    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    sns.violinplot(data=df, x="Room Type", y="Nightly Revenue (USD)",
                   order=order, hue="Room Type", palette=palette,
                   inner="quartile", linewidth=0.9, legend=False, ax=ax)
    sns.stripplot(data=df, x="Room Type", y="Nightly Revenue (USD)",
                  order=order, color="#1a1a1a", size=1.9, alpha=0.42, ax=ax)
    ax.set_title("Nightly Revenue Distribution by Room Category",
                 fontweight="bold", color=C_TITLE, pad=8)
    ax.set_xlabel("")
    ax.grid(axis="y", linestyle=":", alpha=0.35, color="#999")
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=8)
    plt.savefig(os.path.join(OUT, "fig2_violin_revenue.pdf"))
    plt.close()
    print("[OK] fig2_violin_revenue.pdf")

# ===================== Figure 3: Sankey — warm Spectral =====================
def fig3_sankey():
    df = bookings.merge(loyalty, on="guest", how="left")
    df["tier"] = df["tier"].fillna("Non-member")

    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 10)

    tiers = ["Platinum", "Gold", "Silver", "Bronze", "Non-member"]
    statuses = ["Checked-Out", "Checked-In", "Confirmed", "Cancelled"]

    # Tier — luxury-to-casual gradient (Spectral)
    tier_palette = ["#5E4FA2","#3288BD","#66C2A5","#ABDDA4","#D9D9D9"]
    # Status — semantic (green good, blue ongoing, gold pending, red bad)
    status_palette = {
        "Checked-Out": "#3D9A50",
        "Checked-In":  "#2C7FB8",
        "Confirmed":   "#E8A33D",
        "Cancelled":   "#D7484F",
    }
    tier_color = dict(zip(tiers, tier_palette))

    def column(items, x, source_key, total_h=7.4, gap=0.22, y0=1.1):
        sizes = [max((df[source_key] == it).sum(), 0.001) for it in items]
        s = sum(sizes)
        heights = [v/s*(total_h - gap*(len(items)-1)) for v in sizes]
        rects = {}; y = y0
        for it, h in zip(items, heights):
            rects[it] = (x, y, 0.65, h); y += h + gap
        return rects

    c1 = column(tiers, 0.7, "tier")
    c2 = column(statuses, 6.2, "status")

    def draw_col(col, color_map):
        for name, (x, y, w, h) in col.items():
            ax.add_patch(plt.Rectangle((x, y), w, h,
                          color=color_map.get(name, "#bbb"),
                          alpha=0.92, ec="white", lw=0.5))
            ax.text(x + w + 0.10, y + h/2, name, va="center",
                    fontsize=8.5, color="#222")

    draw_col(c1, tier_color)
    draw_col(c2, status_palette)

    # ribbons
    for s_name, (sx, sy, sw, sh) in c1.items():
        sub = df[df["tier"] == s_name]
        if sub.empty: continue
        y_cursor = sy
        for d_name, (dx, dy, dw, dh) in c2.items():
            n = (sub["status"] == d_name).sum()
            if n == 0: continue
            frac = n / len(sub)
            src_seg_h = sh * frac
            dst_share = n / max((df["status"] == d_name).sum(), 1)
            dst_seg_h = dh * dst_share
            xs = np.linspace(sx + sw, dx, 60)
            t = (xs - xs[0]) / (xs[-1] - xs[0])
            ease = 3*t**2 - 2*t**3
            top = (y_cursor + src_seg_h) + (dy + dst_seg_h - (y_cursor + src_seg_h)) * ease
            bot = y_cursor + (dy - y_cursor) * ease
            ax.fill_between(xs, bot, top, color=status_palette[d_name],
                            alpha=0.22, lw=0)
            y_cursor += src_seg_h

    ax.text(0.95, 9.0, "Loyalty Tier",   fontsize=10, fontweight="bold", color=C_TITLE)
    ax.text(6.5,  9.0, "Booking Status", fontsize=10, fontweight="bold", color=C_TITLE)
    ax.text(5.0, 9.65, "Customer Journey: Loyalty Tier → Booking Outcome",
            ha="center", fontsize=12, fontweight="bold", color=C_TITLE)
    plt.savefig(os.path.join(OUT, "fig3_sankey_flow.pdf"))
    plt.close()
    print("[OK] fig3_sankey_flow.pdf")

# ===================== Figure 4: Heatmap — classic Nature RdBu =====================
def fig4_heatmap():
    valid = bookings[bookings["status"] != "Cancelled"].copy()
    valid["total_revenue"] = valid["rate"] * valid["nights"]
    valid = valid.merge(loyalty, on="guest", how="left")
    valid["loyalty_pts"] = valid["points"].fillna(0)
    valid["is_pending"] = (valid["pay_status"] == "Pending").astype(int)
    metrics = valid[["rate","nights","total_revenue","loyalty_pts","is_pending"]]
    metrics.columns = ["Nightly Rate","Stay Nights","Total Revenue",
                       "Loyalty Points","Pending Payment"]
    corr = metrics.corr()

    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-1, vmax=1, square=True,
                cbar_kws={"shrink": 0.75, "label": "Pearson r"},
                linewidths=0.5, linecolor="white",
                annot_kws={"fontsize": 9, "color":"#1a1a1a"}, ax=ax)
    ax.set_title("Correlation Matrix of Booking Metrics",
                 fontweight="bold", color=C_TITLE, pad=8)
    plt.xticks(rotation=25, ha="right")
    plt.yticks(rotation=0)
    plt.savefig(os.path.join(OUT, "fig4_heatmap_corr.pdf"))
    plt.close()
    print("[OK] fig4_heatmap_corr.pdf")

# ===================== Figure 5: Raincloud — fresh teal-coral =====================
def fig5_raincloud():
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    depts = sorted(tasks["dept"].unique())
    dept_colors = {"Housekeeping": "#2A9D8F", "Maintenance": "#E76F51"}
    for i, d in enumerate(depts):
        vals = tasks.loc[tasks["dept"] == d, "quality"].values
        if len(vals) == 0: continue
        col = dept_colors.get(d, "#888")
        parts = ax.violinplot([vals], positions=[i], showmeans=False,
                              showmedians=False, showextrema=False, widths=0.7)
        for pc in parts["bodies"]:
            verts = pc.get_paths()[0].vertices
            verts[:, 0] = np.clip(verts[:, 0], i, i + 1)
            pc.set_facecolor(col); pc.set_alpha(0.42); pc.set_edgecolor("none")
        rng = np.random.default_rng(i)
        xj = i - 0.10 - rng.uniform(0, 0.18, len(vals))
        ax.scatter(xj, vals, color=col, s=28, alpha=0.85,
                   edgecolor="white", linewidth=0.6)
        bp = ax.boxplot(vals, positions=[i - 0.3], widths=0.13,
                        patch_artist=True, showfliers=False)
        for patch in bp["boxes"]:
            patch.set(facecolor=col, alpha=0.9, edgecolor="#222", linewidth=0.7)
        for med in bp["medians"]: med.set(color="white", lw=1.4)

    ax.set_xticks(range(len(depts))); ax.set_xticklabels(depts)
    ax.set_ylabel("Quality Score (0–10)")
    ax.set_title("Task Quality Distribution by Department",
                 fontweight="bold", color=C_TITLE, pad=8)
    ax.set_ylim(6.5, 10.5)
    ax.grid(axis="y", linestyle=":", alpha=0.35, color="#999")
    ax.spines[["top", "right"]].set_visible(False)
    plt.savefig(os.path.join(OUT, "fig5_raincloud_quality.pdf"))
    plt.close()
    print("[OK] fig5_raincloud_quality.pdf")

# ===================== Figure 6: Lollipop — semantic 3-color =====================
def fig6_lollipop():
    df = pricing_rules.sort_values("multiplier")
    fig, ax = plt.subplots(figsize=(7.5, 3.0))
    def pick(m):
        if m < 1:    return "#2A9D8F"   # discount = teal
        if m >= 1.5: return "#D7484F"   # high surge = coral red
        return "#F4A261"                # moderate = warm orange
    colors = [pick(m) for m in df["multiplier"]]
    y = np.arange(len(df))
    ax.hlines(y, 1.0, df["multiplier"], colors=colors, lw=2.2, alpha=0.85)
    ax.scatter(df["multiplier"], y, s=200, c=colors,
               edgecolor="#222", linewidth=0.9, zorder=3)
    ax.axvline(1.0, color="#666", linestyle="--", lw=0.8, alpha=0.7)
    for i, (m, e, w) in enumerate(zip(df["multiplier"], df["event"], df["window"])):
        pct = (m - 1) * 100
        sign = "+" if pct >= 0 else ""
        ax.text(m + (0.04 if m >= 1 else -0.04), i,
                f"  {m:.2f}×  ({sign}{pct:.0f}%)",
                va="center", ha="left" if m >= 1 else "right",
                fontsize=8.8, fontweight="bold", color="#222")
        ax.text(0.36, i - 0.32, w, fontsize=7.3, color="#666", style="italic")

    ax.set_yticks(y); ax.set_yticklabels(df["event"], fontsize=9.5)
    ax.set_xlabel("Price Multiplier (Base = 1.00)")
    ax.set_xlim(0.45, 2.05)
    ax.set_title("Dynamic Pricing Rules — Multiplier Effect",
                 fontweight="bold", color=C_TITLE, pad=8)
    ax.grid(axis="x", linestyle=":", alpha=0.35, color="#999")
    ax.spines[["top", "right"]].set_visible(False)
    plt.savefig(os.path.join(OUT, "fig6_lollipop_pricing.pdf"))
    plt.close()
    print("[OK] fig6_lollipop_pricing.pdf")

# ===================== Figure 7: Agent Flow — soft pastel chain =====================
def fig7_agent_flow():
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    fig, ax = plt.subplots(figsize=(8.5, 2.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 2.4); ax.axis("off")

    # Soft pastel cascade — gentle Nature-style flow
    nodes = [
        ("Input\n(date, type_id)",          0.3, 0.6, 1.6, 1.0, "#B0BEC5", "#37474F"),
        ("Query active\npricing rule",      2.1, 0.6, 1.6, 1.0, "#90CAF9", "#0D47A1"),
        ("Compute\noccupancy",              3.9, 0.6, 1.6, 1.0, "#A5D6A7", "#1B5E20"),
        ("Combine\n$P_\\text{base} \\times m \\times f$",   5.7, 0.6, 1.6, 1.0, "#FFCC80", "#E65100"),
        ("Suggested\nprice",                7.5, 0.6, 1.6, 1.0, "#CE93D8", "#4A148C"),
    ]
    for txt, x, y, w, h, c, tc in nodes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                     linewidth=0, facecolor=c, alpha=0.95))
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center",
                fontsize=9.2, color=tc, fontweight="bold")

    pairs = [(0,1),(1,2),(2,3),(3,4)]
    for a, b in pairs:
        x1 = nodes[a][1] + nodes[a][3]; y1 = nodes[a][2] + nodes[a][4]/2
        x2 = nodes[b][1];               y2 = nodes[b][2] + nodes[b][4]/2
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle="-|>", mutation_scale=11,
                                     lw=1.0, color="#555"))

    ax.text(5.0, 2.0, "Pricing Agent — Database-Driven Decision Flow",
            ha="center", fontsize=11.5, fontweight="bold", color=C_TITLE)
    plt.savefig(os.path.join(OUT, "fig7_agent_flow.pdf"))
    plt.close()
    print("[OK] fig7_agent_flow.pdf")

# ===================== Run =====================
if __name__ == "__main__":
    fig2_violin()
    fig3_sankey()
    fig4_heatmap()
    fig5_raincloud()
    fig6_lollipop()
    fig7_agent_flow()
    print("\nAll figures generated in:", OUT)
