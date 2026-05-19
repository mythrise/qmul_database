# EER 框架图生成 Prompt

## 用途
用于在 ChatGPT-4o / Claude / Gemini / draw.io AI / Excalidraw AI / Mermaid Chart
等支持图像或代码生成的 AI 工具中，生成 EBU5503 酒店数据库的 EER 图。

> **重要**：生成后请确保配色与正文图统一（navy `#2E5C8A`，ochre `#D08B40`，
> sage `#4A7C59`，mauve `#8B5A89`，slate `#5C6670`，背景 `#F0EBE3`）。

---

## Prompt 1 — 用于 AI 图像生成（DALL-E / Midjourney / Gemini Image）

```
Create a clean, publication-quality EER (Enhanced Entity-Relationship) diagram
for a Hotel Booking & Management System. Style: minimalist, academic-textbook,
flat design with thin black borders and a warm-paper background (#F0EBE3).

Use exactly this restrained color palette to fill entity boxes:
  • Customer domain (navy #2E5C8A):     Guest, Loyalty_Program
  • Inventory domain (mauve #8B5A89):   Room_Type, Room
  • Transactional domain (sage #4A7C59): Booking, Booking_Room_Detail, Payment
  • Pricing domain (ochre #D08B40):     Dynamic_Pricing_Rule
  • Operational domain (slate #5C6670): Department, Staff, Task_Log

Show all 11 entities as rounded rectangles. Each box contains:
  • Entity name in BOLD CAPS at the top
  • A horizontal separator
  • Attributes listed; primary keys in BOLD with a key icon or asterisk
  • Foreign keys in italic, prefixed with "FK:"

Required relationships (use Chen notation with cardinality labels 1, N, M):
  1. Guest 1—1 Loyalty_Program   (label "has", optional on Guest side)
  2. Guest 1—N Booking           (label "makes")
  3. Booking 1—N Booking_Room_Detail  (label "contains")
  4. Booking_Room_Detail N—1 Room (label "assigns to")
  5. Room N—1 Room_Type          (label "is a")
  6. Booking 1—N Payment         (label "settled by")
  7. Department 1—N Staff        (label "employs")
  8. Staff 1—N Task_Log          (label "performs")
  9. Task_Log N—1 Room           (label "on")

Special annotations:
  • Mark Booking_Room_Detail as an ASSOCIATIVE ENTITY (diamond on top edge or
    explicit text label "[associative entity]") because it resolves the
    M:N relationship between Booking and Room.
  • Mark Task_Log as realising the TERNARY relationship Staff × Room ×
    Task_Type — add a small text annotation "[ternary]" next to its box.
  • Dynamic_Pricing_Rule should be drawn ISOLATED at the bottom-right, with
    a dashed connector to Booking_Room_Detail labelled "consulted by
    application logic" (no foreign key).

Layout:
  • Left column (top to bottom): Guest, Loyalty_Program, Department, Staff
  • Middle column: Booking, Booking_Room_Detail, Payment
  • Right column: Room, Room_Type, Task_Log
  • Bottom-right: Dynamic_Pricing_Rule
  • Title at top: "Hotel Booking & Management System — EER Diagram"
  • A small footnote: "* primary key   |   FK: foreign key"

Final result: a single A4-landscape image, 300 DPI, no shadows, no gradients,
all text in a serif font (Times New Roman or similar).
```

---

## Prompt 2 — 用于 Mermaid 代码生成（ChatGPT / Claude）

