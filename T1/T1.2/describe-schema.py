"""
T1.2 - کاوش Schema رویدادها

این اسکریپت با استفاده از کوئری DESCRIBE، ساختار سه جدول اصلی PostHog
در ClickHouse را استخراج و در یک فایل متنی ذخیره می‌کند:
    - events
    - person (نکته: اسم واقعی جدول در ClickHouse مفرد "person" است، نه "persons")
    - session_replay_events

پیش‌نیاز:
    pip install clickhouse-connect
"""

import clickhouse_connect
import sys

TABLES = ["events", "person", "session_replay_events"]


def get_client():
    try:
        return clickhouse_connect.get_client(
            host="localhost",
            port=8123,
            username="default",
            password="",
            database="posthog",
        )
    except Exception as e:
        print(f"❌ خطا در برقراری اتصال به ClickHouse: {e}")
        sys.exit(1)


def describe_table(client, table_name: str):
    print(f"\n{'=' * 60}")
    print(f"جدول: {table_name}")
    print("=" * 60)
    result = client.query(f"DESCRIBE TABLE {table_name}")
    for row in result.result_rows:
        # ساختار خروجی DESCRIBE: name, type, default_type, default_expression, comment, ...
        col_name, col_type = row[0], row[1]
        print(f"{col_name:<35} {col_type}")
    return result.result_rows


def main():
    client = get_client()
    output_lines = []

    for table in TABLES:
        rows = describe_table(client, table)
        output_lines.append(f"### {table}\n")
        output_lines.append("| ستون | نوع |\n|---|---|\n")
        for row in rows:
            output_lines.append(f"| {row[0]} | {row[1]} |\n")
        output_lines.append("\n")

    with open("schema_raw_output.md", "w", encoding="utf-8") as f:
        f.writelines(output_lines)

    print("\n✅ خروجی خام Schema در فایل schema_raw_output.md ذخیره شد.")


if __name__ == "__main__":
    main()