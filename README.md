# EBU5503 酒店预订管理系统 — 组员导览

> 7 人小组课程作业 · 场景 2 · 截止 2026-05-23 · QMplus 提交
>
> 本文件是给**全体组员**的项目地图。每位成员看完本文都应能在 5 分钟内
> 找到任何文件、说出它的作用、并能在答辩中讲清自己负责的那块。

---

## 1. 项目结构总览

```
数据库大作业/
│
├─ README.md                    ← 本文档（项目导览）
├─ CLAUDE.md                    ← 项目目标与课程要求摘要
├─ GEMINI.md                    ← 项目任务书
├─ 数据库作业指导文档.pdf       ← 老师发的原版作业说明
├─ 初版草案.jpg                 ← 我们最初的手绘 ER 图
│
├─ src/                         ← 【核心代码】
│  ├─ schema/
│  │  ├─ init.sql               ← 建表脚本（11 张表 + 约束 + 索引）
│  │  └─ sample_data.sql        ← 样本数据（125 行 INSERT）
│  ├─ agent/
│  │  └─ pricing_agent.py       ← 动态定价 Agent（创新点）
│  └─ engine/
│     └─ main.py                ← 数据库引擎：建表→填数据→跑查询
│
├─ tests/
│  └─ test_queries.sql          ← 12 条 SQL 查询（涉及全部 11 表）
│
├─ result/
│  └─ query_outputs/            ← 【MySQL 实跑结果】
│     ├─ png/Q01.png ~ Q12.png  ← 每条查询的论文风格表格截图
│     ├─ text/Q01.txt ~ Q12.txt ← 原始 tab-分隔结果
│     ├─ results_summary.md     ← 12 条查询汇总报告
│     └─ run_queries.py         ← 跑查询并生成图的脚本
│
├─ docs/
│  ├─ report/                   ← 【提交物 1：报告】
│  │  ├─ EBU5503_Hotel_DB_Report.pdf  ★ 最终提交的 7 页报告 PDF
│  │  ├─ EER_PROMPT.md          ← EER 图生成 prompt 集
│  │  ├─ report_outline.md      ← 报告大纲（中文）
│  │  ├─ figures/               ← 6 张论文级图表
│  │  │  ├─ fig1_eer_overview.png    ← EER 图（Workbench 导出）
│  │  │  ├─ fig2_violin_revenue.pdf  ← 小提琴图：房型收入分布
│  │  │  ├─ fig3_sankey_flow.pdf     ← 桑葚图：会员→预订状态
│  │  │  ├─ fig4_heatmap_corr.pdf    ← 相关性热力图
│  │  │  ├─ fig5_raincloud_quality.pdf ← 云雨图：任务质量
│  │  │  ├─ fig6_lollipop_pricing.pdf  ← 棒棒糖图：定价规则
│  │  │  ├─ fig7_agent_flow.pdf      ← Agent 决策流程图
│  │  │  ├─ generate_figures.py      ← 图表生成脚本
│  │  │  └─ compute_query_results.py ← 查询结果计算脚本
│  │  └─ latex/                 ← LaTeX 源码
│  │     └─ report.tex
│  │
│  ├─ presentation/             ← 【提交物 2：演示 PPT】
│  │  └─ slides_outline.md      ← 演示大纲（10 页结构 — 待制作 PDF）
│  │
│  └─ genai_appendix/           ← 【提交物 3：GenAI 附录】
│     ├─ genai_log.md           ← GenAI 使用说明（工具+用途+流程）
│     ├─ prompt_01~06.png       ← 6 张 prompt 终端截图
│     ├─ output_01~06.png       ← 6 张 output 终端截图
│     └─ generate_screenshots.py← 截图生成脚本
│
└─ agent/
   └─ agent_technology.md       ← Agent 技术调研（学术背景 + 论文引用）
```

---

## 2. 数据流（这套东西是怎么串起来的）

