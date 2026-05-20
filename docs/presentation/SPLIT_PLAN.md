# 6 人分工方案 — PPT 制作 + 答辩准备

> EBU5503 Group 13 · Hotel Booking & Management System
>
> **演示时长**：5 分钟（每人 ≈ 50 秒讲解 + 1-2 页 PPT）
> **答辩时长**：15 分钟（多人协同回答，**每人都要懂全局**）
> **PPT 页数**：≤10 页（含封面与结尾）
> **PPT 风格**：与报告统一 — Nature 浅色多彩、纯白背景、Times New Roman 字体

---

## 整体页面布局（共 10 页）

| 页 | 内容 | 负责块 | 时间 |
|----|------|--------|------|
| 1 | 封面：标题、Group 13、6 人名单 | 公共（主讲人开场） | 20 s |
| 2 | **Block 1**：需求与假设 | Member A | 45 s |
| 3 | **Block 2**：EER 图 | Member B | 50 s |
| 4 | **Block 3**：关系模式 + 规范化 | Member C | 45 s |
| 5 | **Block 4**：样本数据 + 边界情况 | Member D | 40 s |
| 6 | **Block 5a**：SQL 查询代码与索引 | Member E | 30 s |
| 7 | **Block 5b**：SQL 实跑结果与图表 | Member E | 35 s |
| 8 | **Block 6a**：创新点 — Pricing Agent 公式与原理 | Member F | 30 s |
| 9 | **Block 6b**：Agent 决策流程 + 数据驱动论证 | Member F | 35 s |
| 10 | 总结 + Q&A 引导 | 公共（主讲人收尾） | 20 s |

**总时长**：~5 分钟（300 s）。Block 5 和 Block 6 各占 2 页（内容较密）。

---

## Block 1 — 需求与假设（Member A）

### PPT 内容（Page 2，约 45 秒）

**幻灯片标题**：Requirements & Assumptions

**3 个区块横向排列**：

1. **Basic Scenario 2**（左列，浅蓝底）
   - Guests · Rooms · Bookings · Payments
   - 4 个核心实体图标 + 一句话定义

2. **Additional Extensions**（中列，5 个 bullet）
   - Loyalty Program → Marriott Bonvoy 类比
   - Dynamic Pricing Rule → 收益管理 (Revenue Mgmt)
   - Room Type abstraction → 2NF 必需
   - Department + Staff → PMS 标配
   - Task Log → 三元关系 KPI

3. **Key Assumptions**（右列）
   - 1 booking → N rooms
   - Payment 含押金/退款
   - Loyalty 可选 1:1
   - 超售由应用层 + Q12 防护

**用到的素材**：报告 §1（已写好的表格可直接截图）

### 讲解要点（45 秒）
> "We start from the four mandated entities of Scenario 2 — guests, rooms, bookings, and payments. Then we extend the design in five realistic directions, each grounded in real hotel-industry practice: loyalty programs as in Marriott Bonvoy, dynamic pricing for revenue management, room-type abstraction for 2NF, departmental organisation, and task-level KPI tracking. Our assumptions explicitly allow multi-room bookings, partial payments including refunds, and concurrent-overlap prevention through both schema constraints and a self-join audit query."

### 答辩 Q&A 预案（Member A 必须能答）

| Q | 一句话答案 |
|---|----------|
| 为什么选场景 2 而不是场景 1/3？ | 酒店 PMS 有真实的多维度业务（房型、季节、忠诚度），数据建模更有挑战 |
| 你们的 5 个附加扩展为什么"切合实际"而非凭空想象？ | 每个都对应真实酒店行业的功能（Marriott Bonvoy、Revenue Management、PMS 标准） |
| Loyalty Program 为什么独立成表而不是给 Guest 加字段？ | 1:1 可选关系；不是所有客人都注册会员；分离避免 NULL 字段 |
| Dynamic Pricing 不放进 Booking 表里？ | 规则可独立演进，不依赖具体预订；Pricing Agent 实时查询 |
| 假设里"超售由应用层防护"够不够？为什么不用数据库约束？ | SQL 标准不支持范围非重叠 CHECK；用 Q12 自连接审计 + 事务锁 |

---

## Block 2 — EER 图（Member B）

### PPT 内容（Page 3，约 50 秒）

