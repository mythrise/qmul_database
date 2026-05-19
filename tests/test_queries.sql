-- ============================================================
-- 酒店预订管理系统 — 高级 SQL 查询集
-- 数据库: hotel_management
-- ============================================================

USE hotel_management;

-- ------------------------------------------------------------
-- Q1: 每位客人的总消费金额与预订次数
-- 涉及表: Guest, Booking, Payment
-- 技术: 多表 JOIN, 聚合函数, GROUP BY
-- ------------------------------------------------------------
SELECT
    g.Guest_ID,
    CONCAT(g.First_Name, ' ', g.Last_Name) AS Guest_Name,
    g.Email,
    COUNT(DISTINCT b.Booking_ID)            AS Total_Bookings,
    COALESCE(SUM(p.Amount), 0)              AS Total_Spent
FROM Guest g
LEFT JOIN Booking b  ON g.Guest_ID = b.Guest_ID
LEFT JOIN Payment p  ON b.Booking_ID = p.Booking_ID
                    AND p.Status = 'Completed'
GROUP BY g.Guest_ID, g.First_Name, g.Last_Name, g.Email
ORDER BY Total_Spent DESC;

-- ------------------------------------------------------------
-- Q2: 入住率最高的房型排名（已剔除取消单）
-- 涉及表: Room_Type, Room, Booking_Room_Detail, Booking
-- 技术: 多表 JOIN(4表), 聚合, DATEDIFF
-- ------------------------------------------------------------
SELECT
    rt.Type_ID,
    rt.Category_Name,
    COUNT(DISTINCT r.Room_ID)                                AS Room_Count,
    COALESCE(SUM(DATEDIFF(brd.CheckOut_Date, brd.CheckIn_Date)), 0)
                                                              AS Total_Booked_Nights,
    ROUND(
        COALESCE(SUM(DATEDIFF(brd.CheckOut_Date, brd.CheckIn_Date)), 0)
        / (COUNT(DISTINCT r.Room_ID) * 365) * 100, 2
    )                                                        AS Occupancy_Rate_Pct
FROM Room_Type rt
JOIN Room r ON rt.Type_ID = r.Type_ID
LEFT JOIN (
    SELECT brd.Room_ID, brd.CheckIn_Date, brd.CheckOut_Date
    FROM Booking_Room_Detail brd
    JOIN Booking b ON brd.Booking_ID = b.Booking_ID
    WHERE b.Overall_Status NOT IN ('Cancelled')   -- 子查询提前剔除取消单
) brd ON r.Room_ID = brd.Room_ID
GROUP BY rt.Type_ID, rt.Category_Name
ORDER BY Occupancy_Rate_Pct DESC;

-- ------------------------------------------------------------
-- Q3: 动态定价影响分析 — 实际成交价 vs 基准价 vs 规则乘数
-- 涉及表: Dynamic_Pricing_Rule, Room_Type, Room, Booking_Room_Detail
-- 技术: 多表 JOIN(4表), 日期区间匹配, CASE WHEN
-- 说明: 将每条入住明细与其入住期间生效的定价规则匹配，
--      对比基准价、规则建议价与实际成交价，分析定价策略效果。
-- ------------------------------------------------------------
SELECT
    brd.Detail_ID,
    rt.Category_Name,
    rt.Base_Nightly_Rate,
    brd.Final_Agreed_Rate                                       AS Actual_Rate,
    dpr.Event_Name,
    dpr.Price_Multiplier,
    ROUND(rt.Base_Nightly_Rate * dpr.Price_Multiplier, 2)       AS Rule_Suggested_Rate,
    ROUND(
        (brd.Final_Agreed_Rate - rt.Base_Nightly_Rate)
        / rt.Base_Nightly_Rate * 100, 1
    )                                                            AS Actual_Premium_Pct,
    CASE
        WHEN dpr.Price_Multiplier > 1.5 THEN 'High Surge'
        WHEN dpr.Price_Multiplier > 1.0 THEN 'Moderate Increase'
        WHEN dpr.Price_Multiplier = 1.0 THEN 'No Change'
        ELSE 'Discount'
    END                                                         AS Pricing_Impact
FROM Booking_Room_Detail brd
JOIN Room r              ON brd.Room_ID = r.Room_ID
JOIN Room_Type rt        ON r.Type_ID    = rt.Type_ID
JOIN Dynamic_Pricing_Rule dpr
      ON dpr.Is_Active = 1
     AND brd.CheckIn_Date  <= dpr.Effective_End
     AND brd.CheckOut_Date >= dpr.Effective_Start
ORDER BY dpr.Priority DESC, brd.CheckIn_Date;

