# مستند Schema داده‌های PostHog (T1.2)

این مستند نتیجه اجرای کوئری `DESCRIBE TABLE` روی سه جدول اصلی PostHog در ClickHouse است.
برای هر جدول، نام ستون، نوع داده و توضیح کاربرد آن (بر اساس مستندات رسمی PostHog و ساختار استاندارد آن) آورده شده است.

---

## ۱. جدول `events`

جدول اصلی و پرحجم‌ترین جدول PostHog که تمام رویدادهای رخ‌داده در سمت کاربر (کلیک، بازدید صفحه، ثبت فرم و غیره) را ذخیره می‌کند.

| ستون | نوع داده | توضیح / کاربرد |
|---|---|---|
| uuid | UUID | شناسه یکتای هر رکورد رویداد |
| event | String | نام رویداد (مثل `$pageview`، `click`، `submit`، `decision_made`) |
| properties | String | ویژگی‌های رویداد به‌صورت JSON (مثل URL صفحه، مرورگر، مقادیر سفارشی) |
| timestamp | DateTime64(6, 'UTC') | زمان دقیق وقوع رویداد (میکروثانیه، UTC) |
| team_id | Int64 | شناسه پروژه/تیم مربوط به این رویداد در PostHog |
| distinct_id | String | شناسه یکتای کاربر (قبل یا بعد از شناسایی/identify) |
| elements_chain | String | زنجیره عناصر DOM که رویداد کلیک روی آن‌ها رخ داده (برای autocapture) |
| created_at | DateTime64(6, 'UTC') | زمان درج رکورد در دیتابیس |
| person_id | UUID | شناسه یکتای فرد (person) مرتبط با این رویداد |
| person_created_at | DateTime64(3) | زمان ایجاد رکورد person مرتبط |
| person_properties | String | ویژگی‌های person در لحظه ثبت رویداد (JSON) |
| group0_properties ... group4_properties | String | ویژگی‌های گروه‌های سازمانی (مثل شرکت، تیم) مرتبط با رویداد؛ PostHog تا ۵ نوع گروه پشتیبانی می‌کند |
| group0_created_at ... group4_created_at | DateTime64(3) | زمان ایجاد هر گروه مرتبط |
| person_mode | Enum8 | حالت ذخیره اطلاعات person (`full`, `propertyless`, `force_upgrade`) برای بهینه‌سازی حجم |
| historical_migration | Bool | مشخص می‌کند آیا رکورد از یک migration تاریخی وارد شده یا خیر |
| dmat_string_0 ... dmat_string_9 | Nullable(String) | ستون‌های materialized پویا برای ذخیره‌سازی بهینه ویژگی‌های پرکاربرد رشته‌ای (بهینه‌سازی داخلی ClickHouse) |
| $group_0 ... $group_4 | String | کلید گروه‌بندی مرتبط با هر نوع گروه (identifier گروه) |
| $window_id | String | شناسه پنجره مرورگر برای دنبال‌کردن session در سمت کلاینت |
| $session_id | String | شناسه session کاربر (برای گروه‌بندی رویدادهای یک نشست) |
| $session_id_uuid | Nullable(UInt128) | نسخه عددی/UUID شناسه session برای بهینه‌سازی join و فیلتر |
| elements_chain_href | String | لینک (href) عنصری که کلیک روی آن رخ داده |
| elements_chain_texts | Array(String) | متن‌های موجود در زنجیره عناصر کلیک‌شده |
| elements_chain_ids | Array(String) | مقادیر id عناصر HTML در زنجیره کلیک |
| elements_chain_elements | Array(Enum8) | نوع تگ‌های HTML موجود در زنجیره (a, button, form, input, select, textarea, label) |
| properties_group_custom | Map(String, String) | نگاشت ویژگی‌های سفارشی رویداد (بهینه‌شده به‌صورت Map) |
| properties_group_ai | Map(String, String) | ویژگی‌های مرتبط با رویدادهای هوش مصنوعی (مثل LLM tracking) |
| properties_group_feature_flags | Map(String, String) | مقادیر فیچر فلگ‌های فعال در لحظه وقوع رویداد |
| person_properties_map_custom | Map(String, String) | نگاشت ویژگی‌های سفارشی person (بهینه‌شده) |
| _timestamp | DateTime | زمان دریافت پیام توسط pipeline پردازش (Kafka ingestion) |
| _offset | UInt64 | آفست پیام در صف Kafka (برای ردیابی پردازش) |
| inserted_at | Nullable(DateTime64(6, 'UTC')) | زمان واقعی درج رکورد در ClickHouse |
| consumer_breadcrumbs | Array(String) | ردپای سرویس‌های consumer که این رکورد از آن‌ها عبور کرده (برای دیباگ pipeline) |
| is_deleted | Bool | مشخص می‌کند رکورد حذف منطقی شده یا خیر |
| mat_$ai_trace_id | Nullable(String) | شناسه trace برای ردیابی زنجیره فراخوانی‌های AI |
| mat_$ai_session_id | Nullable(String) | شناسه session مکالمه/فراخوانی AI |
| mat_$ai_is_error | Nullable(String) | مشخص می‌کند فراخوانی AI با خطا مواجه شده یا خیر |
| mat_$ai_prompt_name | Nullable(String) | نام پرامپت استفاده‌شده در فراخوانی AI |
| mat_$ai_experiment_id | Nullable(String) | شناسه آزمایش AI مرتبط (در صورت وجود) |

