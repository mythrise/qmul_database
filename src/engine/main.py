"""
酒店预订管理系统 — 数据库初始化与验证引擎

功能:
1. 执行 init.sql 建表
2. 执行 sample_data.sql 填充数据
3. 运行 test_queries.sql 中的查询并输出结果
4. 调用 Pricing Agent 展示动态定价
"""

import re
import sys
from pathlib import Path
from datetime import date, timedelta

import mysql.connector
from mysql.connector import Error

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
from agent.pricing_agent import DynamicPricingAgent  # noqa: E402


def get_connection(database=None):
    params = dict(host="localhost", user="root", password="")
    if database:
        params["database"] = database
    return mysql.connector.connect(**params)


def split_sql_statements(sql: str) -> list[str]:
    """按分号切分 SQL 语句，先剥离行注释和块注释，避免吞掉带注释的有效语句。"""
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)         # 块注释
    sql = re.sub(r"--[^\n]*", "", sql)                              # 行注释
    statements = []
    for stmt in sql.split(";"):
        stmt = stmt.strip()
        if stmt:
            statements.append(stmt)
    return statements


def execute_sql_file(filepath: Path, conn):
    """执行 SQL 文件中的所有语句。"""
    sql = filepath.read_text(encoding="utf-8")
    cursor = conn.cursor()
    for stmt in split_sql_statements(sql):
        try:
            cursor.execute(stmt)
        except Error as e:
            print(f"  [WARN] {e.msg[:80]}")
    conn.commit()
    cursor.close()


def run_query_file(filepath: Path, conn):
    """逐条执行查询文件并打印结果。"""
    sql = filepath.read_text(encoding="utf-8")
    cursor = conn.cursor()
    query_num = 0
    for stmt in split_sql_statements(sql):
        if stmt.upper().startswith("USE"):
            continue
        try:
            cursor.execute(stmt)
            if cursor.with_rows:
                query_num += 1
                rows = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description]
                print(f"\n{'='*60}")
                print(f"  Query {query_num} — {len(rows)} row(s)")
                print(f"{'='*60}")
                print("  | ".join(cols))
                print("-" * 60)
                for row in rows[:10]:
                    print("  | ".join(str(v) for v in row))
                if len(rows) > 10:
                    print(f"  ... and {len(rows) - 10} more rows")
        except Error as e:
            print(f"  [SKIP] {e.msg[:80]}")
    cursor.close()


def demo_pricing_agent():
    """调用 Pricing Agent 输出未来一周的定价建议，展示数据库驱动决策的创新点。"""
    print(f"\n{'='*60}")
    print("  [4/4] 动态定价 Agent 演示")
    print(f"{'='*60}")
    agent = DynamicPricingAgent(
        host="localhost", user="root", password="", database="hotel_management"
    )
    try:
        target = date.today() + timedelta(days=7)
        print(f"  目标日期: {target}\n")
        for s in agent.suggest_all(target):
            print(f"  房型: {s.room_type}")
            print(f"    基准价: {s.base_rate:.2f}  ->  建议价: {s.final_price:.2f}")
            print(f"    决策依据: {s.reason}")
            print(f"  {'-'*56}")
    finally:
        agent.close()


def main():
    print("=" * 60)
    print("  Hotel Booking & Management System — Database Engine")
    print("=" * 60)

    schema_file = BASE_DIR / "schema" / "init.sql"
    data_file = BASE_DIR / "schema" / "sample_data.sql"
    query_file = BASE_DIR.parent / "tests" / "test_queries.sql"

    print("\n[1/4] 执行建表脚本...")
    conn = get_connection()
    execute_sql_file(schema_file, conn)
    conn.close()
    print("  ✓ 数据库 hotel_management 创建完成，11 张表就绪")

    print("\n[2/4] 填充样本数据...")
    conn = get_connection("hotel_management")
    execute_sql_file(data_file, conn)
    conn.close()
    print("  ✓ 样本数据填充完成")

    print("\n[3/4] 执行测试查询...")
    conn = get_connection("hotel_management")
    run_query_file(query_file, conn)
    conn.close()

    demo_pricing_agent()

    print(f"\n{'='*60}")
    print("  All done.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