-- ------------------------------------------------------------
-- Q4: 忠诚度客户消费排名
-- 涉及表: Loyalty_Program, Guest, Payment, Booking
-- 技术: 多表 JOIN(4表), 窗口函数 RANK()
-- ------------------------------------------------------------
SELECT
    ranked.*
FROM (
    SELECT
        lp.Loyalty_ID,
        CONCAT(g.First_Name, ' ', g.Last_Name) AS Guest_Name,
        lp.Tier_Level,
        lp.Available_Points,
        COALESCE(SUM(p.Amount), 0)              AS Total_Spent,
        RANK() OVER (
            PARTITION BY lp.Tier_Level
            ORDER BY SUM(p.Amount) DESC
        )                                       AS Spending_Rank
    FROM Loyalty_Program lp
    JOIN Guest g     ON lp.Guest_ID = g.Guest_ID
    JOIN Booking b   ON g.Guest_ID  = b.Guest_ID
    JOIN Payment p   ON b.Booking_ID = p.Booking_ID AND p.Status = 'Completed'
    GROUP BY lp.Loyalty_ID, g.First_Name, g.Last_Name,
             lp.Tier_Level, lp.Available_Points
) ranked
WHERE ranked.Spending_Rank <= 10
ORDER BY ranked.Tier_Level, ranked.Spending_Rank;

-- ------------------------------------------------------------
-- Q5: 查找特定日期范围内可用的房间
-- 涉及表: Room, Booking_Room_Detail, Room_Type
-- 技术: NOT EXISTS 子查询, 日期重叠判断
-- ------------------------------------------------------------
SELECT
    r.Room_ID,
    rt.Category_Name,
    r.Floor_Level,
    rt.Base_Nightly_Rate,
    rt.Max_Capacity
FROM Room r
JOIN Room_Type rt ON r.Type_ID = rt.Type_ID
WHERE r.Current_Status != 'Maintenance'   -- 排除停用维护中房间
  AND NOT EXISTS (
      SELECT 1
      FROM Booking_Room_Detail brd
      JOIN Booking b ON brd.Booking_ID = b.Booking_ID
      WHERE brd.Room_ID = r.Room_ID
        AND b.Overall_Status NOT IN ('Cancelled')
        AND brd.CheckIn_Date  < '2026-06-05'   -- 期望退房日
        AND brd.CheckOut_Date > '2026-06-01'   -- 期望入住日
  )
ORDER BY rt.Base_Nightly_Rate, r.Floor_Level;

-- ------------------------------------------------------------
-- Q6: 每个部门员工的任务完成效率
-- 涉及表: Department, Staff, Task_Log
-- 技术: 多表 JOIN(3表), GROUP BY, HAVING, AVG
-- ------------------------------------------------------------
SELECT
    d.Dept_ID,
    d.Dept_Name,
    COUNT(DISTINCT s.Staff_ID)              AS Staff_Count,
    COUNT(tl.Log_ID)                        AS Total_Tasks,
    ROUND(AVG(tl.Duration_Minutes), 1)      AS Avg_Duration_Min,
    ROUND(AVG(tl.Quality_Score), 2)         AS Avg_Quality_Score,
    SUM(CASE WHEN tl.Completion_Time IS NOT NULL THEN 1 ELSE 0 END) AS Completed_Tasks
FROM Department d
JOIN Staff s     ON d.Dept_ID  = s.Dept_ID
LEFT JOIN Task_Log tl ON s.Staff_ID = tl.Staff_ID
GROUP BY d.Dept_ID, d.Dept_Name
HAVING COUNT(tl.Log_ID) > 0
ORDER BY Avg_Quality_Score DESC;

-- ------------------------------------------------------------
-- Q7: 月度营收趋势报告
-- 涉及表: Payment, Booking
-- 技术: DATE_FORMAT, GROUP BY, 聚合函数
-- ------------------------------------------------------------
SELECT
    DATE_FORMAT(p.Payment_Date, '%Y-%m')    AS Revenue_Month,
    COUNT(DISTINCT p.Payment_ID)            AS Transaction_Count,
    COUNT(DISTINCT b.Booking_ID)            AS Booking_Count,
    SUM(p.Amount)                           AS Total_Revenue,
    ROUND(AVG(p.Amount), 2)                 AS Avg_Transaction,
    MAX(p.Amount)                           AS Max_Transaction,
    SUM(p.Amount) - LAG(SUM(p.Amount)) OVER (
        ORDER BY DATE_FORMAT(p.Payment_Date, '%Y-%m')
    )                                       AS MoM_Change
FROM Payment p
JOIN Booking b ON p.Booking_ID = b.Booking_ID
WHERE p.Status = 'Completed'
GROUP BY DATE_FORMAT(p.Payment_Date, '%Y-%m')
ORDER BY Revenue_Month;

