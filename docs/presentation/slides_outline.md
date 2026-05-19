# EBU5503 酒店预订与管理系统 — 演示幻灯片大纲

## Slide 1: 封面
- **Title:** Hotel Booking & Management System — A Database-Driven Intelligent Approach
- **Course:** EBU5503 Database Systems 2025/26
- **Scenario:** 2 — Hotel Booking and Management System
- 小组成员名单

## Slide 2: 需求概述（Requirements Overview）
- 基本需求：Guests, Rooms, Bookings, Payments
- **附加需求（创新点）：**
  - 忠诚度计划（Loyalty Program）— 积分与会员等级
  - 动态定价系统（Dynamic Pricing）— 基于事件与入住率的智能调价
  - 任务追踪系统（Task Log）— 三元关系追踪 Staff-Room-Task
  - 部门与员工管理（Department & Staff）
- 假设说明

## Slide 3: EER 图设计（Conceptual Schema）
- 完整 EER 图（MySQL Workbench 截图或手绘）
- 标注 11 个实体及其关系
- 重点标注：
  - Booking_Room_Detail 作为关联实体（消除 M:N）
  - Task_Log 的三元关系（Staff × Room × Task_Type）
  - Loyalty_Program 与 Guest 的 1:1 可选关系

## Slide 4: 关系模式与规范化（Relational Schema & Normalization）
- 列出核心关系模式（标注 PK/FK）
- 规范化验证摘要：
  - 1NF: 拆分 LOG → Booking + Booking_Room_Detail + Payment
  - 2NF: 抽离 Room_Type（消除部分依赖）
  - 3NF: Payment 只保留 Booking_ID（消除传递依赖）

## Slide 5: 创新亮点 — 动态定价 Agent（Innovation: Pricing Agent）
- 架构图：Database ↔ Python Agent ↔ 定价建议
- 定价公式：最终价格 = 基准价 × 事件乘数 × 入住率因子
- Dynamic_Pricing_Rule 表的设计理念
- 代码片段展示

## Slide 6-7: 样本数据展示（Sample Data）
- 各表数据量一览
- 重点展示边界情况：
  - 同一客人多次预订
  - 一个预订多个房间
  - 已取消预订 + 退款
  - 同一房间不同时段被不同人预订

## Slide 8-9: SQL 查询与结果（Queries & Results）
- 精选 6-8 条代表性查询，展示结果截图：
  - Q1: 客人消费排行（多表 JOIN + 聚合）
  - Q3: 动态定价影响分析
  - Q5: 可用房间查询（NOT EXISTS）
  - Q8: 清洁质量排行（窗口函数）
  - Q9: 营收仪表盘视图
  - Q11: VIP 客户识别（CTE）
  - Q12: 超售风险检测（自连接）

## Slide 10: 总结与反思（Summary）
- 设计总结：11 张表、全面覆盖酒店运营场景
- 创新总结：动态定价 Agent、三元关系任务追踪、超售检测
- 团队分工与反思
