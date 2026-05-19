# GenAI Usage Appendix — EBU5503 Hotel Booking & Management System

> This appendix discloses every use of generative AI in producing the
> coursework submission, in compliance with the EBU5503 GenAI policy.
> The appendix does **not** count toward the 10-page report limit.

---

## 1. Scope and Philosophy of AI Use

All conceptual decisions — the choice of Scenario 2, the eleven-entity
schema, the normalisation reasoning, the dynamic-pricing innovation, the
12-query strategy, and the report's narrative — were authored by the seven
group members.

**We restricted GenAI to two narrow categories of work:**

1. **Small, repetitive, mechanical coding** — the kind of boilerplate that
   would otherwise be copy-paste-and-modify drudgery (`CREATE TABLE`
   statements, `INSERT` rows, fence-post date formatting, `matplotlib`
   plotting boilerplate). The intellectual content of these artefacts
   came from the human design; the AI saved typing time only.

2. **Language polishing and Chinese→English translation** — converting
   the group's Chinese-language design notes and brainstorm bullets into
   academic English for the final report.

We did **not** use AI to invent the design, write analytical reasoning,
generate the EER diagram, or draft answers we will give at the
defence — those are human authorship.

---

## 2. Tools Used

| Tool | Vendor | Model / Version | Where used |
|------|--------|-----------------|------------|
| Claude Code (CLI) | Anthropic | Opus 4.7 (1M context) | Boilerplate generation, translation |
| Codex CLI (consult mode) | OpenAI | codex-cli 0.128.0 | Independent SQL & Python code review |

No image-generation, voice or web-search AI tools were used.

---

## 3. Concrete Tasks Delegated to AI

### 3.1 Repetitive boilerplate code (saves typing, no design)

| Artefact | What AI produced | Human input |
|----------|------------------|-------------|
| `src/schema/init.sql` — `CREATE TABLE` for 11 tables | Standard MySQL DDL syntax: `ENGINE=InnoDB`, `utf8mb4`, `FOREIGN KEY ... REFERENCES`, `ENUM('...','...')` declarations. | We provided the relation list, attribute types, key/UNIQUE/CHECK constraints, FK naming convention. |
| `src/schema/sample_data.sql` — ~125 `INSERT` rows | The mechanical row-by-row INSERT typing once we specified the values. | We designed the edge-case matrix (repeat guests, cancellations, multi-room bookings, partial deposits, NULL completion). |
| `result/query_outputs/run_queries.py` — table-to-PNG helper | Matplotlib `ax.table(...)` boilerplate, zebra-striping, auto column-width calculation. | We chose the visual style (header colour, font, layout) and decided to render each query result as a PNG. |
| `docs/report/figures/generate_figures.py` — chart scaffolding (violin plot, Sankey, correlation heatmap, raincloud plot, lollipop chart, agent-flow diagram) | Routine matplotlib/seaborn calls: `sns.violinplot(...)` with `palette`+`order`, half-violin path clipping for raincloud, ribbon easing for Sankey, `sns.heatmap(...)` with custom colour-map, `ax.boxplot(patch_artist=True)` styling. | We selected the chart type for each visual question, picked palettes (Set2 pastels, RdBu_r for heatmap, teal/coral for raincloud), wrote titles and captions, and verified that figures actually render the underlying data correctly. |

### 3.2 Translation: Chinese → academic English

The team brainstormed in Chinese; the AI translated the resulting notes
into the academic-English phrasing used in the final report and slides.

| Source (Chinese, in group notes) | Translated output (used in report) |
|----------------------------------|------------------------------------|
| "酒店动态定价：依据节假日、周末、入住率调整价格" | "Event- and season-based rate adjustment (Christmas, Spring Festival, Summer, weekdays) enables a *revenue-management* layer on top of static base prices." |
| "客人忠诚度计划，分四级会员" | "Returning guests are rewarded with tiered benefits (Bronze/Silver/Gold/Platinum) — a retention engine standard across Marriott Bonvoy and Hilton Honors." |
| "Booking 和 Room 是多对多关系，所以拆出 Booking_Room_Detail" | "Booking ↔ Room is an M:N relationship, decomposed by the *associative entity* Booking_Room_Detail." |
| "用 NOT EXISTS 加日期重叠条件来查可用房间，比看 Current_Status 更稳" | "By using NOT EXISTS with a date-overlap predicate rather than relying on Room.Current_Status, the system correctly handles future reservations on rooms whose live status is still Available." |