---

## ۲. جدول `person`

اطلاعات مربوط به هر کاربر/فرد شناسایی‌شده در سیستم را نگه می‌دارد (پروفایل کاربر).

| ستون | نوع داده | توضیح / کاربرد |
|---|---|---|
| id | UUID | شناسه یکتای فرد (person) در سیستم |
| created_at | DateTime64(3) | زمان ایجاد اولین رکورد این فرد |
| team_id | Int64 | شناسه پروژه/تیمی که این فرد به آن تعلق دارد |
| properties | String | ویژگی‌های فرد به‌صورت JSON (مثل ایمیل، نام، ویژگی‌های سفارشی) |
| is_identified | Int8 | مشخص می‌کند آیا فرد از طریق `identify()` شناسایی شده یا هنوز ناشناس (anonymous) است |
| is_deleted | Int8 | مشخص می‌کند رکورد این فرد حذف منطقی شده یا خیر |
| version | UInt64 | شماره نسخه رکورد؛ برای مدیریت به‌روزرسانی‌های همزمان (ReplacingMergeTree) استفاده می‌شود |
| last_seen_at | Nullable(DateTime64(3)) | آخرین زمانی که فعالیتی از این فرد ثبت شده |
| _timestamp | DateTime | زمان دریافت رکورد توسط pipeline پردازش (Kafka ingestion) |
| _offset | UInt64 | آفست پیام در صف Kafka برای ردیابی پردازش |

> نکته: نام واقعی این جدول در ClickHouse به‌صورت مفرد `person` است (نه `persons`).

---

## ۳. جدول `session_replay_events`

جدولی تجمیعی (aggregated) که خلاصه هر نشست ضبط‌شده کاربر (session replay) را نگه می‌دارد؛ برای بازپخش و تحلیل رفتار بصری کاربر استفاده می‌شود.