```
Generate a Mermaid `erDiagram` block for the Hotel Booking & Management
System with 11 entities. Use the following exact attribute lists and
relationship cardinalities:

Entities (with primary key first, foreign keys marked FK):
  Guest          : Guest_ID (PK), First_Name, Last_Name, Email (UK), Phone,
                   Identity_Doc (UK), Personal_Prefs, Registration_Date
  Loyalty_Program: Loyalty_ID (PK), Guest_ID (FK,UK), Tier_Level,
                   Available_Points, Enrollment_Date
  Room_Type      : Type_ID (PK), Category_Name (UK), Base_Nightly_Rate,
                   Max_Capacity, Description
  Room           : Room_ID (PK), Type_ID (FK), Floor_Level, Current_Status
  Booking        : Booking_ID (PK), Guest_ID (FK), Creation_Time,
                   Total_Guests, Overall_Status, Special_Requests
  Booking_Room_Detail : Detail_ID (PK), Booking_ID (FK), Room_ID (FK),
                   CheckIn_Date, CheckOut_Date, Final_Agreed_Rate
  Payment        : Payment_ID (PK), Booking_ID (FK), Amount, Payment_Date,
                   Payment_Method, Status
  Dynamic_Pricing_Rule : Rule_ID (PK), Event_Name, Effective_Start,
                   Effective_End, Price_Multiplier, Priority, Is_Active
  Department     : Dept_ID (PK), Dept_Name (UK)
  Staff          : Staff_ID (PK), Dept_ID (FK), Full_Name, Job_Role,
                   Hire_Date, Phone
  Task_Log       : Log_ID (PK), Staff_ID (FK), Room_ID (FK), Task_Type,
                   Assigned_Time, Completion_Time, Duration_Minutes,
                   Quality_Score

Relationships (Mermaid notation):
  GUEST ||--o| LOYALTY_PROGRAM     : "has"
  GUEST ||--o{ BOOKING             : "makes"
  BOOKING ||--|{ BOOKING_ROOM_DETAIL : "contains"
  BOOKING_ROOM_DETAIL }o--|| ROOM  : "assigns"
  ROOM }o--|| ROOM_TYPE            : "is a"
  BOOKING ||--o{ PAYMENT           : "settled by"
  DEPARTMENT ||--o{ STAFF          : "employs"
  STAFF ||--o{ TASK_LOG            : "performs"
  TASK_LOG }o--|| ROOM             : "on"

Output the Mermaid block only; no commentary.
```

After Mermaid renders the diagram, export as PDF/PNG via
<https://mermaid.live> or `mmdc -i diagram.mmd -o eer.pdf`.

---

## Prompt 3 — 用于 MySQL Workbench EER Reverse-Engineering

1. 打开 MySQL Workbench → `Database` → `Reverse Engineer...`
2. 选择已建好的 `hotel_management` schema
3. 全选 11 张表 → Execute
4. Workbench 自动生成 EER 图
5. 手动调整布局：
   - 三列布局：左 = 客户域，中 = 交易域，右 = 库存与运营
   - Booking_Room_Detail 放在 Booking 和 Room 之间，加文字标签 "associative entity"
   - Task_Log 旁加 "ternary relationship: Staff × Room × Task_Type"
6. `File` → `Export` → `Export as PDF/PNG`
7. 在 Workbench 偏好设置中将 Diagram 颜色改为本报告统一色卡

---

## Prompt 4 — 用于 Excalidraw AI / draw.io AI

```
Create an EER diagram with 11 entity boxes for a Hotel Booking & Management
System. Use 3-column layout. Color-code by domain:
  • Customer (navy): Guest, Loyalty_Program
  • Transactional (sage): Booking, Booking_Room_Detail, Payment
  • Inventory (mauve): Room, Room_Type
  • Pricing (ochre, isolated bottom-right): Dynamic_Pricing_Rule
  • Operational (slate, bottom-left): Department, Staff, Task_Log

Draw connection lines with cardinality labels in the form "1 : N" or "M : N".
Mark Booking_Room_Detail with a small diamond at its top-left corner to
indicate it is an associative entity that resolves the Booking↔Room M:N
relationship. Annotate Task_Log with "[ternary: Staff × Room × Task_Type]".

Hand-drawn / sketchy stroke style, warm-paper background (#F0EBE3).
```

---

## 最终验收清单

生成 EER 图后，请确认以下 8 点：

- [ ] 11 个实体全部出现且名字正确
- [ ] 每个实体显示了主键（带下划线或星号）
- [ ] 外键明确标注（italic 或 "FK:" 前缀）
- [ ] 所有 9 条关系都有线 + 基数标签（1:1 / 1:N / M:N）
- [ ] `Booking_Room_Detail` 明确标注为关联实体
- [ ] `Task_Log` 明确标注为三元关系实现
- [ ] `Dynamic_Pricing_Rule` 没有 FK 实线，用虚线或文字说明独立
- [ ] 配色与正文统一（5 色系，navy / ochre / sage / mauve / slate）

生成完成后，将 EER 图导出为 `fig1_eer_overview.pdf` 放入
`docs/report/figures/` 目录，然后在 `report.tex` 中把第 91 行的 `\fbox{...}`
占位框替换为：

```latex
\includegraphics[width=0.92\linewidth]{fig1_eer_overview.pdf}
```

再用 `xelatex report.tex` 重新编译即可。