### 3.3 Independent code review (a sanity-checking second opinion)

We ran Codex CLI as an adversarial reviewer against
`tests/test_queries.sql`, `src/schema/init.sql`, and
`src/agent/pricing_agent.py`. It surfaced **7 mechanical bugs** we then
fixed manually (see Section 5).

---

## 4. Representative Prompts

The four most consequential prompts are reproduced verbatim below.
Submission note: matching terminal screenshots
(`prompt_01.png` … `prompt_04.png`) will be added to this folder before
final upload. The verbatim text below is provided so the appendix is
self-contained.

### Prompt 1 — `CREATE TABLE` boilerplate
> *"Given the following 11 relations and their attribute lists, generate
> a MySQL 8.0 `init.sql` script. Use `ENGINE=InnoDB`, `utf8mb4`, name
> foreign keys `fk_<table>_<reference>`, add a `CHECK` on
> `CheckOut_Date > CheckIn_Date`, and on `Price_Multiplier > 0`. Do not
> add any tables I did not list."*

### Prompt 2 — Sample-data row typing
> *"Produce `INSERT INTO ...` rows that satisfy the following edge-case
> matrix: 2 repeat guests, 3 multi-room bookings, 2 cancellations with
> refund, 1 partial-payment booking, 1 task entry with NULL completion.
> Keep totals consistent with `nights × Final_Agreed_Rate`."*

### Prompt 3 — Chinese-to-English translation
> *"Translate the following Chinese design notes into formal academic
> English suitable for an EBU5503 database-systems report. Keep
> technical terms unchanged (e.g. `Booking_Room_Detail`, `1NF`,
> `NOT EXISTS`). Preserve meaning; do not embellish."*

### Prompt 4 — Codex independent review
> *"Audit `tests/test_queries.sql`, `src/schema/init.sql`, and
> `pricing_agent.py` against EBU5503 requirements. Find ENUM
> mismatches, missing CHECK constraints, and logic bugs in queries.
> Output one finding per bullet."*

### Prompt 5 — Violin-plot boilerplate (figures)
> *"Write a matplotlib + seaborn snippet to render a violin plot of
> per-night room revenue. Requirements: 5 room categories on X axis
> ordered cheapest → most expensive; seaborn Set2-style palette
> (5 distinct pastels); inner quartile lines visible; overlay raw
> data points (`stripplot`) at size=2, alpha=0.45; hide top/right
> spines; Times New Roman 10pt serif; 300 DPI output to
> `fig2_violin_revenue.pdf`."*

### Prompt 6 — Raincloud-plot boilerplate (figures)
> *"Generate a raincloud plot (half-violin + jittered scatter + small
> box) for `Task_Log.Quality_Score`, grouped by department. Per
> department: half-violin on the right (clip the left half of the
> violin path), jittered scatter points on the left, narrow boxplot
> further left with white median line. Colors: Housekeeping `#2A9D8F`
> (teal), Maintenance `#E76F51` (coral). Y-range 6.5 → 10.5; save to
> `fig5_raincloud_quality.pdf`."*

---

## 5. Representative Outputs

Corresponding code snippets are reproduced inline below; matching
terminal screenshots (`output_01.png` … `output_04.png`) will be
attached at submission time.

### Output 1 — `CREATE TABLE` (excerpt of generated boilerplate)
```sql
CREATE TABLE Booking (
    Booking_ID     INT AUTO_INCREMENT,
    Guest_ID       INT NOT NULL,
    Creation_Time  DATETIME NOT NULL DEFAULT NOW(),
    Total_Guests   INT NOT NULL DEFAULT 1,
    Overall_Status ENUM('Confirmed','Checked-In','Checked-Out','Cancelled')
                   NOT NULL DEFAULT 'Confirmed',
    PRIMARY KEY (Booking_ID),
    CONSTRAINT fk_booking_guest FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID),
    CONSTRAINT chk_booking_guests CHECK (Total_Guests > 0)
) ENGINE=InnoDB;
```

### Output 2 — `INSERT` rows (excerpt of generated boilerplate)
```sql
-- Booking 6 reserves two rooms simultaneously for a group of 4
INSERT INTO Booking_Room_Detail VALUES
  (6, 6, 103, '2026-02-10', '2026-02-13', 110.50),
  (7, 6, 201, '2026-02-10', '2026-02-13', 110.50);
```

