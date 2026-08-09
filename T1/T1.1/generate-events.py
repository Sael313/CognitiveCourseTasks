import time
import requests

# آدرس پست‌هاگ لوکال شما روی پورت 80
POSTHOG_HOST = "http://localhost"
# کلید پروژه (Project API Key / Write Key) از تنظیمات پست‌هاگ لوکال
# اگر ندارید، می‌توانید آن را از پنل PostHog -> Project Settings برداشت کنید
PROJECT_API_KEY = "phc_mBcUArraWx2STiWJVzSDsaMiVRPEKJboKcGmc68MNMhf"


def generate_dummy_events(count=120):
    url = f"{POSTHOG_HOST}/capture/"
    print(f"در حال ارسال {count} رویداد به PostHog لوکال...")

    events_list = [
        "$pageview",
        "click",
        "submit",
        "$feature_flag_called",
        "decision_made",
    ]

    for i in range(count):
        event_name = events_list[i % len(events_list)]
        user_id = f"user_{i % 5}"  # شبیه‌سازی ۵ کاربر مختلف

        data = {
            "api_key": PROJECT_API_KEY,
            "event": event_name,
            "properties": {
                "distinct_id": user_id,
                "button_id": f"btn_{i % 3}",
                "decision_latency_ms": 150 + (i * 10),
            },
        }

        try:
            res = requests.post(url, json=data)
            if res.status_code != 200:
                print(f"خطا در ارسال: {res.status_code}")
        except Exception as e:
            print(f"خطا: {e}")
            break

    print("ارسال رویدادها تمام شد. چند ثانیه صبر کنید تا داده‌ها در ClickHouse flush شوند...")
    time.sleep(5)


if __name__ == "__main__":
    generate_dummy_events(120)