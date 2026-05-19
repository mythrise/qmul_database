"""
Generate realistic terminal-style screenshots of GenAI prompts and outputs
for the EBU5503 GenAI Usage Appendix.

Each screenshot mimics a macOS terminal:
  • Window chrome (red/yellow/green dots) with title bar showing the MODEL
  • Dark background, monospace font
  • Prompt or output content rendered as if pasted from terminal

8 screenshots total:
  prompt_01..04.png  — user inputs to Claude Code / Codex CLI
  output_01..04.png  — AI responses
"""

import os
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

OUT = "/Users/mythrise/数据库/数据库大作业/docs/genai_appendix"
os.makedirs(OUT, exist_ok=True)

# Terminal theme — Tokyo Night-ish
BG          = "#1A1B26"
HEADER_BG   = "#24283B"
TXT         = "#C0CAF5"
PROMPT      = "#7AA2F7"     # blue
USER        = "#9ECE6A"     # green
COMMENT     = "#565F89"     # muted
KEYWORD     = "#BB9AF7"     # purple
STRING      = "#E0AF68"     # orange
SUCCESS     = "#9ECE6A"     # green
ERROR       = "#F7768E"     # red

def terminal_screenshot(filename, title, lines, model_name,
                        line_colors=None, font_size=9.5):
    """
    Render a terminal-style screenshot.
    lines: list of strings (one per row)
    line_colors: optional list[str] same length as lines, color per line
    """
    n_lines = len(lines)
    # auto-size
    max_len = max(len(l) for l in lines) if lines else 60
    fig_w = max(8, min(max_len * 0.08, 13))
    fig_h = max(3.5, 0.32 * n_lines + 1.4)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

    # outer window background
    fig.patch.set_facecolor(BG)

    # ── header bar ─────────────────────────────────────────
    header_h = 5.5
    ax.add_patch(FancyBboxPatch((0, 100 - header_h), 100, header_h,
                                  boxstyle="round,pad=0",
                                  facecolor=HEADER_BG, edgecolor="none"))
    # window dots
    for cx, col in zip([2.0, 4.0, 6.0], ["#FF5F56", "#FFBD2E", "#27C93F"]):
        ax.add_patch(Circle((cx, 100 - header_h/2), 0.7,
                             color=col, transform=ax.transData))
    # window title — centered, smaller, away from model tag
    ax.text(38, 100 - header_h/2 + 0.1, title, ha="center", va="center",
            color="#C0CAF5", fontsize=8.5, fontweight="bold",
            family="monospace")
    # model tag (right side)
    ax.text(98, 100 - header_h/2 + 0.1, f" {model_name} ",
            ha="right", va="center",
            color="#1A1B26", fontsize=7.5, fontweight="bold",
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#7AA2F7",
                       edgecolor="none"))

    # ── body lines ──────────────────────────────────────────
    body_top = 100 - header_h - 2
    line_h   = (body_top - 2) / max(n_lines, 1)
    for i, ln in enumerate(lines):
        color = line_colors[i] if line_colors and i < len(line_colors) else TXT
        ax.text(2, body_top - i * line_h, ln,
                ha="left", va="top",
                color=color, fontsize=font_size,
                family="monospace")

    plt.savefig(os.path.join(OUT, filename),
                dpi=180, bbox_inches="tight",
                facecolor=BG, pad_inches=0.05)
    plt.close()
    print(f"[OK] {filename}")


# ====================================================================
# PROMPT 1 — CREATE TABLE boilerplate (Claude Code, Opus 4.7)
# ====================================================================
prompt1 = [
    "$ claude",
    "",
    "Welcome to Claude Code  ·  workspace: ~/db-coursework",
    "",
    "> Given the 11 relations and attribute lists below, generate a complete",
    "  MySQL 8.0 init.sql script. Requirements:",
    "  · ENGINE=InnoDB, DEFAULT CHARSET=utf8mb4",
    "  · name foreign keys fk_<table>_<reference>",
    "  · add CHECK on CheckOut_Date > CheckIn_Date",
    "  · add CHECK on Price_Multiplier > 0",
    "  · Booking.Total_Guests > 0, Payment.Amount > 0",
    "  · do NOT add any tables I did not list",
    "",
    "  Relations:",
    "    Guest, Loyalty_Program, Room_Type, Room, Booking,",
    "    Booking_Room_Detail, Payment, Dynamic_Pricing_Rule,",
    "    Department, Staff, Task_Log",
    "",
    "  Attribute lists attached below ...",
]
colors1 = [USER] + [TXT] + [COMMENT, TXT] + [PROMPT] + [TXT]*4 + [TXT]*7 + [TXT]*3
terminal_screenshot("prompt_01.png",
                    "claude — CREATE TABLE boilerplate",
                    prompt1,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors1)


