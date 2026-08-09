import os
import clickhouse_connect

# تنظیم دیتابیس پیش‌فرض روی posthog
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "8123"))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")
CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB", "posthog")  # تغییر به posthog


def fetch_events_local():
    try:
        print("در حال اتصال به ClickHouse لوکال...")
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DB,
        )
        print("اتصال موفقیت‌آمیز بود!\n")

        # کوئری صریح از جدول posthog.events
        query = """
            SELECT 
                event,
                distinct_id,
                timestamp,
                properties
            FROM posthog.events
            LIMIT 100
        """

        print("در حال اجرای کوئری...")
        result = client.query(query)

        rows = result.result_rows
        print(f"تعداد ردیف‌های دریافت شده: {len(rows)}\n")

        if rows:
            print("نمونه 100 ردیف اول:")
            print("-" * 50)
            for row in rows[:100]:
                print(
                    f"Event: {row[0]} | User: {row[1]} | Timestamp: {row[2]}"
                )
        else:
            print("جدول events خالی است یا هنوز داده‌ای ثبت نشده است.")

        return rows

    except Exception as e:
        print(f"خطا در اتصال: {e}")
        return None


if __name__ == "__main__":
    fetch_events_local()