**幻灯片标题**：Conceptual Schema (EER Design)

**布局**：全屏一张 EER 图 + 右下角小文字框

- **主图**：MySQL Workbench 导出的 EER（`fig1_eer_overview.png`）占 80% 屏幕
- **关键标注**（图上箭头指向）：
  - "Associative entity ★" 指向 Booking_Room_Detail
  - "Ternary relationship ★" 指向 Task_Log
  - "Global rule entity (no FK) ★" 指向 Dynamic_Pricing_Rule
- **右下角小文字**：4 functional domains: Customer / Inventory / Transactional / Operational

### 讲解要点（50 秒）
> "Our schema has 11 entities grouped into 4 functional domains. The most important design decisions: **Booking_Room_Detail** is the associative entity that resolves the M:N between Booking and Room, carrying per-room dates and the agreed rate. **Task_Log** realises a true ternary relationship over Staff × Room × Task_Type. **Dynamic_Pricing_Rule** is deliberately a global entity without any foreign key — this decoupling lets pricing strategies evolve at the data layer without touching the inventory schema. **Loyalty_Program** is optional 1:1 with Guest. Everything else is straightforward 1:N."

### 答辩 Q&A 预案（Member B 必须能答）

| Q | 一句话答案 |
|---|----------|
| 什么是关联实体？为什么需要它？ | 解决 M:N 关系；本身有自己的属性（如 CheckIn_Date、Final_Agreed_Rate） |
| Task_Log 怎么算"三元"而不是"二元加属性"？ | Task_Type 是分类维度而非简单属性，决定任务的语义 |
| 为什么 Dynamic_Pricing_Rule 没有 FK 连到房型？ | 全局规则，所有房型都查；FK 会变成强耦合，规则无法独立增删 |
| Guest 和 Loyalty 为什么不合并？ | 不是所有客人都注册；强制合并会有大量 NULL 字段 |
| 11 个实体会不会过度设计？ | 每个都对应真实操作需求，且都参与 SQL 查询（12 条覆盖 11 表） |

---

## Block 3 — 关系模式与规范化（Member C）

### PPT 内容（Page 4，约 45 秒）

**幻灯片标题**：Schema & Normalisation to BCNF

**上半部分**：关系模式一览表（缩小版，只展示 PK / FK，不写 attribute 全名）
```
Guest(Guest_ID*)        Booking(Booking_ID*, Guest_ID→)
Loyalty(Loyalty_ID*, Guest_ID→)        BRD(Detail_ID*, Booking_ID→, Room_ID→)
Room_Type(Type_ID*)     Payment(Payment_ID*, Booking_ID→)
Room(Room_ID*, Type_ID→)        Pricing_Rule(Rule_ID*)
Department(Dept_ID*)    Staff(Staff_ID*, Dept_ID→)
Task_Log(Log_ID*, Staff_ID→, Room_ID→)
```

**下半部分**：规范化 4 步进化箭头图
```
Draft LOG表 ──1NF──► 拆为 Booking+BRD+Payment （消除嵌套）
                ──2NF──► 抽出 Room_Type（消除部分依赖）
                ──3NF──► Payment 不存 guest_name（消除传递依赖）
                ──BCNF─► 所有 FD 左侧都是超键 ✓
```

### 讲解要点（45 秒）
> "The conceptual model translates into 11 relations. Three normalisation moves matter most: **1NF** required splitting the draft's monolithic LOG table that mixed booking, room assignment, and payment into nested groups. **2NF** required factoring out Room_Type because price functionally depended on type, not on the physical room. **3NF** ensures Payment only stores Booking_ID — guest details are reached via JOIN. **BCNF** is also satisfied: every non-trivial functional dependency has a superkey on its left."

### 答辩 Q&A 预案（Member C 必须能答）

| Q | 一句话答案 |
|---|----------|
| 怎么验证 BCNF？ | 检查每个 FD 左侧是否包含候选键；本设计所有 FD 左侧都是 PK |
| 1NF 的违反具体在哪里？ | 草案的 LOG 表对每个预订/房间/支付组合都重复一行，是嵌套重复组 |
| 为什么要单独抽出 Room_Type？ | 价格依赖房型而非具体房间号 → 部分依赖 → 违反 2NF |
| 3NF 与 BCNF 的区别？ | BCNF 更严：3NF 允许"prime attribute depends on partial key"，BCNF 不允许 |
| 有没有反规范化的地方？ | 没有；Booking.Total_Guests 是冗余但属于汇总属性，不算反规范化 |

