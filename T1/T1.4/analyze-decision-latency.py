# -*- coding: utf-8 -*-
"""
T1.4 - تحلیل اکتشافی داده‌های استخراج‌شده

این اسکریپت فایل decision_related_events.csv (خروجی T1.3) را می‌خواند و
"Decision Latency" را محاسبه می‌کند: فاصله زمانی (بر حسب میلی‌ثانیه) بین
هر رویداد متوالی برای هر کاربر (user_id) به‌صورت جداگانه.

سپس آمار توصیفی (میانگین، میانه، انحراف معیار) این فاصله‌های زمانی محاسبه
و هیستوگرام توزیع آن رسم و در قالب PNG ذخیره می‌شود.

پیش‌نیاز:
    pip install pandas matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# فونت پیش‌فرض برای نمایش بهتر (در صورت نبود فونت فارسی، اعداد و عناوین انگلیسی هم قابل فهم می‌مانند)
matplotlib.rcParams["axes.unicode_minus"] = False

INPUT_FILE = "decision_related_events.csv"
OUTPUT_PNG = "decision_latency_distribution.png"
OUTPUT_STATS_CSV = "decision_latency_stats.csv"


def main():
    df = pd.read_csv(INPUT_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # مرتب‌سازی بر اساس کاربر و زمان
    df = df.sort_values(["user_id", "timestamp"]).reset_index(drop=True)

    # محاسبه فاصله زمانی (latency) بین هر رویداد و رویداد قبلی همان کاربر
    df["latency_ms"] = (
        df.groupby("user_id")["timestamp"].diff().dt.total_seconds() * 1000
    )

    # حذف اولین رویداد هر کاربر (چون فاصله‌ای برای محاسبه ندارد -> NaN)
    latency_series = df["latency_ms"].dropna()

    if latency_series.empty:
        print("⚠️ داده کافی برای محاسبه Decision Latency وجود ندارد (هر کاربر فقط یک رویداد دارد).")
        return

    # --- آمار توصیفی ---
    mean_val = latency_series.mean()
    median_val = latency_series.median()
    std_val = latency_series.std()
    min_val = latency_series.min()
    max_val = latency_series.max()
    count_val = latency_series.count()

    stats_df = pd.DataFrame(
        {
            "معیار": ["تعداد نمونه", "میانگین (ms)", "میانه (ms)", "انحراف معیار (ms)", "حداقل (ms)", "حداکثر (ms)"],
            "مقدار": [count_val, round(mean_val, 2), round(median_val, 2), round(std_val, 2), round(min_val, 2), round(max_val, 2)],
        }
    )
    stats_df.to_csv(OUTPUT_STATS_CSV, index=False, encoding="utf-8-sig")

    print("=" * 50)
    print("آمار توصیفی Decision Latency (میلی‌ثانیه)")
    print("=" * 50)
    print(stats_df.to_string(index=False))
    print(f"\n✅ آمار در فایل {OUTPUT_STATS_CSV} ذخیره شد.")

    # --- رسم هیستوگرام ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(latency_series, bins=20, color="#4C72B0", edgecolor="black", alpha=0.8)

    ax.set_title("توزیع فاصله زمانی تصمیم‌گیری کاربر (Decision Latency)", fontsize=14)
    ax.set_xlabel("فاصله زمانی بین رویدادهای متوالی (میلی‌ثانیه)", fontsize=12)
    ax.set_ylabel("تعداد رویدادها", fontsize=12)

    # افزودن خطوط میانگین و میانه برای خوانایی بهتر
    ax.axvline(mean_val, color="red", linestyle="--", linewidth=1.5, label=f"میانگین: {mean_val:.1f}ms")
    ax.axvline(median_val, color="green", linestyle="--", linewidth=1.5, label=f"میانه: {median_val:.1f}ms")
    ax.legend()

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=150)
    print(f"✅ نمودار هیستوگرام در فایل {OUTPUT_PNG} ذخیره شد.")


if __name__ == "__main__":
    main()