"""
T1.1 - اتصال به ClickHouse پست‌هاگ

این اسکریپت با استفاده از کتابخانه clickhouse-connect به دیتابیس ClickHouse
مربوط به PostHog (اجرا شده با docker-compose، سرویس posthog-hobby-clickhouse-1)
متصل می‌شود و یک کوئری ساده SELECT اجرا می‌کند تا از برقراری اتصال و
وجود داده‌ی واقعی در جدول events اطمینان حاصل شود.

پیش‌نیاز نصب:
    pip install clickhouse-connect
"""

import clickhouse_connect
import sys


def get_client():
    """ساخت و بازگرداندن کلاینت اتصال به ClickHouse."""
    try:
        client = clickhouse_connect.get_client(
            host="localhost",
            port=8123,          # پورت HTTP ClickHouse (posthog-hobby)
            username="default", # یوزر پیش‌فرض (پسوردی ست نشده)
            password="",
            database="posthog", # دیتابیس مشخص‌شده در docker-compose.base.yml
        )
        return client
    except Exception as e:
        print(f"❌ خطا در برقراری اتصال به ClickHouse: {e}")
        sys.exit(1)


def main():
    client = get_client()

    # 1) تست ساده اتصال: گرفتن نسخه سرور
    version = client.command("SELECT version()")
    print(f"✅ اتصال برقرار شد. نسخه ClickHouse: {version}")

    # 2) کوئری موفق SELECT روی جدول events با حداقل ۱۰۰ ردیف رویداد واقعی
    result = client.query(
        """
        SELECT
            event,
            timestamp,
            distinct_id,
            uuid
        FROM events
        ORDER BY timestamp DESC
        LIMIT 100
        """
    )

    rows = result.result_rows
    print(f"\n✅ کوئری با موفقیت اجرا شد. تعداد ردیف‌های دریافتی: {len(rows)}")

    if len(rows) < 100:
        print(
            "⚠️  هشدار: تعداد رویدادهای واقعی در جدول events کمتر از ۱۰۰ است. "
            "لطفاً ابتدا کمی با PostHog تعامل کنید (کلیک/بازدید صفحه) تا رویداد تولید شود."
        )

    print("\n--- نمونه 100 ردیف اول ---")
    for row in rows[:100]:
        print(row)


if __name__ == "__main__":
    main()