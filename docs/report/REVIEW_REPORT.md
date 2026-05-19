# 论文最终评审报告 — EBU5503 Group 13

## A. 评分（满分 55）
- 数据库设计 **28/30**
- 样本数据 **5/5**
- SQL 查询 **14/15**
- GenAI 附录 **4.5/5**
- **合计 51.5/55**

## B. 已合规项

**设计 (28/30)**
- ✓ 5 项创意扩展（Loyalty、Dynamic Pricing、Room_Type、Department/Staff、Task_Log）均给出真实世界对标依据
- ✓ 11 实体 4 域结构清晰；§2 显式列出 7 类关系（M:N 用 Booking_Room_Detail 解，三元用 Task_Log 解）
- ✓ §3.2 1NF→BCNF 推导有具体反例（早期 LOG / ROOM 草案 → 分解），不是套话
- ✓ 假设段落（§1.3）覆盖跨房日期、付款状态、Loyalty 1:1、规则窗口冲突解决

**数据 (5/5)**
- ✓ 125 行覆盖 11 表，并显式枚举边界：重复客 G1/G2、多房 B2/B6/B12、取消退款 B4/B9、房间复用、Pending 部分付款、NULL completion

**SQL (14/15)**
- ✓ §5.1 表格列出每条 Q 用到的关系；交叉核对 `test_queries.sql` 确认 11 个关系全部被引用
- ✓ 覆盖技术广：NOT EXISTS、RANK/ROW_NUMBER、CTE、VIEW、HAVING、self-join
- ✓ Q5/Q11 代码贴出并配业务解释，不是裸 dump

**GenAI (4.5/5)**
- ✓ 6 个 prompt + 6 个 output 截图齐全；工具版本号明确
- ✓ Codex 反查的 7 个 bug 全部记录并标注人工修复

**5 项 Finding 嵌入度**
- ✓ F1 在 §4.3、F2 在 §4.2 & §5.2、F3 在 §6、F4 在 §5.3、F5 在 §4.1 末 & §5.3 — 真正分散在正文，不是末尾堆砌

**版式**
- ✓ 正文 10 页（pdfinfo 确认），未超
- ✓ 11 张图全部前后有解释段，无孤立成页
- ✓ LaTeX 日志仅 3 处 13.14pt overfull（轻微，肉眼不可见）

## C. 仍需改进项（按严重程度）

1. **[轻]** §6 内文称"Figure 10 summarises the four rules"但图编号系列里 fig6_lollipop_pricing.pdf 仍存在于目录 — 检查 `report.tex` 是否引用了未使用的 fig6/fig7（生成目录有 fig3_sankey_flow & fig3_sankey_loyalty_flow 等重复文件，提交目录建议清理避免审阅困惑）。一句话：删除 figures/ 下未被 \includegraphics 引用的 PDF。
2. **[轻]** §3.1 表格中 "Identity_Doc^U" 等上标 U 在 PDF 中渲染良好，但建议在表头脚注里显式写 "U = UNIQUE constraint"（目前只在表前一句话提到）。一句话：在表 caption 加 "U denotes UNIQUE" 脚注以独立可读。
3. **[轻]** Q5 列出的 WHERE 子句中 `'Cancelled '`、`'Completed '` 等枚举值末尾带空格（PDF 第 6 页 Listing 1，第 7 页 Listing 2），是 listings 包对引号内空格的渲染习惯而非真实 SQL bug — 答辩时可能被考官质疑。一句话：在 `\lstset` 中设置 `showstringspaces=false` 重排版。
4. **[轻]** §4.3 同时给出 r≈0.41 和 r=0.455 两个相关系数描述同一对变量，读者会困惑。一句话：明确两值分别对应"Rate vs Points"和"Spend vs Points"（已隐含但需明写）。
5. **[轻]** §5.3 "$2,480 lost" 与 §4.1 "$7,624 settled / 12.37% at risk" 数字需要在答辩时能口述推导路径 — 建议在答辩补充材料里准备一页交叉表。一句话：非论文修改项，准备答辩 backup slide。

## D. 是否可以提交？

**是 ✓**

若仍要打磨，按优先级处理 C1–C3 即可（≤30 分钟工作量），C4/C5 属于答辩准备而非论文修改。

## E. 一句话总评

一份结构紧凑、五处 Finding 真正贯穿正文的 BCNF 级报告 — 不是"能交"，而是"能拿高分"，剩下三处都是格式层面的微调而非内容缺陷。
