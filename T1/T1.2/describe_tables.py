import clickhouse_connect

client = clickhouse_connect.get_client(
    host="localhost", port=8123, username="default", password=""
)

tables = ["events", "person", "session_replay_events"]

for table in tables:
    print(f"\n{'='*20} Schema for: posthog.{table} {'='*20}")
    try:
        result = client.query(f"DESCRIBE posthog.{table}")
        for row in result.result_rows:
            # row[0]: name, row[1]: type
            print(f"Column: {row[0]:<30} | Type: {row[1]}")
    except Exception as e:
        print(f"Error fetching schema for {table}: {e}")