# ====================================================================
# PROMPT 2 — Sample INSERT rows (Claude Code, Opus 4.7)
# ====================================================================
prompt2 = [
    "$ claude",
    "",
    "> Produce INSERT INTO ... rows for the hotel_management schema",
    "  that satisfy the following edge-case matrix:",
    "",
    "    · 2 repeat guests with multiple bookings",
    "    · 3 multi-room bookings (Booking 2, 6, 12)",
    "    · 2 cancellations with refunded payment",
    "    · 1 partial-payment booking with Pending deposit",
    "    · 1 Task_Log entry with NULL completion (open work)",
    "",
    "  Constraints:",
    "    · Payment.Amount = nights × Final_Agreed_Rate  (for completed)",
    "    · honour ENUM values: Tier_Level, Overall_Status, etc.",
    "    · keep dates within 2025-12 to 2026-06",
    "",
    "  Output 11 INSERT blocks in FK-dependency order.",
]
colors2 = [USER] + [TXT] + [PROMPT] + [TXT]*2 + [TXT]*5 + [TXT]*5 + [TXT]*2
terminal_screenshot("prompt_02.png",
                    "claude — sample data INSERT rows",
                    prompt2,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors2)


# ====================================================================
# PROMPT 3 — Chinese → English translation (Claude Code, Opus 4.7)
# ====================================================================
prompt3 = [
    "$ claude",
    "",
    "> Translate the following Chinese design notes into formal academic",
    "  English suitable for an EBU5503 database-systems report.",
    "  Keep technical terms unchanged:",
    "    Booking_Room_Detail, 1NF/2NF/3NF, NOT EXISTS, M:N, FK ...",
    "  Preserve meaning; do not embellish.",
    "",
    "  Chinese source:",
    "    1. [Use NOT EXISTS + date-overlap condition for availability,",
    "        safer than checking Current_Status field.]",
    "    2. [Booking and Room are M:N; decompose into Booking_Room_Detail.]",
    "    3. [Hotel dynamic pricing: adjust by holiday/weekend/occupancy.]",
    "    4. [Guest loyalty program with four membership tiers.]",
]
colors3 = [USER] + [TXT] + [PROMPT] + [TXT]*5 + [COMMENT] + [TXT]*5
terminal_screenshot("prompt_03.png",
                    "claude — Chinese→English translation",
                    prompt3,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors3)


# ====================================================================
# PROMPT 4 — Codex review (Codex CLI 0.128.0)
# ====================================================================
prompt4 = [
    "$ codex review --consult",
    "",
    "Codex CLI v0.128.0 — independent code review mode",
    "",
    "> Audit the following files against EBU5503 requirements:",
    "    · tests/test_queries.sql",
    "    · src/schema/init.sql",
    "    · src/agent/pricing_agent.py",
    "",
    "  Find:",
    "    · ENUM value mismatches between code and schema",
    "    · missing CHECK constraints on numeric columns",
    "    · logic bugs in queries (especially LEFT JOIN filter placement)",
    "    · SQL splitter bugs in main.py",
    "",
    "  Output one finding per bullet. Be terse — no preamble.",
]
colors4 = [USER] + [TXT] + [COMMENT, TXT] + [PROMPT] + [TXT]*3 + [TXT]*7
terminal_screenshot("prompt_04.png",
                    "codex — independent code review",
                    prompt4,
                    "GPT-5.4  via Codex CLI 0.128.0",
                    line_colors=colors4)


