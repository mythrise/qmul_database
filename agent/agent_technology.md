# Agent 技术调研：数据库驱动的智能决策系统

## 1. 核心概念

**Database-Driven Agent** 指的是以数据库为核心知识源和决策依据的智能体系统。与传统硬编码规则不同，Agent 从数据库中实时获取业务状态、历史模式和外部约束，通过算法推理产生决策输出，再将结果写回数据库形成闭环。

```
┌─────────────┐     查询状态      ┌──────────────┐
│   Database   │ ◄──────────────  │  Pricing     │
│  (MySQL)     │                  │  Agent       │
│              │ ──────────────►  │  (Python)    │
│  - 房型价格   │    返回数据       │              │
│  - 入住率     │                  │  决策逻辑:    │
│  - 定价规则   │ ◄──────────────  │  - 供需分析   │
│  - 预订记录   │    写入定价建议    │  - 规则匹配   │
└─────────────┘                  │  - 乘数计算   │
                                 └──────────────┘
```

## 2. 学术背景

### 2.1 动态定价（Dynamic Pricing）

动态定价在酒店收益管理（Revenue Management）中已有成熟研究：

- **Talluri & van Ryzin (2004)** — *The Theory and Practice of Revenue Management*：奠定了基于需求预测的动态定价理论框架，提出了按时间窗口、库存水平调整价格的核心模型。
- **Bitran & Caldentey (2003)** — *An Overview of Pricing Models for Revenue Management* (Manufacturing & Service Operations Management)：系统综述了定价模型在服务行业的应用，特别是酒店和航空业。

### 2.2 数据库中的智能查询优化

- **Marcus et al. (2019)** — *Neo: A Learned Query Optimizer* (VLDB)：展示了如何将机器学习 Agent 嵌入数据库查询优化器中，实现自适应的查询计划选择。
- **Kraska et al. (2018)** — *The Case for Learned Index Structures* (SIGMOD)：提出用学习型模型替代传统 B-Tree 索引，开启了 "AI for DB" 研究方向。

### 2.3 Multi-Agent 系统与数据库交互

- **Jennings et al. (1998)** — *A Roadmap of Agent Research and Development* (Autonomous Agents and Multi-Agent Systems)：定义了 Agent 的自主性、社交性、反应性和主动性四大特征。

## 3. 本项目的 Agent 设计

### 3.1 Pricing Agent（动态定价 Agent）

**输入：**
- 目标入住日期范围
- 房型（Room_Type）
- 当前入住率（从 Booking_Room_Detail 实时计算）
- 活跃的定价规则（Dynamic_Pricing_Rule）

**决策逻辑：**
```
最终价格 = 基准房价 × 事件乘数 × 入住率因子

其中：
- 事件乘数 = MAX(匹配的定价规则的 Price_Multiplier)
- 入住率因子 = 1 + 0.3 × (当前入住率 - 0.7)  当入住率 > 70%
             = 0.9                              当入住率 < 40%
             = 1.0                              其他情况
```

**输出：**
- 定价建议（含明细拆解）
- 预计收益变化

### 3.2 设计亮点

| 特性 | 传统系统 | 本项目 Agent 方案 |
|------|---------|-----------------|
| 定价方式 | 固定价格表 | 基于实时数据库状态的动态计算 |
| 规则管理 | 硬编码 | 存储在 Dynamic_Pricing_Rule 表中，可运行时增删 |
| 入住率感知 | 无 | 实时查询 Booking_Room_Detail 计算 |
| 可审计性 | 低 | 所有定价依据均可追溯至数据库记录 |

## 4. 技术实现栈

- **Python 3.x** + `mysql-connector-python`：Agent 运行时
- **MySQL 8.0**：核心数据存储与查询引擎
- **SQL 视图/CTE**：为 Agent 预计算关键指标（入住率、营收趋势）

## 5. 与课程知识的关联

本 Agent 设计直接建立在课程核心概念之上：
- **关系代数 → SQL 查询**：Agent 通过 JOIN、聚合、子查询获取决策数据
- **规范化设计**：Dynamic_Pricing_Rule 独立成表（满足 3NF），避免规则数据与房型表耦合
- **数据完整性**：CHECK 约束确保 Price_Multiplier > 0，防止 Agent 写入非法数据
- **并发控制**：通过日期区间重叠检测（Date Overlap Query）防止超售
