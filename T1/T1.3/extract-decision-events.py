"""
T1.3 - استخراج رویدادهای مرتبط با تصمیم‌گیری کاربر

این اسکریپت رویدادهایی که نشان‌دهنده فرآیند تصمیم‌گیری کاربر هستند
(click، $pageview، submit، $feature_flag_called) را از جدول events
استخراج کرده و در قالب یک فایل CSV ذخیره می‌کند.

نکته: نام واقعی رویداد "بازدید صفحه" در PostHog به‌صورت "$pageview" است.

پیش‌نیاز:
    pip install clickhouse-connect
"""

import clickhouse_connect
import csv
import sys

TARGET_EVENTS = ["click", "$pageview", "submit", "$feature_flag_called"]
OUTPUT_FILE = "decision_related_events.csv"


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


def main():
    client = get_client()

    events_list = ", ".join(f"'{e}'" for e in TARGET_EVENTS)
    query = f"""
        SELECT
            timestamp,
            distinct_id AS user_id,
            event,
            properties
        FROM events
        WHERE event IN ({events_list})
        ORDER BY timestamp ASC
    """

    result = client.query(query)
    rows = result.result_rows
    columns = result.column_names

    if not rows:
        print("⚠️  هیچ رکوردی با این شرایط پیدا نشد.")
        sys.exit(1)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    # گزارش خلاصه بر اساس نوع رویداد
    event_counts = {}
    for row in rows:
        ev = row[2]
        event_counts[ev] = event_counts.get(ev, 0) + 1

    print(f"✅ استخراج با موفقیت انجام شد. تعداد کل رکوردها: {len(rows)}")
    print(f"✅ فایل خروجی ذخیره شد: {OUTPUT_FILE}")
    print("\n--- توزیع بر اساس نوع رویداد ---")
    for ev, cnt in event_counts.items():
        print(f"{ev:<25} {cnt}")

    print(f"\nتعداد انواع رویداد مختلف: {len(event_counts)}")
    if len(event_counts) < 3:
        print("⚠️  هشدار: تعداد انواع رویداد کمتر از ۳ است (معیار پذیرش برآورده نشده).")


if __name__ == "__main__":
    main()