"""
动态定价 Agent — 酒店预订管理系统

基于数据库驱动的智能定价决策原型。Agent 从 MySQL 数据库实时获取
定价规则、房型信息和入住率数据，综合计算动态房价并输出定价建议。

核心公式: 动态价格 = 基准价 x 定价乘数 x 入住率因子
"""

import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta
from dataclasses import dataclass


@dataclass
class PricingSuggestion:
    """定价建议结果"""
    room_type: str
    base_rate: float
    multiplier: float
    occupancy_factor: float
    final_price: float
    reason: str


class DynamicPricingAgent:
    """数据库驱动的动态定价 Agent。

    通过查询 Dynamic_Pricing_Rule、Room_Type、Room 和 Booking_Room_Detail
    四张核心表，实时计算某一日期的最优房价。
    """

    # 入住率对应的调价因子
    OCCUPANCY_TIERS = [
        (0.9, 1.30, "入住率 >90%: 高需求溢价"),
        (0.7, 1.10, "入住率 >70%: 适度上调"),
        (0.4, 1.00, "入住率 40%-70%: 维持基准"),
        (0.0, 0.85, "入住率 <40%: 促销折扣"),
    ]

    def __init__(self, host="localhost", user="root", password="", database="hotel_management"):
        """初始化数据库连接。"""
        try:
            self.conn = mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )
            print("[Agent] 数据库连接成功")
        except Error as e:
            raise ConnectionError(f"数据库连接失败: {e}")

    def _query(self, sql, params=None):
        """执行查询并返回结果列表。"""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_active_rules(self, target_date: date) -> list[dict]:
        """查询目标日期生效的定价规则（按优先级降序）。"""
        sql = """
            SELECT Rule_ID, Event_Name, Price_Multiplier, Priority
            FROM Dynamic_Pricing_Rule
            WHERE Is_Active = 1
              AND Effective_Start <= %s
              AND Effective_End   >= %s
            ORDER BY Priority DESC
        """
        return self._query(sql, (target_date, target_date))

    def get_occupancy_rate(self, type_id: int, target_date: date) -> float:
        """计算指定房型在目标日期的入住率。

        通过子查询先剔除已取消的预订，再统计目标日期被占用的房间数，
        避免 cancelled 明细被错误计入入住率。
        """
        sql = """
            SELECT
                (SELECT COUNT(*) FROM Room WHERE Type_ID = %s) AS total_rooms,
                COUNT(DISTINCT brd.Room_ID)                     AS booked_rooms
            FROM Booking_Room_Detail brd
            JOIN Booking b ON brd.Booking_ID = b.Booking_ID
            JOIN Room r    ON brd.Room_ID    = r.Room_ID
            WHERE r.Type_ID = %s
              AND b.Overall_Status NOT IN ('Cancelled')
              AND brd.CheckIn_Date  <= %s
              AND brd.CheckOut_Date >  %s
        """
        result = self._query(sql, (type_id, type_id, target_date, target_date))
        row = result[0]
        if row["total_rooms"] == 0:
            return 0.0
        return row["booked_rooms"] / row["total_rooms"]

    def _occupancy_factor(self, rate: float) -> tuple[float, str]:
        """根据入住率返回调价因子和原因说明。"""
        for threshold, factor, reason in self.OCCUPANCY_TIERS:
            if rate >= threshold:
                return factor, reason
        return 1.0, "默认"

    def calculate_price(self, type_id: int, target_date: date) -> PricingSuggestion:
        """核心决策: 综合定价规则、基准价和入住率计算最终价格。"""
        # 1. 获取房型基准价
        room_types = self._query(
            "SELECT Category_Name, Base_Nightly_Rate FROM Room_Type WHERE Type_ID = %s",
            (type_id,),
        )
        if not room_types:
            raise ValueError(f"房型 {type_id} 不存在")
        rt = room_types[0]
        base_rate = float(rt["Base_Nightly_Rate"])

        # 2. 获取最高优先级的定价规则乘数（无规则则为 1.0）
        rules = self.get_active_rules(target_date)
        multiplier = rules[0]["Price_Multiplier"] if rules else 1.0
        event_name = rules[0]["Event_Name"] if rules else "无特殊事件"

        # 3. 计算入住率因子
        occ_rate = self.get_occupancy_rate(type_id, target_date)
        occ_factor, occ_reason = self._occupancy_factor(occ_rate)

        # 4. 最终价格 = 基准价 x 定价乘数 x 入住率因子
        final_price = round(base_rate * float(multiplier) * occ_factor, 2)

        reason = (
            f"事件「{event_name}」乘数 {multiplier} | "
            f"入住率 {occ_rate:.0%} -> 因子 {occ_factor} ({occ_reason})"
        )
        return PricingSuggestion(
            room_type=rt["Category_Name"],
            base_rate=base_rate,
            multiplier=float(multiplier),
            occupancy_factor=occ_factor,
            final_price=final_price,
            reason=reason,
        )

    def suggest_all(self, target_date: date) -> list[PricingSuggestion]:
        """为所有房型生成定价建议。"""
        types = self._query("SELECT Type_ID FROM Room_Type")
        return [self.calculate_price(t["Type_ID"], target_date) for t in types]

    def close(self):
        """关闭数据库连接。"""
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("[Agent] 数据库连接已关闭")


# ── 演示入口 ──────────────────────────────────────────────
if __name__ == "__main__":
    agent = DynamicPricingAgent(
        host="localhost", user="root", password="", database="hotel_management"
    )
    try:
        target = date.today() + timedelta(days=7)
        print(f"\n{'='*60}")
        print(f"  动态定价建议  |  目标日期: {target}")
        print(f"{'='*60}")

        for s in agent.suggest_all(target):
            print(f"\n  房型: {s.room_type}")
            print(f"  基准价: ¥{s.base_rate:.2f}")
            print(f"  建议价: ¥{s.final_price:.2f}")
            print(f"  决策依据: {s.reason}")
            print(f"  {'-'*56}")
    finally:
        agent.close()