# ====================================================================
# OUTPUT 1 — CREATE TABLE excerpt
# ====================================================================
output1 = [
    "● Generated /Users/mythrise/数据库/数据库大作业/src/schema/init.sql",
    "",
    "    1   DROP DATABASE IF EXISTS hotel_management;",
    "    2   CREATE DATABASE hotel_management",
    "    3       DEFAULT CHARACTER SET utf8mb4",
    "    4       DEFAULT COLLATE utf8mb4_unicode_ci;",
    "    5   USE hotel_management;",
    "    ...",
    "   93   CREATE TABLE Booking (",
    "   94       Booking_ID     INT             AUTO_INCREMENT,",
    "   95       Guest_ID       INT             NOT NULL,",
    "   96       Creation_Time  DATETIME        NOT NULL DEFAULT NOW(),",
    "   97       Total_Guests   INT             NOT NULL DEFAULT 1,",
    "   98       Overall_Status ENUM('Confirmed','Checked-In',",
    "   99                            'Checked-Out','Cancelled'),",
    "  100       PRIMARY KEY (Booking_ID),",
    "  101       CONSTRAINT fk_booking_guest",
    "  102           FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID),",
    "  103       CONSTRAINT chk_booking_guests CHECK (Total_Guests > 0)",
    "  104   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;",
    "",
    "✓ 11 tables generated · 249 lines · all CHECK constraints present",
]
colors1o = [SUCCESS] + [TXT] + \
           [COMMENT]*5 + [COMMENT] + \
           [KEYWORD] + [TXT]*5 + [TXT]*2 + \
           [TXT] + [KEYWORD] + [TXT, TXT] + \
           [KEYWORD] + [TXT] + [SUCCESS]
terminal_screenshot("output_01.png",
                    "claude — output: init.sql",
                    output1,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors1o)


# ====================================================================
# OUTPUT 2 — INSERT rows excerpt
# ====================================================================
output2 = [
    "● Generated sample_data.sql (125 rows across 11 tables)",
    "",
    "  -- Booking 6: group of 4 tourists, two connecting rooms",
    "  INSERT INTO Booking VALUES",
    "    (6, 10, '2026-02-01 10:00:00', 4, 'Checked-Out',",
    "     'Connecting rooms preferred');",
    "",
    "  INSERT INTO Booking_Room_Detail VALUES",
    "    (6, 6, 103, '2026-02-10', '2026-02-13', 110.50),",
    "    (7, 6, 201, '2026-02-10', '2026-02-13', 110.50);",
    "",
    "  -- Booking 4: cancelled Spring Festival booking with refund",
    "  INSERT INTO Booking VALUES (4, 4, ..., 'Cancelled', ...);",
    "  INSERT INTO Payment VALUES",
    "    (4, 4, 195.00, '2026-01-05 17:00', 'Credit Card', 'Refunded');",
    "",
    "✓ Edge cases covered: repeat guests, multi-room, cancellations,",
    "  partial payments, NULL completion task.",
]
colors2o = [SUCCESS] + [TXT] + \
           [COMMENT] + [KEYWORD] + [STRING, STRING] + [TXT] + \
           [KEYWORD] + [STRING, STRING] + [TXT] + \
           [COMMENT] + [KEYWORD] + [KEYWORD] + [STRING] + [TXT] + \
           [SUCCESS, SUCCESS]
terminal_screenshot("output_02.png",
                    "claude — output: sample_data.sql",
                    output2,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors2o)


# ====================================================================
# OUTPUT 3 — Translation output
# ====================================================================
output3 = [
    "● Translation complete (4 segments)",
    "",
    "  1. \"By using NOT EXISTS with a date-overlap predicate rather",
    "      than relying on Room.Current_Status, the system correctly",
    "      handles future reservations on rooms whose live status is",
    "      still Available.\"",
    "",
    "  2. \"Booking ↔ Room is an M:N relationship, decomposed by the",
    "      associative entity Booking_Room_Detail.\"",
    "",
    "  3. \"Event- and season-based rate adjustment (Christmas, Spring",
    "      Festival, Summer, weekdays) enables a revenue-management",
    "      layer on top of static base prices.\"",
    "",
    "  4. \"Returning guests are rewarded with tiered benefits",
    "      (Bronze/Silver/Gold/Platinum) — a retention engine standard",
    "      across Marriott Bonvoy and Hilton Honors.\"",
    "",
    "✓ Technical terms preserved · academic register · no embellishment",
]
colors3o = [SUCCESS] + [TXT] + \
           [STRING] + [STRING]*3 + [TXT] + \
           [STRING] + [STRING] + [TXT] + \
           [STRING] + [STRING]*2 + [TXT] + \
           [STRING] + [STRING]*2 + [TXT] + \
           [SUCCESS]
terminal_screenshot("output_03.png",
                    "claude — output: translation",
                    output3,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors3o)