```
┌─────────────────────┐     mysql < init.sql      ┌───────────────────────┐
│  src/schema/        │ ────────────────────────► │  MySQL: hotel_         │
│  init.sql           │                            │  management           │
│  sample_data.sql    │     mysql < sample.sql     │  (11 tables, 125 rows)│
└─────────────────────┘ ────────────────────────► └────────┬──────────────┘
                                                            │
                                                            │ run_queries.py
                                                            ▼
┌─────────────────────┐                            ┌───────────────────────┐
│  tests/             │                            │  result/query_outputs/│
│  test_queries.sql   │ ────────────────────────► │  png/  text/  md/     │
│  (12 queries)       │                            │  (实跑结果)            │
└─────────────────────┘                            └────────┬──────────────┘
                                                            │
                                                            ▼
┌─────────────────────┐                            ┌───────────────────────┐
│  docs/report/       │ ◄────────── insert ─────── │  6 figures + result   │
│  figures/*.pdf      │                            │  tables               │
└──────────┬──────────┘                            └───────────────────────┘
           │
           │ \input{}
           ▼
┌─────────────────────┐
│  docs/report/latex/ │   xelatex report.tex
│  report.tex         │ ────────────────────────► EBU5503_Hotel_DB_Report.pdf
└─────────────────────┘                            (7 页最终报告)

并行的创新点：
  src/agent/pricing_agent.py
      └─ queries → MySQL → 计算 P_base × m_rule × f_occ → 输出建议价
```

---

## 3. 三件提交物对应关系

| 提交物 | 文件 | 状态 | 谁负责 |
|--------|------|------|--------|
| **报告 PDF** | `docs/report/EBU5503_Hotel_DB_Report.pdf`（7 页） | ✅ 完成 | 全员审稿 |
| **演示 PDF** | 基于 `docs/presentation/slides_outline.md` 制作（≤10 页） | ⚠️ 待做 | 待分工 |
| **GenAI 附录** | `docs/genai_appendix/`（markdown + 12 张截图） | ✅ 完成 | 全员审稿 |

---

## 4. 数据库的 11 张表（每个人都要能背）

按四大功能域分组：

| 域 | 表 | 关键作用 |
|----|-----|---------|
| **客户域** | `Guest` | 客人基本信息（姓名、邮箱、护照号唯一） |
| | `Loyalty_Program` | 忠诚度计划（与 Guest 1:1） |
| **库存域** | `Room_Type` | 房型（标间、套房等，含基准价） |
| | `Room` | 物理房间（关联 Room_Type） |
| **交易域** | `Booking` | 预订主表（关联 Guest） |
| | `Booking_Room_Detail` | **关联实体**！解决 Booking↔Room 的 M:N |
| | `Payment` | 支付记录（关联 Booking） |
| | `Dynamic_Pricing_Rule` | **全局规则实体**，无 FK，由应用层查询 |
| **运营域** | `Department` | 部门 |
| | `Staff` | 员工（关联 Department） |
| | `Task_Log` | **三元关系**：Staff × Room × Task_Type |

---

## 5. 12 条 SQL 查询索引

| 查询 | 涉及表 | 技术亮点 |
|------|--------|---------|
| Q1  | Guest, Booking, Payment | 多表 JOIN + 聚合 |
| Q2  | Room_Type, Room, Booking_Room_Detail, Booking | LEFT JOIN + 子查询（剔除取消） |
| Q3  | Dynamic_Pricing_Rule, Room_Type, Room, Booking_Room_Detail | 日期区间匹配 + CASE WHEN |
| Q4  | Loyalty_Program, Guest, Booking, Payment | **窗口函数 RANK()** |
| Q5  | Room, Booking_Room_Detail, Room_Type, Booking | **NOT EXISTS + 日期重叠** |
| Q6  | Department, Staff, Task_Log | GROUP BY + HAVING |
| Q7  | Payment, Booking | DATE_FORMAT + **LAG()** (MoM 变化) |
| Q8  | Staff, Task_Log, Room | **窗口函数 ROW_NUMBER()** |
| Q9  | Guest, Booking, Booking_Room_Detail, Room, Room_Type, Payment | **CREATE VIEW**（6 表） |
| Q10 | Booking | CASE WHEN 分级告警 |
| Q11 | Guest, Booking, Payment, Loyalty_Program | **CTE (WITH)** + VIP 评分 |
| Q12 | Booking_Room_Detail, Booking, Room | **自连接**（超售检测，返回 0 行 = 正确） |