---

## Block 4 — 样本数据 + 边界情况（Member D）

### PPT 内容（Page 5，约 40 秒）

**幻灯片标题**：Sample Data & Edge Cases

**左列**：数据规模表
| Table | Rows |
|-------|------|
| Department/Staff | 5/8 |
| Room_Type/Room | 5/12 |
| Guest/Loyalty | 10/6 |
| Pricing_Rule | 4 |
| Booking/BRD/Payment | 15/18/12 |
| Task_Log | 15 |
| **Total** | **125 rows** |

**右列**：6 类边界情况（含小图标）
- ✓ 重复客人（Guest 1 & 2 多次预订）
- ✓ 多房间预订（Booking 2, 6, 12）
- ✓ 取消 + 退款（Booking 4, 9）
- ✓ 房间复用（Room 101, 303 不同人）
- ✓ 部分支付（Booking 12 Pending）
- ✓ 空完成时间（Task 4 维修中）

**底部**：关键 finding 节选
> "Finding 1: Silver members average \$1,380/booking vs Bronze's \$400 — a 3.5× gap.
> Finding 2: 13.3% cancellation rate concentrates in premium inventory (\$2,480 lost)."

### 讲解要点（40 秒）
> "Our 125-row dataset is small enough to verify by hand yet covers six categories of edge cases — repeat guests, multi-room bookings, cancellations with refunds, room reuse, partial payments, and open work items. Two managerial insights emerge directly from the data: Silver loyalty members spend 3.5× more per booking than Bronze, and 13.3% of bookings are cancelled — concentrated in premium inventory, costing \$2,480 in potential revenue."

### 答辩 Q&A 预案（Member D 必须能答）

| Q | 一句话答案 |
|---|----------|
| 为什么数据只有 125 行？够用吗？ | 够；每条查询都能验证 + 覆盖边界，再多反而难手工核对 |
| Payment 金额有时不等于夜数×房价，为什么？ | 押金（Booking 12）、退款（Booking 4/9）、部分支付场景，符合真实业务 |
| 怎么保证数据"真实"？ | 客人国籍多元（9 国）、邮箱格式符合域名规范、护照号有国家前缀 |
| 5 个 Finding 是怎么算出来的？ | Python 脚本读 sample_data.sql 计算（见 data_analysis_findings.md） |
| Task 4 NULL 完成时间会不会破坏查询？ | 不会；Q6/Q8 用 IS NOT NULL 显式过滤；展示边界处理能力 |

---

## Block 5 — SQL 查询与结果（Member E，占 2 页）

### PPT 内容 Page 6：查询索引与代表代码（约 30 秒）

**标题**：SQL Queries — Covering All 11 Relations

**主要内容**：12 查询索引表（紧凑展示）
```
Q1  Guest spending          Q7  Monthly revenue (LAG)
Q2  Occupancy by type       Q8  Cleaning quality (ROW_NUMBER)
Q3  Pricing impact          Q9  Revenue dashboard VIEW
Q4  Loyalty rank (RANK)     Q10 Cancellation alerts
Q5  Availability (NOT EXISTS)  Q11 VIP scoring CTE
Q6  Dept efficiency         Q12 Overlap detection (self-join)
```

**底部小代码块**：Q5 NOT EXISTS 示例（最能体现防御式设计）
```sql
SELECT r.Room_ID FROM Room r ...
WHERE NOT EXISTS (
  SELECT 1 FROM Booking_Room_Detail brd
  JOIN Booking b ON ...
  WHERE brd.Room_ID = r.Room_ID
    AND b.Overall_Status NOT IN ('Cancelled')
    AND brd.CheckIn_Date  < '2026-06-05'
    AND brd.CheckOut_Date > '2026-06-01');
```

### PPT 内容 Page 7：实跑结果图表（约 35 秒）

**标题**：Live MySQL Results & Insights

**布局**：3 张关键图横排
- 左：`fig3_sankey_loyalty_flow.pdf` — 会员流向预订状态
- 中：`fig5_raincloud_quality.pdf` — 部门质量对比
- 右：`fig9_stacked_bar_payments.pdf` — 支付状态金额分布