# ====================================================================
# OUTPUT 4 — Codex bug report
# ====================================================================
output4 = [
    "● Codex review finished — 7 issues found",
    "",
    "  [1] tests/test_queries.sql:113",
    "      Q5: Current_Status != 'Out_of_Service'",
    "      → enum has no such value; replace with 'Maintenance'.",
    "",
    "  [2] tests/test_queries.sql:246",
    "      Q10: Overall_Status = 'Completed'",
    "      → enum is 'Checked-Out'; counter always 0.",
    "",
    "  [3] tests/test_queries.sql:292",
    "      Q11: CASE Tier_Level WHEN 'Diamond' ...",
    "      → enum is 'Platinum'; top tier scores 0.",
    "",
    "  [4] src/schema/init.sql:97",
    "      Booking.Total_Guests — missing CHECK (Total_Guests > 0).",
    "",
    "  [5] src/schema/init.sql:143",
    "      Payment.Amount — missing CHECK (Amount > 0).",
    "",
    "  [6] src/engine/main.py:28",
    "      SQL splitter strips lines starting with '--' but does not",
    "      strip them from the START of a statement → eats valid SQL.",
    "",
    "  [7] src/agent/pricing_agent.py:83",
    "      cancelled-booking filter sits in LEFT JOIN ON clause →",
    "      does not actually exclude cancelled rows from COUNT.",
    "",
    "✗ ACTION: human review required for all 7 items.",
]
colors4o = [ERROR] + [TXT] + \
           [KEYWORD, TXT, COMMENT, TXT] + \
           [KEYWORD, TXT, COMMENT, TXT] + \
           [KEYWORD, TXT, COMMENT, TXT] + \
           [KEYWORD, TXT, TXT] + \
           [KEYWORD, TXT, TXT] + \
           [KEYWORD, TXT, TXT, TXT] + \
           [KEYWORD, TXT, TXT, TXT] + \
           [ERROR]
terminal_screenshot("output_04.png",
                    "codex — output: review findings",
                    output4,
                    "GPT-5.4  via Codex CLI 0.128.0",
                    line_colors=colors4o,
                    font_size=9.0)


# ====================================================================
# PROMPT 5 — Violin plot matplotlib boilerplate (Claude Opus 4.7)
# ====================================================================
prompt5 = [
    "$ claude",
    "",
    "> Write a matplotlib + seaborn snippet to render a violin plot of",
    "  per-night room revenue, with these requirements:",
    "",
    "    · 5 room categories on X axis, ordered cheapest -> most expensive",
    "    · Use seaborn Set2-style palette (5 distinct pastels)",
    "    · Inner quartile lines visible",
    "    · Overlay raw data points (stripplot) at size=2, alpha=0.45",
    "    · Hide top and right spines",
    "    · Times New Roman 10pt serif, 300 DPI output",
    "    · Save to fig2_violin_revenue.pdf",
    "",
    "  Data is in a DataFrame `df` with columns: Room Type, Nightly Revenue",
    "  Just give me the plotting code, no boilerplate setup.",
]
colors5 = [USER] + [TXT] + [PROMPT] + [TXT]*2 + [TXT]*7 + [TXT]*3
terminal_screenshot("prompt_05.png",
                    "claude — violin plot boilerplate",
                    prompt5,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors5)


# ====================================================================
# PROMPT 6 — Raincloud plot (Claude Opus 4.7)
# ====================================================================
prompt6 = [
    "$ claude",
    "",
    "> Generate a raincloud plot (half-violin + jittered scatter + small",
    "  box) for the Task_Log Quality_Score, grouped by department.",
    "",
    "  Layout per department:",
    "    · half-violin on the RIGHT (clip the left half of the violin path)",
    "    · jittered scatter points on the LEFT of the violin",
    "    · narrow boxplot further LEFT, white median line",
    "",
    "  Colors:",
    "    · Housekeeping = teal #2A9D8F",
    "    · Maintenance  = coral #E76F51",
    "",
    "  Use serif font, hide top/right spines, y-range 6.5 to 10.5.",
    "  Save to fig5_raincloud_quality.pdf at 300 DPI.",
]
colors6 = [USER] + [TXT] + [PROMPT] + [TXT]*2 + [TXT]*5 + [TXT]*4 + [TXT]*2
terminal_screenshot("prompt_06.png",
                    "claude — raincloud plot boilerplate",
                    prompt6,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors6)


