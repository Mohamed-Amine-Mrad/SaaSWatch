
import csv
import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from faker import Faker

# ==================================================
# 1. REPRODUCIBILITY
# ==================================================

SEED = 42
random.seed(SEED)

fake = Faker()
Faker.seed(SEED)

REFERENCE_TIME = datetime(
    2026, 11, 26, 12, 0, 0, tzinfo=timezone.utc
)

# ==================================================
# 2. PROJECT PATHS
# ==================================================

ROOT = Path(__file__).resolve().parent.parent

CSV_DIR = ROOT / "data" / "samples" / "csv"
JSON_DIR = ROOT / "data" / "samples" / "json"

CSV_DIR.mkdir(parents=True, exist_ok=True)
JSON_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# 3. DATASET CONFIGURATION
# ==================================================

TOTAL_RECORDS = 1000

EVENT_DISTRIBUTION = {
    "web_access": 250,
    "application": 250,
    "database": 200,
    "performance": 150,
    "business": 150,
}

FIELDS = [
    "timestamp",
    "level",
    "service",
    "environment",
    "host",
    "source_ip",
    "method",
    "endpoint",
    "status_code",
    "response_time_ms",
    "message",
    "user_id",
    "request_id",
    "event_type",
    "database_operation",
    "database_name",
    "cpu_usage_percent",
    "memory_usage_mb",
    "business_action",
    "business_value",
    "sql_query",
    "query_duration_ms",
    "session_id",
    "session_event",
    "feature_name",
]

SERVICES = {
    "web_access": [
        "api-gateway",
        "auth-service",
        "user-service",
    ],
    "application": [
        "auth-service",
        "payment-service",
        "user-service",
        "subscription-service",
        "notification-service",
    ],
    "database": [
        "database-service",
        "payment-service",
        "user-service",
    ],
    "performance": [
        "monitoring-agent",
        "api-gateway",
        "payment-service",
    ],
    "business": [
        "payment-service",
        "subscription-service",
        "user-service",
    ],
}

LEVEL_WEIGHTS = {
    "web_access": [75, 15, 8, 2],
    "application": [70, 18, 10, 2],
    "database": [65, 20, 13, 2],
    "performance": [20, 60, 15, 5],
    "business": [80, 10, 8, 2],
}

LEVELS = ["INFO", "WARNING", "ERROR", "CRITICAL"]

DATABASE_OPERATIONS = [
    "SELECT",
    "INSERT",
    "UPDATE",
    "DELETE",
]

DATABASE_NAMES = [
    "users_db",
    "payments_db",
    "subscriptions_db",
    "notifications_db",
]

SQL_QUERIES = {
    "SELECT": [
        "SELECT * FROM users WHERE id = ?",
        "SELECT * FROM payments WHERE user_id = ?",
        "SELECT * FROM subscriptions WHERE user_id = ?",
    ],
    "INSERT": [
        "INSERT INTO users (name, email) VALUES (?, ?)",
        "INSERT INTO payments (user_id, amount) VALUES (?, ?)",
    ],
    "UPDATE": [
        "UPDATE subscriptions SET status = ? WHERE id = ?",
        "UPDATE users SET email = ? WHERE id = ?",
    ],
    "DELETE": [
        "DELETE FROM notifications WHERE id = ?",
    ],
}

BUSINESS_ACTIONS = [
    "payment_completed",
    "subscription_created",
    "subscription_cancelled",
    "user_registered",
    "invoice_generated",
]

FEATURE_MAPPING = {
    "payment_completed": "payment_management",
    "subscription_created": "subscription_management",
    "subscription_cancelled": "subscription_management",
    "user_registered": "user_management",
    "invoice_generated": "billing",
}

MESSAGES = {
    "web_access": [
        "HTTP request processed",
        "HTTP request rejected",
        "Unauthorized access attempt",
        "Endpoint unavailable",
    ],
    "application": [
        "User logged in successfully",
        "Payment processing failed",
        "Subscription created",
        "External service unavailable",
        "Application exception detected",
    ],
    "database": [
        "Database query executed",
        "Database connection established",
        "Database connection pool nearly full",
        "Database query failed",
        "Database unavailable",
    ],
    "performance": [
        "Performance metrics collected",
        "High CPU utilization detected",
        "Memory consumption above threshold",
        "High response time detected",
    ],
    "business": [
        "Payment completed",
        "Subscription created",
        "Subscription cancelled",
        "New user registered",
        "Invoice generated",
        "Business transaction failed",
    ],
}

# ==================================================
# 4. HELPER FUNCTIONS
# ==================================================

def generate_timestamp():
    timestamp = REFERENCE_TIME - timedelta(
        seconds=random.randint(0, 7 * 24 * 3600)
    )

    return timestamp.isoformat(
        timespec="milliseconds"
    ).replace("+00:00", "Z")


def generate_level(event_type):
    return random.choices(
        LEVELS,
        weights=LEVEL_WEIGHTS[event_type],
        k=1,
    )[0]


def generate_status_code(level):
    if level == "INFO":
        return random.choice([200, 201, 204])

    if level == "WARNING":
        return random.choice([200, 429, 503])

    if level == "ERROR":
        return random.choice([400, 401, 404, 500, 502])

    return random.choice([500, 502, 503])


# ==================================================
# 5. LOG GENERATION
# ==================================================