-- ------------------------------------------------------------
-- Q8: 客房清洁质量评分排行
-- 涉及表: Staff, Task_Log, Room
-- 技术: 窗口函数 ROW_NUMBER(), 多表 JOIN
-- ------------------------------------------------------------
SELECT * FROM (
    SELECT
        s.Staff_ID,
        s.Full_Name,
        s.Job_Role,
        COUNT(tl.Log_ID)                       AS Task_Count,
        ROUND(AVG(tl.Quality_Score), 2)        AS Avg_Quality,
        ROUND(AVG(tl.Duration_Minutes), 1)     AS Avg_Duration,
        COUNT(DISTINCT tl.Room_ID)             AS Rooms_Serviced,
        ROW_NUMBER() OVER (
            ORDER BY AVG(tl.Quality_Score) DESC, AVG(tl.Duration_Minutes) ASC
        )                                      AS Quality_Rank
    FROM Staff s
    JOIN Task_Log tl ON s.Staff_ID = tl.Staff_ID
    JOIN Room r      ON tl.Room_ID = r.Room_ID
    WHERE tl.Task_Type = 'Cleaning'
      AND tl.Completion_Time IS NOT NULL
    GROUP BY s.Staff_ID, s.Full_Name, s.Job_Role
    HAVING COUNT(tl.Log_ID) >= 5
) quality_ranking
ORDER BY Quality_Rank;

-- ------------------------------------------------------------
-- Q9: 营收仪表盘视图
-- 涉及表: Guest, Booking, Booking_Room_Detail, Room, Room_Type, Payment
-- 技术: CREATE VIEW, 多表 JOIN(6表)
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_revenue_dashboard AS
SELECT
    b.Booking_ID,
    CONCAT(g.First_Name, ' ', g.Last_Name)          AS Guest_Name,
    rt.Category_Name                                  AS Room_Category,
    r.Room_ID,
    r.Floor_Level,
    brd.CheckIn_Date,
    brd.CheckOut_Date,
    DATEDIFF(brd.CheckOut_Date, brd.CheckIn_Date)    AS Stay_Nights,
    brd.Final_Agreed_Rate                             AS Nightly_Rate,
    rt.Base_Nightly_Rate,
    ROUND(
        (brd.Final_Agreed_Rate - rt.Base_Nightly_Rate)
        / rt.Base_Nightly_Rate * 100, 1
    )                                                 AS Rate_Variance_Pct,
    COALESCE(pay.Paid_Amount, 0)                      AS Paid_Amount,
    b.Overall_Status
FROM Booking b
JOIN Guest g                 ON b.Guest_ID    = g.Guest_ID
JOIN Booking_Room_Detail brd ON b.Booking_ID  = brd.Booking_ID
JOIN Room r                  ON brd.Room_ID   = r.Room_ID
JOIN Room_Type rt            ON r.Type_ID     = rt.Type_ID
LEFT JOIN (
    SELECT Booking_ID, SUM(Amount) AS Paid_Amount
    FROM Payment
    WHERE Status = 'Completed'
    GROUP BY Booking_ID
) pay ON b.Booking_ID = pay.Booking_ID;

-- 使用视图查询示例
SELECT * FROM v_revenue_dashboard
WHERE Stay_Nights >= 3
ORDER BY Paid_Amount DESC
LIMIT 20;

-- ------------------------------------------------------------
-- Q10: 取消预订分析
-- 涉及表: Booking
-- 技术: CASE WHEN 条件表达式, 比例计算, DATE_FORMAT
-- ------------------------------------------------------------
SELECT
    DATE_FORMAT(b.Creation_Time, '%Y-%m')   AS Month,
    COUNT(*)                                 AS Total_Bookings,
    SUM(CASE WHEN b.Overall_Status = 'Cancelled' THEN 1 ELSE 0 END)
                                             AS Cancelled_Count,
    SUM(CASE WHEN b.Overall_Status = 'Confirmed' THEN 1 ELSE 0 END)
                                             AS Confirmed_Count,
    SUM(CASE WHEN b.Overall_Status = 'Checked-Out' THEN 1 ELSE 0 END)
                                             AS Completed_Count,
    ROUND(
        SUM(CASE WHEN b.Overall_Status = 'Cancelled' THEN 1 ELSE 0 END)
        / COUNT(*) * 100, 2
    )                                        AS Cancellation_Rate_Pct,
    CASE
        WHEN SUM(CASE WHEN b.Overall_Status = 'Cancelled' THEN 1 ELSE 0 END)
             / COUNT(*) > 0.3 THEN 'CRITICAL — Above 30%'
        WHEN SUM(CASE WHEN b.Overall_Status = 'Cancelled' THEN 1 ELSE 0 END)
             / COUNT(*) > 0.15 THEN 'WARNING — Above 15%'
        ELSE 'NORMAL'
    END                                      AS Alert_Level
