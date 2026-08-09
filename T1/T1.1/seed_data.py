from datetime import datetime
import uuid
import clickhouse_connect

# اتصال مستقیم به ClickHouse
client = clickhouse_connect.get_client(
    host="localhost", port=8123, username="default", password=""
)

print("در حال تزریق ۱۲۰ رویداد تستی به ClickHouse...")

# ساخت ۱۲۰ ردیف داده
data = []
now = datetime.now()
event_types = [
    "$pageview",
    "click",
    "submit",
    "$feature_flag_called",
    "decision_made",
]

for i in range(120):
    row = [
        uuid.uuid4(),  # uuid
        event_types[i % len(event_types)],  # event
        '{"browser": "Chrome", "latency_ms": 250}',  # properties
        now,  # timestamp
        1,  # team_id
        f"user_{i % 10}",  # distinct_id
        now,  # created_at
    ]
    data.append(row)

# درج مستقیم در جدول sharded_events
client.insert(
    "posthog.sharded_events",
    data,
    column_names=[
        "uuid",
        "event",
        "properties",
        "timestamp",
        "team_id",
        "distinct_id",
        "created_at",
    ],
)

print("تزریق داده‌ها با موفقیت انجام شد!")