### Output 3 — A typical translation pass
```
Chinese in:
  "通过 NOT EXISTS 和日期重叠条件查可用房间，
   这样比检查 Current_Status 字段更安全，
   因为它能正确处理那些 Current_Status 还是 Available 但已经被预订的房间。"

English out (used in §5 of the report):
  "By using NOT EXISTS with a date-overlap predicate rather than relying
   on Room.Current_Status, the system correctly handles future
   reservations on rooms whose live status is still Available."
```

### Output 4 — Codex review surfaced 7 bugs (paraphrased)
```
1. Q5  : Current_Status != 'Out_of_Service'  → enum has no such value;
         replace with 'Maintenance'.
2. Q10 : Overall_Status = 'Completed'        → enum is 'Checked-Out'.
3. Q11 : Tier_Level WHEN 'Diamond'           → enum is 'Platinum'.
4. init.sql : Booking.Total_Guests           → missing CHECK (>0).
5. init.sql : Payment.Amount                 → missing CHECK (>0).
6. main.py  : SQL splitter swallows lines    → starting with '--'.
7. pricing_agent.py : cancelled-booking      → filter in LEFT JOIN ON
                                                clause does not exclude.
```
All seven items were reviewed by a human author and fixed manually in the
codebase. The fix commits live in `tests/test_queries.sql` and
`src/schema/init.sql` (see Section 6 verification log).

### Output 5 — Violin-plot code (excerpt of generated boilerplate)
```python
palette = ["#66C2A5","#FC8D62","#8DA0CB","#E78AC3","#A6D854"]
order   = ["Standard Single","Standard Double","Family Room",
           "Deluxe Suite","Presidential Suite"]

fig, ax = plt.subplots(figsize=(7.5, 3.6))
sns.violinplot(data=df, x="Room Type", y="Nightly Revenue (USD)",
               order=order, hue="Room Type", palette=palette,
               inner="quartile", linewidth=0.9, legend=False, ax=ax)
sns.stripplot(data=df, x="Room Type", y="Nightly Revenue (USD)",
              order=order, color="#1a1a1a", size=1.9, alpha=0.42)

ax.spines[["top","right"]].set_visible(False)
plt.savefig("fig2_violin_revenue.pdf", dpi=300, bbox_inches="tight")
```

### Output 6 — Raincloud-plot code (excerpt)
```python
dept_colors = {"Housekeeping": "#2A9D8F", "Maintenance": "#E76F51"}

for i, d in enumerate(sorted(tasks["dept"].unique())):
    vals = tasks.loc[tasks["dept"] == d, "quality"].values
    col  = dept_colors[d]

    # ① half-violin: clip the left half of the violin path
    parts = ax.violinplot([vals], positions=[i], widths=0.7,
                          showmeans=False, showextrema=False)
    for pc in parts["bodies"]:
        verts = pc.get_paths()[0].vertices
        verts[:, 0] = np.clip(verts[:, 0], i, i + 1)
        pc.set_facecolor(col); pc.set_alpha(0.42)

    # ② jittered rain on the left
    xj = i - 0.10 - np.random.default_rng(i).uniform(0,0.18,len(vals))
    ax.scatter(xj, vals, color=col, s=28, alpha=0.85)

    # ③ narrow boxplot further left, white median
    bp = ax.boxplot(vals, positions=[i-0.3], widths=0.13,
                   patch_artist=True, showfliers=False)
```
In both figure-code cases the AI produced the syntactic skeleton; we
chose the chart type, palette, layout decisions, and validated visual
fidelity against the underlying data.

---

## 6. Human Verification

Every AI-produced artefact was:

1. **Read line-by-line** by at least one group member.
2. **Executed against MySQL 8.0** — `init.sql` plus `sample_data.sql`
   plus all 12 queries — to confirm runtime behaviour. The 12 query
   results are stored in `result/query_outputs/`.
3. **Modified** where the suggestion did not fit the design
   (e.g. Q5 enum correction `Out_of_Service` → `Maintenance`;
   Q11 tier `Diamond` → `Platinum`).
4. **Documented** in this appendix.

Final responsibility for correctness, design choices, and academic
integrity rests with the seven group members.
