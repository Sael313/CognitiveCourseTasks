# PostHog ClickHouse Schema Documentation (T1.2)

## 1. posthog.events
| Column | Type | Description |
| :--- | :--- | :--- |
| uuid | UUID | Unique event identifier |
| event | String | Event name |
| properties | String | JSON metadata of event |
| timestamp | DateTime64 | UTC timestamp of event |
| team_id | Int64 | Project ID |
| distinct_id | String | User identifier |
| person_id | UUID | Reference ID to posthog.person |
| created_at | DateTime64 | Ingestion timestamp |

## 2. posthog.person
| Column | Type | Description |
| :--- | :--- | :--- |
| id | UUID | Unique person profile ID |
| team_id | Int64 | Project ID |
| properties | String | User attributes in JSON |
| is_identified | Int8 | 1 = identified, 0 = anonymous |
| last_seen_at | DateTime64 | Last activity time |
| created_at | DateTime64 | First seen timestamp |

## 3. posthog.session_replay_events
| Column | Type | Description |
| :--- | :--- | :--- |
| session_id | String | Session recording ID |
| distinct_id | String | Associated user identifier |
| min_first_timestamp | DateTime64 | Session start time |
| max_last_timestamp | DateTime64 | Session end time |
| active_milliseconds | Int64 | Active duration in ms |
| click_count | Int64 | Total user clicks |


# PostHog Database Schema

## جدول `posthog.events`

| نام ستون         | نوع داده (Data Type)   | توضیح و کاربرد فارسی                                      |
| ---------------- | ---------------------- | --------------------------------------------------------- |
| `uuid`           | `UUID`                 | شناسه منحصر‌به‌فرد و یکتای هر رویداد                      |
| `event`          | `String`               | نام رویداد (مانند `$pageview`، `click`، `submit`)         |
| `properties`     | `String` (JSON)        | ویژگی‌ها و متادیتای اختصاصی رویداد به فرمت JSON           |
| `timestamp`      | `DateTime64(6, 'UTC')` | زمان دقیق وقوع رویداد در منطقه زمانی UTC                  |
| `team_id`        | `Int64`                | شناسه پروژه‌ای که رویداد متعلق به آن است                  |
| `distinct_id`    | `String`               | شناسه کاربر ایفا‌کننده رویداد (شناسانه یا ناشناس)         |
| `person_id`      | `UUID`                 | شناسه ارجاعی به پروفایل کاربر در جدول `person`            |
| `elements_chain` | `String`               | زنجیره عناصر HTML درگیر در تعامل (مانند دکمه‌ها و فرم‌ها) |
| `created_at`     | `DateTime64(6, 'UTC')` | زمان درج و ورود داده به دیتابیس ClickHouse                |
| `$session_id`    | `String`               | شناسه نشستی (Session) که رویداد در آن رخ داده است         |

---

## جدول `posthog.person`

| نام ستون        | نوع داده (Data Type)      | توضیح و کاربرد فارسی                                  |
| --------------- | ------------------------- | ----------------------------------------------------- |
| `id`            | `UUID`                    | شناسه یکتا و اصلی پروفایل کاربر (Person ID)           |
| `team_id`       | `Int64`                   | شناسه پروژه مرتبط                                     |
| `properties`    | `String` (JSON)           | ویژگی‌های شخصی کاربر (مانند ایمیل، نام، سطح اشتراک)   |
| `is_identified` | `Int8`                    | وضعیت شناسایی کاربر (۱ = کاربر لاگین‌شده، ۰ = ناشناس) |
| `is_deleted`    | `Int8`                    | وضعیت حذف شدن پروفایل کاربر (۱ = حذف‌شده، ۰ = فعال)   |
| `version`       | `UInt64`                  | شماره نسخه به‌روزرسانی مشخصات کاربر                   |
| `last_seen_at`  | `Nullable(DateTime64(3))` | آخرین زمانی که از کاربر فعالیتی ثبت شده است           |
| `created_at`    | `DateTime64(3)`           | زمان اولین ثبت‌نام یا مشاهده کاربر در سیستم           |

---

## جدول `posthog.session_replay_events`

| نام ستون              | نوع داده (Data Type)   | توضیح و کاربرد فارسی                             |
| --------------------- | ---------------------- | ------------------------------------------------ |
| `session_id`          | `String`               | شناسه اختصاصی نشست ضبط‌شده                       |
| `team_id`             | `Int64`                | شناسه پروژه مرتبط                                |
| `distinct_id`         | `String`               | شناسه کاربر دارنده نشست                          |
| `min_first_timestamp` | `DateTime64(6, 'UTC')` | زمان دقیق شروع ضبط نشست                          |
| `max_last_timestamp`  | `DateTime64(6, 'UTC')` | زمان دقیق پایان ضبط نشست                         |
| `all_urls`            | `Array(String)`        | لیست تمام آدرس‌های وب بازدیدشده در طول نشست      |
| `click_count`         | `Int64`                | تعداد کل کلیک‌های ثبت‌شده در نشست                |
| `keypress_count`      | `Int64`                | تعداد فشردن کلیدهای کیبورد توسط کاربر            |
| `active_milliseconds` | `Int64`                | زمان فعال بودن کاربر در طول نشست (به میلی‌ثانیه) |
| `console_error_count` | `Int64`                | تعداد خطاهای کنسول مرورگر ثبت‌شده در نشست        |