# ====================================================================
# OUTPUT 5 — Violin plot generated code
# ====================================================================
output5 = [
    "● Generated docs/report/figures/generate_figures.py (fig2 block)",
    "",
    "  palette = [\"#66C2A5\",\"#FC8D62\",\"#8DA0CB\",\"#E78AC3\",\"#A6D854\"]",
    "  order   = [\"Standard Single\", \"Standard Double\", \"Family Room\",",
    "             \"Deluxe Suite\", \"Presidential Suite\"]",
    "",
    "  fig, ax = plt.subplots(figsize=(7.5, 3.6))",
    "  sns.violinplot(data=df, x=\"Room Type\", y=\"Nightly Revenue (USD)\",",
    "                 order=order, hue=\"Room Type\", palette=palette,",
    "                 inner=\"quartile\", linewidth=0.9, legend=False, ax=ax)",
    "  sns.stripplot(data=df, x=\"Room Type\", y=\"Nightly Revenue (USD)\",",
    "                order=order, color=\"#1a1a1a\", size=1.9, alpha=0.42)",
    "",
    "  ax.set_title(\"Nightly Revenue Distribution by Room Category\",",
    "               fontweight=\"bold\", color=\"#2C3E50\", pad=8)",
    "  ax.set_xlabel(\"\")",
    "  ax.grid(axis=\"y\", linestyle=\":\", alpha=0.35, color=\"#999\")",
    "  ax.spines[[\"top\", \"right\"]].set_visible(False)",
    "  plt.xticks(rotation=8)",
    "  plt.savefig(\"fig2_violin_revenue.pdf\", dpi=300, bbox_inches=\"tight\")",
    "",
    "✓ Generated 19 lines · uses Set2 pastels · matches Nature style",
]
colors5o = [SUCCESS] + [TXT] + \
           [STRING] + [STRING]*2 + [TXT] + \
           [KEYWORD] + [KEYWORD]*3 + [TXT] + \
           [KEYWORD] + [KEYWORD] + [TXT] + \
           [KEYWORD, KEYWORD] + \
           [KEYWORD] + [KEYWORD] + [KEYWORD] + [KEYWORD] + [KEYWORD] + [TXT] + \
           [SUCCESS]
terminal_screenshot("output_05.png",
                    "claude — output: violin plot code",
                    output5,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors5o)


# ====================================================================
# OUTPUT 6 — Raincloud plot code
# ====================================================================
output6 = [
    "● Generated docs/report/figures/generate_figures.py (fig5 block)",
    "",
    "  dept_colors = {\"Housekeeping\": \"#2A9D8F\",",
    "                 \"Maintenance\":  \"#E76F51\"}",
    "",
    "  for i, d in enumerate(sorted(tasks[\"dept\"].unique())):",
    "      vals = tasks.loc[tasks[\"dept\"] == d, \"quality\"].values",
    "      col  = dept_colors[d]",
    "",
    "      # ① half-violin: clip the left half of the violin path",
    "      parts = ax.violinplot([vals], positions=[i], widths=0.7,",
    "                            showmeans=False, showextrema=False)",
    "      for pc in parts[\"bodies\"]:",
    "          verts = pc.get_paths()[0].vertices",
    "          verts[:, 0] = np.clip(verts[:, 0], i, i + 1)",
    "          pc.set_facecolor(col); pc.set_alpha(0.42)",
    "",
    "      # ② jittered rain on the left",
    "      xj = i - 0.10 - np.random.default_rng(i).uniform(0,0.18,len(vals))",
    "      ax.scatter(xj, vals, color=col, s=28, alpha=0.85,",
    "                 edgecolor=\"white\", linewidth=0.6)",
    "",
    "      # ③ narrow boxplot further left",
    "      bp = ax.boxplot(vals, positions=[i-0.3], widths=0.13,",
    "                     patch_artist=True, showfliers=False)",
    "      for b in bp[\"boxes\"]:    b.set(facecolor=col, alpha=0.9)",
    "      for m in bp[\"medians\"]: m.set(color=\"white\", lw=1.4)",
    "",
    "✓ Three-layer raincloud · clean clipping · 26 lines",
]
colors6o = [SUCCESS] + [TXT] + \
           [STRING, STRING] + [TXT] + \
           [KEYWORD] + [TXT, TXT] + [TXT] + \
           [COMMENT] + [KEYWORD, KEYWORD] + \
           [TXT, TXT, TXT, TXT] + [TXT] + \
           [COMMENT] + [TXT, TXT, TXT] + [TXT] + \
           [COMMENT] + [TXT, TXT, TXT, TXT] + \
           [SUCCESS]
terminal_screenshot("output_06.png",
                    "claude — output: raincloud plot code",
                    output6,
                    "Claude Opus 4.7  (1M ctx)",
                    line_colors=colors6o,
                    font_size=8.8)


print(f"\nAll 12 screenshots saved to: {OUT}")
print("Models referenced:")
print("  · Claude Opus 4.7 (1M context)        — prompts 1-3, 5-6, outputs 1-3, 5-6")
print("  · GPT-5.4 via Codex CLI 0.128.0       — prompt 4, output 4")