FROM Booking b
GROUP BY DATE_FORMAT(b.Creation_Time, '%Y-%m')
ORDER BY Month;

-- ------------------------------------------------------------
-- Q11: VIP 客户识别 — 综合消费、忠诚度、频率
-- 涉及表: Guest, Booking, Payment, Loyalty_Program
-- 技术: CTE (WITH 子句), 多维度评分
-- ------------------------------------------------------------
WITH customer_metrics AS (
    SELECT
        g.Guest_ID,
        CONCAT(g.First_Name, ' ', g.Last_Name)  AS Guest_Name,
        g.Email,
        g.Registration_Date,
        COUNT(DISTINCT b.Booking_ID)             AS Booking_Count,
        COALESCE(SUM(p.Amount), 0)               AS Total_Spent,
        DATEDIFF(CURDATE(), MAX(b.Creation_Time)) AS Days_Since_Last_Booking
    FROM Guest g
    LEFT JOIN Booking b  ON g.Guest_ID   = b.Guest_ID
    LEFT JOIN Payment p  ON b.Booking_ID = p.Booking_ID AND p.Status = 'Completed'
    GROUP BY g.Guest_ID, g.First_Name, g.Last_Name, g.Email, g.Registration_Date
),
vip_scoring AS (
    SELECT
        cm.*,
        lp.Tier_Level,
        lp.Available_Points,
        -- 综合 VIP 评分 (0-100)
        ROUND(
            (LEAST(cm.Total_Spent / 10000, 1) * 40)  +   -- 消费权重 40%
            (LEAST(cm.Booking_Count / 10, 1)   * 30)  +   -- 频率权重 30%
            (CASE lp.Tier_Level
                WHEN 'Platinum' THEN 30
                WHEN 'Gold'     THEN 22
                WHEN 'Silver'   THEN 14
                WHEN 'Bronze'   THEN 6
                ELSE 0
            END)                                           -- 忠诚度权重 30%
        , 1) AS VIP_Score
    FROM customer_metrics cm
    LEFT JOIN Loyalty_Program lp ON cm.Guest_ID = lp.Guest_ID
)
SELECT
    Guest_ID, Guest_Name, Email, Tier_Level,
    Booking_Count, Total_Spent, Available_Points,
    VIP_Score,
    CASE
        WHEN VIP_Score >= 80 THEN 'Platinum VIP'
        WHEN VIP_Score >= 60 THEN 'Gold VIP'
        WHEN VIP_Score >= 40 THEN 'Silver VIP'
        ELSE 'Regular'
    END AS VIP_Category
FROM vip_scoring
WHERE VIP_Score >= 40
ORDER BY VIP_Score DESC;

-- ------------------------------------------------------------
-- Q12: 超售风险检测 — 同一房间同一时段的重叠预订
-- 涉及表: Booking_Room_Detail, Booking, Room
-- 技术: 自连接, 日期重叠检测
-- ------------------------------------------------------------
SELECT
    brd1.Room_ID,
    r.Floor_Level,
    brd1.Detail_ID   AS Booking_Detail_1,
    brd1.Booking_ID  AS Booking_1,
    brd1.CheckIn_Date  AS CheckIn_1,
    brd1.CheckOut_Date AS CheckOut_1,
    brd2.Detail_ID   AS Booking_Detail_2,
    brd2.Booking_ID  AS Booking_2,
    brd2.CheckIn_Date  AS CheckIn_2,
    brd2.CheckOut_Date AS CheckOut_2,
    DATEDIFF(
        LEAST(brd1.CheckOut_Date, brd2.CheckOut_Date),
        GREATEST(brd1.CheckIn_Date, brd2.CheckIn_Date)
    ) AS Overlap_Days
FROM Booking_Room_Detail brd1
JOIN Booking_Room_Detail brd2
    ON  brd1.Room_ID    = brd2.Room_ID
    AND brd1.Detail_ID  < brd2.Detail_ID          -- 避免重复配对
    AND brd1.CheckIn_Date  < brd2.CheckOut_Date    -- 重叠条件
    AND brd1.CheckOut_Date > brd2.CheckIn_Date
JOIN Booking b1 ON brd1.Booking_ID = b1.Booking_ID
JOIN Booking b2 ON brd2.Booking_ID = b2.Booking_ID
JOIN Room r     ON brd1.Room_ID    = r.Room_ID
WHERE b1.Overall_Status NOT IN ('Cancelled')
  AND b2.Overall_Status NOT IN ('Cancelled')
ORDER BY brd1.Room_ID, Overlap_Days DESC;

-- ============================================================
-- END OF QUERY SET
-- ============================================================