**底部**：关键数字
> "Finding 3: Net price premium only +2.20% — weekday discount (−\$1,230) erodes Christmas surge (+\$1,496).
> Finding 5: 12.37% of payment volume at risk (Pending + Refunded)."

### 讲解要点（共 65 秒）
**Page 6（30s）**：
> "Our 12 SQL queries collectively reference all 11 relations and demonstrate the full course toolkit — joins, sub-queries, window functions like RANK and ROW_NUMBER, common table expressions, views, and a self-join for overlap detection. Q5 here illustrates defensive design: we check date-range non-overlap rather than relying on a status flag, which would miss future bookings on rooms still marked Available."

**Page 7（35s）**：
> "Three live findings emerge. Sankey on the left shows our two Platinum members account for repeat business; the small red branch is the cancelled-and-refunded flow. The raincloud reveals Housekeeping's 8.7 mean quality versus Maintenance's 7.3 — a 1.4-point gap pointing to a maintenance staffing bottleneck. The stacked bar exposes 12.37% of revenue at risk — Pending plus Refunded — concentrated in card payments."

### 答辩 Q&A 预案（Member E 必须能答）

| Q | 一句话答案 |
|---|----------|
| Q5 为什么用 NOT EXISTS 而不查 Current_Status？ | Current_Status 只是当下状态；未来预订的房间状态可能还是 Available |
| Q11 的 VIP 评分公式怎么定的？ | 消费 40% + 频率 30% + 忠诚度 30%，三维加权 |
| Q12 为什么返回 0 行是好事？ | 说明数据集无重叠，应用层防护正常工作 |
| 窗口函数 RANK 和 ROW_NUMBER 区别？ | RANK 同分并列、跳号；ROW_NUMBER 永不并列、连续 |
| 12 条查询哪条性能最差？ | Q9 视图 6 表 JOIN；生产环境会加索引 + materialize |
| HAVING 和 WHERE 的区别？为什么 Q8 用 HAVING ≥ 5？ | WHERE 过滤行，HAVING 过滤聚合结果；防止小样本均值误导 |

---

## Block 6 — 创新点：Pricing Agent（Member F，占 2 页）

### PPT 内容 Page 8：公式与原理（约 30 秒）

**标题**：Innovation — Database-Driven Pricing Agent

**中心大公式**（黑板风格）：
```
P_final = P_base × m_rule × f_occ
```

**3 列说明**：
- **P_base**：从 Room_Type.Base_Nightly_Rate 读
- **m_rule**：查 Dynamic_Pricing_Rule（按当前日期匹配最高优先级）
- **f_occ**：实时算 Booking_Room_Detail 的占用率
  - >90% → 1.30
  - >70% → 1.10
  - <40% → 0.85

**核心论点**（高亮）：
> "Pricing intelligence lives in the **DATA layer**, not in code."

### PPT 内容 Page 9：决策流程 + 论证（约 35 秒）

**标题**：Why This Matters — Agent Flow & 3NF Payoff

**主图**：`fig7_agent_flow.pdf` 占 60%

**侧边论点**：
1. 改 1 行 Dynamic_Pricing_Rule → 定价立即变化（无需部署）
2. Pricing 与 Inventory 完全解耦（3NF 设计的回报）
3. 所有定价决策都可审计（每次查询都留痕）

**底部**：与传统方案对比小表
| | Traditional | Our Approach |
|---|---|---|
| Pricing logic | hardcoded | data-driven |
| Change cost | redeploy | UPDATE |
| Auditability | low | high (SQL trace) |

### 讲解要点（共 65 秒）
**Page 8（30s）**：
> "Our innovation is a pricing agent driven entirely by the database. The final price is the product of three factors: the base rate from Room_Type, a rule multiplier from Dynamic_Pricing_Rule, and an occupancy factor computed in real time from Booking_Room_Detail. The intelligence lives in the data layer, not in the code."

**Page 9（35s）**：
> "This matters because changing a single row in Dynamic_Pricing_Rule instantly retargets pricing without a redeployment. The pricing engine and the inventory schema are fully decoupled — that decoupling is the payoff of our BCNF normalisation. Every pricing decision is auditable through SQL traces. This separates us from naive approaches where pricing logic is hardcoded in application code."