| ستون | نوع داده | توضیح / کاربرد |
|---|---|---|
| session_id | String | شناسه یکتای نشست ضبط‌شده |
| team_id | Int64 | شناسه پروژه/تیم مرتبط با این نشست |
| distinct_id | String | شناسه کاربری که این نشست به او تعلق دارد |
| min_first_timestamp | SimpleAggregateFunction(min) | اولین زمان ثبت‌شده در این نشست |
| max_last_timestamp | SimpleAggregateFunction(max) | آخرین زمان ثبت‌شده در این نشست |
| block_first_timestamps | SimpleAggregateFunction(groupArrayArray) | زمان شروع هر بلوک (chunk) ضبط‌شده نشست |
| block_last_timestamps | SimpleAggregateFunction(groupArrayArray) | زمان پایان هر بلوک ضبط‌شده نشست |
| block_urls | SimpleAggregateFunction(groupArrayArray) | آدرس صفحاتی که در هر بلوک نشست بازدید شده |
| first_url | AggregateFunction(argMin) | اولین URL بازدیدشده در این نشست |
| all_urls | SimpleAggregateFunction(groupUniqArrayArray) | مجموعه یکتای همه URL های بازدیدشده در نشست |
| click_count | SimpleAggregateFunction(sum) | مجموع تعداد کلیک‌های ثبت‌شده در نشست |
| keypress_count | SimpleAggregateFunction(sum) | مجموع تعداد ضربه‌های کیبورد ثبت‌شده |
| mouse_activity_count | SimpleAggregateFunction(sum) | مجموع تعداد فعالیت‌های موس (حرکت/کلیک) |
| active_milliseconds | SimpleAggregateFunction(sum) | مجموع میلی‌ثانیه‌های فعال بودن کاربر در نشست |
| console_log_count | SimpleAggregateFunction(sum) | تعداد پیام‌های لاگ کنسول مرورگر در طول نشست |
| console_warn_count | SimpleAggregateFunction(sum) | تعداد پیام‌های هشدار (warn) کنسول مرورگر |
| console_error_count | SimpleAggregateFunction(sum) | تعداد پیام‌های خطای کنسول مرورگر |
| size | SimpleAggregateFunction(sum) | حجم کل داده ضبط‌شده این نشست (بایت) |
| message_count | SimpleAggregateFunction(sum) | تعداد پیام‌های خام rrweb ثبت‌شده در نشست |
| event_count | SimpleAggregateFunction(sum) | تعداد کل رویدادهای ضبط‌شده در نشست |
| snapshot_source | AggregateFunction(argMin) | منبع ضبط نشست (مثل web، mobile) |
| snapshot_library | AggregateFunction(argMin) | نسخه/کتابخانه SDK استفاده‌شده برای ضبط |
| _timestamp | SimpleAggregateFunction(max) | آخرین زمان دریافت داده توسط pipeline پردازش |
| is_deleted | SimpleAggregateFunction(max) | مشخص می‌کند نشست حذف منطقی شده یا خیر |
| ai_tags_fixed | SimpleAggregateFunction(groupUniqArrayArray) | برچسب‌های از پیش تعریف‌شده AI برای این نشست (تحلیل هوشمند) |
| ai_tags_freeform | SimpleAggregateFunction(groupUniqArrayArray) | برچسب‌های آزاد تولیدشده توسط AI برای این نشست |
| ai_highlighted | SimpleAggregateFunction(max) | مشخص می‌کند این نشست توسط AI به‌عنوان قابل‌توجه (highlighted) علامت خورده یا خیر |
| surfacing_score | SimpleAggregateFunction(max) | امتیاز اولویت نمایش این نشست (برای برجسته‌سازی نشست‌های مهم) |
| retention_period_days | SimpleAggregateFunction(max) | تعداد روزهایی که این نشست باید نگهداری شود پیش از حذف خودکار |

---

## جمع‌بندی

سه جدول اصلی مورد بررسی قرار گرفتند:

1. **events** — رویدادهای خام رفتار کاربر (کلیک، بازدید، ثبت فرم و ...)
2. **person** — پروفایل و ویژگی‌های هر کاربر شناسایی‌شده
3. **session_replay_events** — خلاصه تجمیعی نشست‌های ضبط‌شده برای بازپخش رفتار کاربر

این سه جدول پایه اصلی تحلیل‌های شناختی (Cognitive Data Analysis) در تسک‌های بعدی (T1.3 به بعد) خواهند بود؛ به‌ویژه ستون‌های `event`، `timestamp`، `distinct_id` و `properties` از جدول `events` که برای استخراج رویدادهای مرتبط با تصمیم‌گیری کاربر (T1.3) کلیدی هستند.