def generate_log(index, event_type):

    level = generate_level(event_type)

    record = {
        "timestamp": generate_timestamp(),
        "level": level,
        "service": random.choice(SERVICES[event_type]),
        "environment": random.choices(
            ["production", "staging", "development"],
            weights=[75, 15, 10],
            k=1,
        )[0],
        "host": f"server-{random.randint(1, 5):02d}",
        "source_ip": fake.ipv4_private(),
        "method": "",
        "endpoint": "",
        "status_code": "",
        "response_time_ms": random.randint(10, 3000),
        "message": random.choice(MESSAGES[event_type]),
        "user_id": f"user_{random.randint(1, 200):03d}",
        "request_id": str(uuid.uuid5(
            uuid.NAMESPACE_DNS,
            f"saaswatch-{SEED}-{index}",
        )),
        "event_type": event_type,
        "database_operation": "",
        "database_name": "",
        "cpu_usage_percent": "",
        "memory_usage_mb": "",
        "business_action": "",
        "business_value": "",
	"sql_query": "",
        "query_duration_ms": "",
        "session_id": "",
        "session_event": "",
        "feature_name": "",
    }

    # Web access events
    if event_type == "web_access":
        record.update({
            "method": random.choice(
                ["GET", "POST", "PUT", "DELETE"]
            ),
            "endpoint": random.choice([
                "/api/login",
                "/api/users",
                "/api/payments",
                "/api/subscriptions",
                "/api/notifications",
            ]),
            "status_code": generate_status_code(level),
        })

    # Database events
    elif event_type == "database":
        operation = random.choice(DATABASE_OPERATIONS)

        record.update({
            "database_operation": operation,
            "database_name": random.choice(DATABASE_NAMES),
            "sql_query": random.choice(SQL_QUERIES[operation]),
            "query_duration_ms": random.randint(5, 5000),
        })

    # Performance events
    elif event_type == "performance":
        record.update({
            "cpu_usage_percent": round(
                random.uniform(5, 99), 2
            ),
            "memory_usage_mb": random.randint(100, 4096),
        })

    # Business events
    elif event_type == "business":
        action = random.choice(BUSINESS_ACTIONS)

        business_value = ""

        if action in [
            "payment_completed",
            "invoice_generated",
        ]:
            business_value = round(
                random.uniform(10, 2000), 2
            )

        record.update({
            "business_action": action,
            "business_value": business_value,
	    "feature_name": FEATURE_MAPPING[action],
        })

    return record


# ==================================================
# 6. VALID DATASET GENERATION
# ==================================================
def enrich_user_sessions(records):

    application_records = [
        r for r in records
        if r["event_type"] == "application"
    ]

    for i in range(0, len(application_records) - 1, 2):

        start_record = application_records[i]
        end_record = application_records[i + 1]

        session_id = str(uuid.uuid5(
            uuid.NAMESPACE_DNS,
            f"saaswatch-session-{SEED}-{i}"
        ))

        duration = random.randint(60, 43200)

        start_time = REFERENCE_TIME - timedelta(
            seconds=random.randint(
                duration,
                7 * 24 * 3600
            )
        )

        end_time = start_time + timedelta(
            seconds=duration
        )

        user_id = f"user_{random.randint(1, 200):03d}"

        start_record.update({
            "user_id": user_id,
            "session_id": session_id,
            "session_event": "login",
            "timestamp": start_time.isoformat(
                timespec="milliseconds"
            ).replace("+00:00", "Z"),
        })

        end_record.update({
            "user_id": user_id,
            "session_id": session_id,
            "session_event": "logout",
            "timestamp": end_time.isoformat(
                timespec="milliseconds"
            ).replace("+00:00", "Z"),
        })

def generate_valid_datasets():

    event_types = []

    for event_type, count in EVENT_DISTRIBUTION.items():
        event_types.extend([event_type] * count)

    random.shuffle(event_types)

    records = [
        generate_log(index, event_type)
        for index, event_type in enumerate(
            event_types, start=1
        )
    ]
    enrich_user_sessions(records)

    csv_path = CSV_DIR / "saas_logs.csv"
    json_path = JSON_DIR / "saas_logs.jsonl"

    # Generate CSV
    with csv_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
            lineterminator="\n",
        )

        writer.writeheader()
        writer.writerows(records)

    # Generate JSON Lines
    with json_path.open(
        "w", encoding="utf-8"
    ) as file:

        for record in records:
            file.write(json.dumps(record) + "\n")

    return records, csv_path, json_path


# ==================================================
# 7. MALFORMED TEST DATASETS
# ==================================================

def generate_malformed_datasets(records):

    malformed_csv = CSV_DIR / "saas_logs_malformed.csv"
    malformed_json = JSON_DIR / "saas_logs_malformed.jsonl"

    with malformed_csv.open(
        "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
            lineterminator="\n",
        )

        writer.writeheader()
        writer.writerow(records[0])

        writer.writerow({
            **records[1],
            "timestamp": "NOT_A_TIMESTAMP",
            "status_code": "INVALID",
        })

        file.write('"broken CSV record\n')

    with malformed_json.open(
        "w", encoding="utf-8"
    ) as file:

        file.write(json.dumps(records[0]) + "\n")
        file.write('{"level": "ERROR", "message":\n')
        file.write('"this is not a JSON object"\n')


# ==================================================
# 8. MAIN
# ==================================================

def main():

    records, csv_path, json_path = generate_valid_datasets()

    generate_malformed_datasets(records)

    print("=" * 50)
    print("SaaSWatch Log Dataset Generation")
    print("=" * 50)

    print(f"Valid records: {len(records)}")

    print("\nEvent distribution:")

    for event_type, expected in EVENT_DISTRIBUTION.items():
        actual = sum(
            r["event_type"] == event_type
            for r in records
        )

        print(f"{event_type}: {actual}/{expected}")

    print(f"\nCSV: {csv_path}")
    print(f"JSONL: {json_path}")

    print("Malformed CSV and JSONL test files generated.")
    print(f"Random seed: {SEED}")


if __name__ == "__main__":
    main()