### 答辩 Q&A 预案（Member F 必须能答）

| Q | 一句话答案 |
|---|----------|
| 为什么不直接在 SQL 里写 CASE WHEN 定价？ | Agent 还需要做占用率计算 + 多维聚合，SQL 表达困难且不可复用 |
| 规则改了真的不用重启吗？ | 每次查询 Agent 都重新读规则；改 UPDATE 立即生效 |
| 多条规则同时匹配怎么办？ | 用 Priority 字段排序取最高优先级 |
| 占用率因子的阈值（0.85/1.0/1.10/1.30）怎么定的？ | 参考酒店业 Revenue Management 实践；本作业为说明性数值 |
| 这个创新有学术依据吗？ | Talluri & van Ryzin 2004 — Revenue Management 经典；详见 agent_technology.md |

---

## 制作 PPT 的统一要求

### 视觉规范
- **配色**：与报告统一 — Nature 浅色多彩，纯白背景
- **字体**：标题 Calibri/Helvetica Bold；正文 Times New Roman / Calibri 24pt
- **图表**：直接复用 `docs/report/figures/` 里的 PDF（已是高分辨率）
- **标题色**：`#2C3E50`（深蓝灰）— 与报告统一
- **页眉**：左 "EBU5503 Group 13"，右 "Page X of 10"
- **避免**：动画、过场、艺术字、装饰性图标（学术演示忌讳）

### 制作工具建议
- **Keynote**（Mac，推荐 — 与 PDF 兼容好）
- **PowerPoint**（Windows / Mac，普及）
- **LaTeX Beamer**（最专业但学习曲线高）
- **Google Slides**（团队协作但导出 PDF 有时变形）

### 协作分工建议
1. 选 1 个人**统一模板**（封面、配色、字体、页眉页脚） — 这个人不算 6 个块的人
2. 其他 6 人各做 1-2 页填内容
3. 最后**合并 + 统一节奏排练**

### 演讲前 24 小时检查清单
- [ ] 每个组员能在 1 分钟内讲完自己的块（计时演练）
- [ ] 切换时主讲人能流畅串场（"接下来由 X 介绍我们的 EER 设计..."）
- [ ] 答辩 Q&A 表格里每个人至少能独立答 3 个问题
- [ ] PPT 文件已上传 QMplus（演示时必须用这一份）
- [ ] 备份 1 份 PDF 在 U 盘 + 邮件附件

---

## 时间总览（5 分钟严格倒计时）

```
00:00 ─┬─ Page 1  封面开场                 (20s)
00:20 ─┼─ Page 2  Block 1 - Requirements    (45s) ← Member A
01:05 ─┼─ Page 3  Block 2 - EER             (50s) ← Member B
01:55 ─┼─ Page 4  Block 3 - Schema/Normalise(45s) ← Member C
02:40 ─┼─ Page 5  Block 4 - Sample Data     (40s) ← Member D
03:20 ─┼─ Page 6  Block 5a - SQL Code       (30s) ← Member E
03:50 ─┼─ Page 7  Block 5b - SQL Results    (35s) ← Member E (continued)
04:25 ─┼─ Page 8  Block 6a - Agent Formula  (30s) ← Member F
04:55 ─┼─ Page 9  Block 6b - Agent Flow     (35s) ← Member F (continued)
05:30 ─┴─ Page 10 Conclusion + thanks       (20s) ← 主讲人收尾
```

⚠️ 实际时间会 ~5:50，建议每块再压缩 5 秒到 5:00 内。

---

## 答辩注意事项（35 分核心）

**评分原话**：
> "Multiple members confidently and accurately contribute. Answers are clear, accurate, well-justified, and demonstrate critical thinking."

**陷阱**：
- ❌ 只有 1-2 个人答问题 → 直接降级（评分原话："Only 1-2 key members answer most questions" 是 14-20 分档）
- ❌ 照着 PPT 念 → 演示分扣到 4-5 分
- ❌ 答不出"为什么这么设计" → 答辩分大幅扣分

**对策**：
1. 每个组员**至少答对 1 个跨域问题**（不是只答自己负责块）
2. 准备好"我去问问队友"的话术 — 比如"This is more in B 的领域, B 你来补充" — 既显得团队协作好又不出错
3. 全员熟读 `agent/agent_technology.md`（创新点的学术背景）
