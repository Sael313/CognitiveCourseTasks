import csv
import clickhouse_connect

def extract_and_export():
    try:
        # اتصال به ClickHouse
        client = clickhouse_connect.get_client(
            host="localhost", port=8123, username="default", password="", database="posthog"
        )

        # کوئری فیلتر رویدادهای تصمیم‌گیری
        query = """
            SELECT 
                timestamp,
                distinct_id AS user_id,
                event,
                properties
            FROM posthog.sharded_events
            WHERE event IN ('$pageview', 'click', 'submit', '$feature_flag_called', 'decision_made')
            ORDER BY timestamp DESC
        """

        print("در حال اجرای کوئری استخراج رویدادها...")
        result = client.query(query)
        rows = result.result_rows

        print(f"تعداد رویدادهای استخراج‌شده: {len(rows)}")

        # ذخیره در فایل CSV
        csv_filename = "decision_events.csv"
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # نوشتن هدر فایل CSV
            writer.writerow(["timestamp", "user_id", "event", "properties"])
            # نوشتن ردیف‌ها
            writer.writerows(rows)

        print(f"فایل با موفقیت ذخیره شد: {csv_filename}\n")

        # بررسی معیار پذیرش (حداقل ۳ نوع رویداد مختلف)
        unique_events = set(row[2] for row in rows)
        print("انواع رویدادهای موجود در فایل:")
        for ev in unique_events:
            print(f"- {ev}")

        if len(unique_events) >= 3:
            print("\n✅ معیار پذیرش برآورده شد (حداقل ۳ نوع رویداد متناظر یافت شد).")
        else:
            print("\n⚠️ هشدار: تعداد انواع رویدادها کمتر از ۳ نوع است.")

    except Exception as e:
        print(f"خطا در استخراج داده‌ها: {e}")

if __name__ == "__main__":
    extract_and_export()