**关键事实**：12 条查询**覆盖了全部 11 张表**（老师评分硬要求）。

---

## 6. 给组员的"答辩讲解分工建议"

每人至少负责 1-2 个模块，但**所有人都要懂整体设计**（答辩 35 分占比最高）。

| 模块 | 该看哪些文件 | 答辩必答问题 |
|------|------------|-------------|
| **A. 需求与设计** | `report.tex` §1-2 + `agent/agent_technology.md` | 为什么选场景 2？附加需求怎么定的？|
| **B. EER 图与关系** | `fig1_eer_overview.png` + `report.tex` §2 | 关联实体 vs 三元关系的区别？ |
| **C. 规范化推导** | `report.tex` §3 | 1NF/2NF/3NF/BCNF 各是怎么验证的？ |
| **D. 建表 SQL** | `src/schema/init.sql` | 为什么这么命名 FK？CHECK 约束防什么？ |
| **E. 样本数据** | `src/schema/sample_data.sql` | 覆盖了哪些边界？为什么 Payment 有时不等于夜数×房价？ |
| **F. SQL 查询** | `tests/test_queries.sql` + `result/query_outputs/` | Q5 为什么 NOT EXISTS？Q11 VIP 公式怎么定的？|
| **G. 动态定价 Agent** | `src/agent/pricing_agent.py` + `fig7_agent_flow.pdf` | 为什么是数据库驱动？规则改了要重启吗？|

---

## 7. 怎么本地跑起来（开发环境）

### MySQL 端
```bash
# 1. 建表
mysql -uroot -p < src/schema/init.sql
# 2. 灌数据
mysql -uroot -p hotel_management < src/schema/sample_data.sql
# 3. 跑查询
mysql -uroot -p hotel_management < tests/test_queries.sql
```

### Python 端（生成结果截图）
```bash
cd result/query_outputs && python3 run_queries.py
```

### LaTeX 端（重编译报告）
```bash
cd docs/report/latex && xelatex report.tex
```

---

## 8. 答辩前 24 小时检查清单

- [ ] 每个组员能在白板上画出 EER 简图（11 个实体 + 9 条关系）
- [ ] 每个组员能解释自己负责模块中的至少 2 条查询
- [ ] 全员熟悉创新点：动态定价 Agent 的三层结构（规则 × 入住率 × 基准价）
- [ ] 全员熟悉关键设计决策：
  - 为什么 Booking_Room_Detail 而不是 Booking-Room 多对多直连？
  - 为什么 Dynamic_Pricing_Rule 没有外键？
  - Q12 为什么返回 0 行是好事？
  - 超售怎么防？（应用层 + Q5/Q12 的查询保护）
- [ ] 演示 PDF 已上传到 QMplus
- [ ] 报告 PDF 已上传到 QMplus
- [ ] GenAI 附录中的 12 张截图都附在最终报告里（或独立打包）

---

## 9. 联系方式与版本

- 提交截止：**2026-05-23 周六午夜（英国时间）**
- 演示时间：**2026-05-25 起**（5 分钟演示 + 15 分钟提问）
- 报告版本：v1.0（7 页正文 + GenAI 附录）
- 最近一次大改：嵌入真实 EER 图、12 张 GenAI 截图、12 条 SQL 实跑结果
